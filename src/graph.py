from log import Log
Log.init()

try:
    Log.info(f"Importation du paquet 're'")
    import re

    Log.info(f"Importation du paquet 'networkx'")
    import networkx as nx

    Log.info(f"Importation du paquet 'matplotlib.pyplot'")
    import matplotlib.pyplot as plt

    Log.info(f"Importation du paquet 'pickle'")
    import pickle

except ModuleNotFoundError as e:
    Log.critical(f"Erreur lors de l'importation des paquets. Si les paquets ne sont pas présents sur votre machine, vous pourriez envisager d'utiliser l'environnement python 'env'. ", e)


G = nx.Graph()

class WordGraph:
    def __init__(self):
        Log.info("Initialisation du graphe")
        self.__graph = nx.Graph()   # Graphe comportant les mots et leur lien

    def draw(self):
        pos = nx.spring_layout(self.__graph)
        node_sizes = self.word_frequency.values()
        nx.draw(self.__graph, pos, with_labels=True, node_size=node_sizes, node_color="skyblue")

        edge_labels = nx.get_edge_attributes(self.__graph, 'weight')
        nx.draw_networkx_edge_labels(self.__graph, pos, edge_labels=edge_labels)

        plt.title("Graphe des mots")
        plt.show()

    @property
    def words(self) -> list:
        return list(self.__graph.nodes)
    
    @property
    def word_frequency(self):
        return {node: self.__graph.nodes[node]['value'] for node in self.__graph.nodes}
    
    def save(self, path: str):
        save_test = Log.check(f"Sauvegarde des données dans le fichier '{path}'")
        try:
            with open(path, 'wb') as file:
                pickle.dump(self, file)
                save_test.check()
        except Exception as e:
            Log.error(f"Impossible de sauvegarder l'objet dans le fichier '{path}'", e)
            save_test.fail()
    
    @classmethod
    def load(cls, path: str):
        load_test = Log.check(f"Chargement des données depuis le fichier '{path}'")
        try:
            with open(path, 'rb') as file:
                load_test.check()
                return pickle.load(file)
        except Exception as e:
            load_test.fail()
            Log.error(f"Impossible de charger l'objet du fichier '{path}'", e)
            return None

    def add_word(self, word: str):
        if word in self.words:
            self.__graph.nodes[word]['value'] += 1 
        else:
            self.__graph.add_node(word, value=1)

    def link(self, w1: str, w2: str) -> int:
        if w1 in self.words and w1 in self.words:
            if self.__graph.has_edge(w1, w2):
                return self.__graph[w1][w2]['weight']
        return 0

    def add_link(self, w1: str, w2: str):
        if self.link(w1, w2):
            self.__graph[w1][w2]['weight'] += 1
        else:
            self.__graph.add_edge(w1, w2, weight=1)

    def sentence_analysis(self, sentence: str) -> list:
        words = re.findall(r"\b\w+\b", sentence)
        for i in range(len(words)):  
            words[i] = words[i].lower()  
            self.add_word(words[i])

        for i, w1 in enumerate(words):
            for w2 in words[i+1:]:
                self.add_link(w1, w2)
        return words

    def text_analysis(self, text: str) -> list:
        test = Log.check("Analyse du texte")
        sentences = re.findall(r"[^.!?]*[.!?]", text)
        all_words = []
        # Utilisation correcte de la méthode progress de Log
        for sentence in Log.progress(sentences, "Analyse des phrases"):
            words_in_sentence = self.sentence_analysis(sentence)
            all_words.append(words_in_sentence)
        test.check()
        return all_words
    
    def file_analysis(self, path: str):
        try:
            with open(path, 'r', encoding="utf-8") as file:
                text = file.read()
                self.text_analysis(text)
        except Exception as e:
            Log.error(f"Erreur à la lecture du fichier '{path}'", e)
