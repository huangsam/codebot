"""
A sample Python script with some code quality issues for testing the code review agent.
"""


def calculate_sum(a, b):
    """Add two numbers"""
    result = a + b
    return result


def divide(x, y):
    # This function has no error handling
    return x / y


class MyClass:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)


if __name__ == "__main__":
    print(calculate_sum(5, 10))
    print(divide(10, 2))
    obj = MyClass("Test")
    obj.print_name()
