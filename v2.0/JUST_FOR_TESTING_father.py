
class Father:
    def __init__(self, first, second):
        self._first = first
        self._second = second

    def change_first(self, para1):
        self._first.update(para1)
        # self._first.append(para1)

    def change_second(self, para2):
        # self._second.append(para2)
        self._second.update(para2)

    def get_first(self):
        return self._first

    def get_second(self):
        return self._second
