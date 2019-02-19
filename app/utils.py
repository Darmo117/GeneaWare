class LastName:
    def __init__(self, label):
        self.__label = label


class Date:
    def __init__(self, day, month, year):
        self.__day = day
        self.__month = month
        self.__year = year


class Place:
    def __init__(self, label, x, y):
        self.__label = label
        self.__x = x
        self.__y = y


class Event:
    def __init__(self, date: Date, place: Place):
        self.__date = date
        self.__place = place
