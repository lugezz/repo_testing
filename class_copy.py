
class A:
    def __init__(self, name, age, basic_list=[]):
        print("A.__init__")
        self.name = name
        self.age = age
        self.basic_list = basic_list

    def copy(self):
        return A(self.name, self.age, self.basic_list.copy())


class_01 = A("Juan", 30, [1, 2, 3])
class_02 = class_01
class_03 = class_01.copy()

print("Dir Class 1", id(class_01))
print("Dir Class 2", id(class_02))
print("Son iguales?", class_01 is class_02)
print("="*100)
print("Class 1:", "name", class_01.name, "age", class_01.age)
print("="*100)

print("Dir Class 1", id(class_01))
print("Dir Class 3", id(class_03))
print("Son iguales?", class_01 is class_03)


print("="*100)
class_03.name = "Pedro"
class_03.basic_list = [4, 5, 6]

print("Class 1:", "name", class_01.name, "age", class_01.age, "Basic List", class_01.basic_list)
print("Class 3:", "name", class_03.name, "age", class_03.age, "Basic List", class_03.basic_list)
