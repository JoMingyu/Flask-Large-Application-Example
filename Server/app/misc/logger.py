from termcolor import colored


def logger(message: str, type: str="WARN"):
    if type == "WARN":
        print(colored('[WARN]', 'yellow'), message)
    elif type == "ERROR":
        print(colored('[ERROR] ' + message, 'red'))
    elif type == "INFO":
        print(colored('[INFO]', 'blue'), message)
