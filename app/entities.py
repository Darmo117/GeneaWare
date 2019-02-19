from .utils import LastName, Event


class Person:
    def __init__(self, lastname: LastName, firstnames, birthday: Event, death: Event):
        self.__lastname = lastname
        self.__firstnames = firstnames
        self.__birthday = birthday
        self.__death = death
