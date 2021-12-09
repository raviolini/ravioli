"""
    Logging and message printing utility
"""

from colorama import Fore

def message_info(info: str, second_arg = ""):
    """
        Print informaton level message
    """

    message = Fore.GREEN + f"[INFO] : {info} {second_arg}" + Fore.RESET
    print(message)

def message_warn(warning: str, second_arg = ""):
    """
        Print warning level message
    """

    message = Fore.YELLOW + f"[WARNING] : {warning} {second_arg}" + Fore.RESET
    print(message)

def compose_info(message, second_arg = ""):
    """
        Compose information level message
    """

    message = Fore.GREEN + f"[INFO] : {message} {second_arg}" + Fore.RESET
    return message

def compose_warn(message, second_arg = " "):
    """
        Compose warning level message
    """

    message = Fore.YELLOW + f"[WARNING] : {message} {second_arg}" + Fore.RESET
    return message

def test():
    """
        Helper function to display how logging looks like
    """

    message_info("testing the message function")
    message_warn("testing the W function")

    message_info("this is message_info() without second arg")
    message_info("this is message_info() with second arg,","hello i'm the second arg")

    message_warn("this is message_W() without second arg")
    message_warn("this is message_W() with second arg,","hello i'm the second arg")

if __name__ == '__main__':
    test()
