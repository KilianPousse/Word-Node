# Word-Node

World-Node est un projet personnel visant à créer un logiciel capable d'examiner un texte et d'en extraire des informations. En effet, Word-Node examine les mots présents dans un texte fourni. Ce projet découle de la réflexion qui a suivi les cours de Théorie des graphes de L3-Informatique à l'université du Mans. 

Une analyse permet d'extraire des informations concernant les mots du texte, notamment leurs occurrences et leur relation avec d'autres termes.

## Installation
Vous pouvez installer ce projet directement depuis cette page GitHub ou en utilisant la commande suivant:

```bash
git clone https://github.com/your-username/your-project.git
```

## utilisation 
Exemple d'utilisation:
```python
Log.init()
    
g = WordGraph() 
g.file_analysis("./txt/Les_Miserables.txt")
g.save("Les_Miserables.pkl")
```

## Contribution

#### Auteurs:
- Kilian Pousse: Kilian.Pousse.Etud@univ-lemans.fr