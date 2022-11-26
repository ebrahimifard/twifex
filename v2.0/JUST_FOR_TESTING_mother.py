
from JUST_FOR_TESTING_father import Father


class Mother:
    def __init__(self, arg_a, arg_b):
        self._var1 = arg_a
        self._var2 = arg_b

    def get_first_var(self):
        return self._var1

    def get_second_var(self):
        return self._var2

    def father_func(self):
        return Father(self._var1, self._var2)

