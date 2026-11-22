# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: Demonstrates data classes, inheritance, properties, JSON files, and error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   Mahmoud Bza,11/22/2026,Completed data classes and JSON processing
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course.
    2. Show current data.
    3. Save data to a file.
    4. Exit the program.
-----------------------------------------
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []
menu_choice: str = ""


# Data classes --------------------------------------- #
class Person:
    """Represent a person with validated first and last name properties."""

    def __init__(self, first_name: str = "", last_name: str = ""):
        """Initialize a person using the validated property setters."""
        self._first_name = ""
        self._last_name = ""
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self) -> str:
        """Return the person's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        """Require letters in a nonempty first name; allow blank defaults."""
        if not isinstance(value, str) or (value and not value.isalpha()):
            raise ValueError("The first name must contain letters only.")
        self._first_name = value

    @property
    def last_name(self) -> str:
        """Return the person's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        """Require letters in a nonempty last name; allow blank defaults."""
        if not isinstance(value, str) or (value and not value.isalpha()):
            raise ValueError("The last name must contain letters only.")
        self._last_name = value

    def __str__(self) -> str:
        """Return comma-separated person data."""
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    """Represent a student enrolled in a course; inherit the person's names."""

    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        """Initialize inherited name properties and a validated course name."""
        super().__init__(first_name, last_name)
        self._course_name = ""
        self.course_name = course_name

    @property
    def course_name(self) -> str:
        """Return the course name."""
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        """Require a string course name, allowing an empty default."""
        if not isinstance(value, str):
            raise ValueError("The course name must be text.")
        self._course_name = value

    def __str__(self) -> str:
        """Return comma-separated student details including the course."""
        return f"{super().__str__()},{self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """Provide processing-layer functions for reading and writing JSON data."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """Read JSON dictionaries and return a list of Student objects."""
        file = None
        try:
            file = open(file_name, "r", encoding="utf-8")
            json_students = json.load(file)
            if not isinstance(json_students, list):
                raise ValueError("The enrollment file must contain a list.")
            student_objects = []
            for student in json_students:
                student_objects.append(Student(student["FirstName"],
                                               student["LastName"],
                                               student["CourseName"]))
            return student_objects
        except (OSError, ValueError, TypeError, KeyError) as error:
            IO.output_error_messages("Error: There was a problem with reading the file.", error)
            return student_data
        finally:
            if file is not None and not file.closed:
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Convert Student objects into dictionaries and save JSON data."""
        file = None
        try:
            json_students = [{"FirstName": student.first_name,
                              "LastName": student.last_name,
                              "CourseName": student.course_name}
                             for student in student_data]
            file = open(file_name, "w", encoding="utf-8")
            json.dump(json_students, file, indent=2)
            print("The following data was saved to file!")
            IO.output_student_and_course_names(student_data)
        except (OSError, TypeError, ValueError, AttributeError) as error:
            IO.output_error_messages("Error: There was a problem with writing to the file.", error)
        finally:
            if file is not None and not file.closed:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """Provide presentation-layer functions for user input and output."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """Display a clear error message and optional technical details."""
        print(message)
        if error is not None:
            print(f"Technical error: {type(error).__name__}: {error}")

    @staticmethod
    def output_menu(menu: str):
        """Print the menu choices."""
        print(menu)

    @staticmethod
    def input_menu_choice():
        """Return the user's menu choice as text."""
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise ValueError("Please choose only 1, 2, 3, or 4.")
            return choice
        except ValueError as error:
            IO.output_error_messages(str(error))
            return "0"

    @staticmethod
    def output_student_courses(student_data: list):
        """Display the course registrations using Student.__str__()."""
        IO.output_student_and_course_names(student_data)

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """Print a comma-separated row for every Student object."""
        print("-" * 50)
        for student in student_data:
            print(str(student))
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """Collect valid details and append a new Student object."""
        try:
            first_name = input("Enter the student's first name: ").strip()
            if not first_name:
                raise ValueError("The first name cannot be empty.")
            if not first_name.isalpha():
                raise ValueError("The first name must contain letters only.")
            last_name = input("Enter the student's last name: ").strip()
            if not last_name:
                raise ValueError("The last name cannot be empty.")
            if not last_name.isalpha():
                raise ValueError("The last name must contain letters only.")
            course_name = input("Please enter the name of the course: ").strip()
            if not course_name:
                raise ValueError("The course name cannot be empty.")
            student = Student(first_name, last_name, course_name)
            student_data.append(student)
            print(f"You have registered {first_name} {last_name} for {course_name}.")
        except ValueError as error:
            IO.output_error_messages("Error entering student data.", error)
        return student_data


# Main body --------------------------------------- #
def main():
    """Load registrations and process menu options until the user exits."""
    students: list = []
    menu_choice: str = ""
    students = FileProcessor.read_data_from_file(FILE_NAME, students)
    while menu_choice != "4":
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
        if menu_choice == "1":
            students = IO.input_student_data(students)
        elif menu_choice == "2":
            IO.output_student_courses(students)
        elif menu_choice == "3":
            FileProcessor.write_data_to_file(FILE_NAME, students)
        elif menu_choice == "4":
            print("Program Ended")


if __name__ == "__main__":
    main()
