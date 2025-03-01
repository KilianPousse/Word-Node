import sys
import time
from tqdm import tqdm

class LogCheck:
    __checks = {}
    __id_counter = 0

    def __init__(self, msg: str, line: int =0, id: int=0):
        if id <= 0 or id in self.__checks:
            self.__id = LogCheck.id_generate()
        else:
            self.__id = id
        LogCheck.__checks[self.id] = self
        self.__line = line
        self.__msg = msg

    @classmethod
    def id_generate(cls) -> int:
        cls.__id_counter += 1
        return cls.__id_counter
    
    @classmethod
    def all_checks(cls) -> dict:
        return cls.__checks

    @property
    def id(self):
        return self.__id

    def check(self):
        Log.write_on_line(self.__line, self.__msg+"OK")

    def fail(self):
        Log.error(f"Check with identifier {self.id} failed.")
        Log.write_on_line(self.__line, self.__msg + "FAILURE")

class Log:
    __debug_mode = False
    __captured_output = []
    output = None
    __start_ts = None

    COLOR_RESET         = "\033[0m"
    COLOR_BLACK         = "\033[30m"
    COLOR_RED           = "\033[31m"
    COLOR_GREEN         = "\033[32m"
    COLOR_YELLOW        = "\033[33m"
    COLOR_BLUE          = "\033[34m"
    COLOR_MAGENTA       = "\033[35m"
    COLOR_CYAN          = "\033[36m"
    COLOR_WHITE         = "\033[37m"
    COLOR_LIGHT_GRAY    = "\033[90m"
    COLOR_LIGHT_RED     = "\033[91m"
    COLOR_LIGHT_GREEN   = "\033[92m"
    COLOR_LIGHT_YELLOW  = "\033[93m"
    COLOR_LIGHT_BLUE    = "\033[94m"
    COLOR_LIGHT_MAGENTA = "\033[95m"
    COLOR_LIGHT_CYAN    = "\033[96m"
    COLOR_LIGHT_WHITE   = "\033[97m"

    stdout = None

    @classmethod
    def init(cls):
        cls.__captured_output = []
        cls.stdout = DualOutput(cls.__captured_output)
        cls.output = cls.stdout
        sys.stdout = cls.output
        cls.__start_ts = time.time()

    @classmethod
    def set_debug_mode(cls, enabled: bool):
        cls.__debug_mode = enabled

    @classmethod
    def debug_mode(cls) -> bool:
        return cls.__debug_mode
    
    @classmethod
    def start_time(cls) -> float:
        return cls.__start_ts
    
    @classmethod
    def __line_with_type(cls, log_type: str, type_color: str, msg: str) -> str:
        return f"{cls.COLOR_RESET}[{type_color}{log_type}{cls.COLOR_RESET}]: {msg}"

    @classmethod
    def __write_type(cls, log_type: str, type_color: str, msg: str) -> str:
        line = cls.__line_with_type(log_type, type_color, msg)
        print(line)
        return line

    @classmethod
    def write(cls, msg: str):
        print(msg)

    @classmethod
    def write_on_line(cls, line: int, msg: str):
        steps = cls.output.line - line + 1
        print(f"\033[{steps}A\033[K"+msg+f"\033[{steps-1}B")

    @classmethod
    def info(cls, msg: str):
        cls.__write_type("INFO", cls.COLOR_CYAN, msg)

    @classmethod
    def debug(cls, msg: str):
        if cls.__debug_mode:
            cls.__write_type("DEBUG", cls.COLOR_LIGHT_GRAY, msg)
    
    @classmethod
    def __write_error(cls, e: Exception) -> str:
        if not e is None:
            return f"\n  --> Error: {e}"
        else:
            return ""

    @classmethod
    def warning(cls, msg: str, e:Exception = None):
        err = cls.__write_error(e)
        cls.__write_type("WARNING", cls.COLOR_LIGHT_YELLOW, msg + err)

    @classmethod
    def error(cls, msg: str, e:Exception = None):
        err = cls.__write_error(e)
        cls.__write_type("ERROR", cls.COLOR_RED, msg + err)

    @classmethod
    def critical(cls, msg: str, e: Exception):
        err = cls.__write_error(e)
        cls.__write_type("CRITICAL", cls.COLOR_MAGENTA, msg + err)
        exit()

    @classmethod
    def check(cls, msg: str) -> LogCheck:
        id = LogCheck.id_generate()
        txt = cls.__write_type(f"CHECK:{id}", cls.COLOR_BLUE, f"{msg} ..... ")
        return LogCheck(txt, cls.output.line, id=id)
    
    @classmethod
    def progress(cls, elem, msg: str):
        # Ajout de la barre de progression à la liste d'éléments (par exemple, les phrases)
        desc = cls.__line_with_type("PROGRESS", cls.COLOR_GREEN, msg)
        cls.output.additional_line += 1
        return tqdm(elem, desc=desc)
    
    @classmethod
    def input(cls, msg: str) -> str:
        cls.__write_type("INPUT", cls.COLOR_YELLOW, msg)
        return input("  > ")
    
    @classmethod
    def input_YorN(cls, msg: str) -> bool:
        cls.__write_type("INPUT", cls.COLOR_YELLOW, msg)
        res = input("  (y/n) > ").lower()
        if res not in ["y", "n"]:
            return cls.input_YorN(cls, msg)
        return True if res == "y" else False
        

class DualOutput:
    def __init__(self, var: list):
        self.list = var  
        self.terminal = sys.stdout  
        self.additional_line = 0

    def write(self, msg: str):
        self.list.append(msg)  
        self.terminal.write(msg) 

    def flush(self):
        self.terminal.flush()  

    @property
    def line(self) -> int:
        return self.text.count('\n') + self.additional_line
    
    @property
    def text(self) -> str:
        return ''.join(self.list)

