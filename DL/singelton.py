import sqlite3
from sqlite3 import Error

class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            print('Singleton instance creating')
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class DBConnection(object):

    def __init__(self):
        self.__db = None
        try:
            self.__db = sqlite3.connect('pagesDB')
            print(sqlite3.version)
        except Error as e:
            print(e)

    def __del__(self):
        self.__db.close()


    def __str__(self):
        return 'Database connection object'


c1 = DBConnection.Instance()
c2 = DBConnection.Instance()

print("Id of c1 : {}".format(str(id(c1))))
print("Id of c2 : {}".format(str(id(c2))))

print("c1 is c2 ? " + str(c1 is c2))
