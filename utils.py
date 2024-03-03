def get_default_code():
    return  """
# This is an example code. You can write your own code here.
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."

class Student(Person):
    def __init__(self, name, age, major):
        super().__init__(name, age)
        self.major = major

    def greet(self):
        return f"{super().greet()} I'm studying {self.major}."

# Create a Person and a Student
person = Person("Alice", 30)
student = Student("Bob", 20, "Computer Science")

# Print their greetings
print(person.greet())
print(student.greet())
    """