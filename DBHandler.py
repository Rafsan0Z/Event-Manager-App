def DBFactory():
    try:
        new_handler = DBHandler()
    except RuntimeError as r:
        print("You cant request any more handlers!!")
    else:
        return new_handler


class DBHandler:
    
    num = 0

    def __new__(cls, *args, **kawrgs):
        if DBHandler.num > 0:
            raise RuntimeError("You cannot create any more Database Handlers")
        else:
            return super().__new__(cls)
        
    def __init__(self):
        DBHandler.num += 1

    def __del__(self):
        DBHandler.num -= 1
