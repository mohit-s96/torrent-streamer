class printcolor:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

    def error(self, text):
        print(self.RED + text + self.RESET)

    def success(self, text):
        print(self.GREEN + text + self.RESET)

    def warning(self, text):
        print(self.YELLOW + text + self.RESET)

    def message(self, text):
        print(self.CYAN + text + self.RESET)

    def info(self, text):
        print(self.BLUE + text + self.RESET)


colors = printcolor()
