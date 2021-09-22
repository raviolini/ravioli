from colorama import Fore

#message automatic print message
def message_info(message, second_arg = " "):
    Message = Fore.GREEN + "[INFO] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    print(Message)

def message_W(message, second_arg = " "):
    Message = Fore.YELLOW + "[WARNING] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    print(Message)

#compose return composed string
def compose_info(message, second_arg = " "):
    Message = Fore.GREEN + "[INFO] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    return Message

def compose_W(message, second_arg = " "):
    Message = Fore.YELLOW + "[WARNING] : {_message} {_second_arg}".format(_message=message, _second_arg=second_arg)
    return Message

def test():
    message_info("testing the message function")
    message_W("testing the W function")

    message_info("this is message_info() without second arg")
    message_info("this is message_info() with second arg,","hello i'm the second arg")

    message_W("this is message_W() without second arg")
    message_W("this is message_W() with second arg,","hello i'm the second arg")
    
if __name__ == '__main__':
    test()