from colorama import Fore

def message_info(message, second_arg = " "):
    Message = Fore.GREEN + "[INFO] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    print(Message)

def message_warn(message, second_arg = " "):
    Message = Fore.YELLOW + "[WARNING] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    print(Message)

def compose_info(message, second_arg = " "):
    Message = Fore.GREEN + "[INFO] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    return Message

def compose_warn(message, second_arg = " "):
    Message = Fore.YELLOW + "[WARNING] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    return Message

def test():
    message_info("testing the message function")
    message_warn("testing the W function")

    message_info("this is message_info() without second arg")
    message_info("this is message_info() with second arg,","hello i'm the second arg")

    message_warn("this is message_W() without second arg")
    message_warn("this is message_W() with second arg,","hello i'm the second arg")

if __name__ == '__main__':
    test()
