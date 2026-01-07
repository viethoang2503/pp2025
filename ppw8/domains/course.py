class Course:
    def __init__(self, course_id=None, name=None, credits=0):
        self.__id = course_id
        self.__name = name
        self.__credits = credits

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_credits(self):
        return self.__credits

    def __str__(self):
        return f"ID: {self.__id} | Course: {self.__name} | Credits: {self.__credits}"