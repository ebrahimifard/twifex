
from JUST_FOR_TESTING_mother import Mother

mother_obj = Mother({"er": [11, 12, 33], "vb": [45, 67]}, {"gtr": ["asd", "sdf", "fdg"], "yy": ["er", "cv"]})
print(mother_obj.get_first_var())
print(mother_obj.get_second_var())

print("$$$$$")

print(mother_obj.father_func().get_first())
print(mother_obj.father_func().get_second())

print("@@@@@")

mother_obj.father_func().change_first({"HELLO": 12, 4564: [12, 546, 56]})
mother_obj.father_func().change_second({"BYE": "FDSSDF", "RETTD": [1233333, 31546, "000", 56]})
print(mother_obj.father_func().get_first())
print(mother_obj.father_func().get_second())

print("#####")

print(mother_obj.get_first_var())
print(mother_obj.get_second_var())
