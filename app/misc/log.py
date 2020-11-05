from termcolor import colored


def log(message: str, keyword: str = "WARN"):
    """
    Log a message

    Args:
        message: (str): write your description
        keyword: (str): write your description
    """
    if keyword == "WARN":
        print(colored("[WARN]", "yellow"), message)
    elif keyword == "ERROR":
        print(colored("[ERROR] " + message, "red"))
    elif keyword == "INFO":
        print(colored("[INFO]", "blue"), message)
    else:
        print(colored("[{}]".format(type), "cyan"), message)
