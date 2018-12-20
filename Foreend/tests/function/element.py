class BaseInput():
    """Base page class that is initialized on every page object class."""
    def __init__(self,inp):
        self.__input = inp

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.__input.clear()
        self.__input.send_keys(value)

    @input.getter
    def input(self):
        return self.__input.get_attribute("value")



