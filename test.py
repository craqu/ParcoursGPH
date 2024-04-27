import unittest
from ParcourGPH import Bacc, into_course

class TestBacc(unittest.TestCase):
    def setUp(self):
        # Initialize test data
        self.bacc_instance = Bacc([[], [], [], [], [], [], [], []])
        self.course1 = ("CoursA", 1)  # Example course tuple
        self.course2 = ("CoursB", 1)  # Another example course tuple

    def test_add_course(self):
        # Test adding a course
        self.bacc_instance.add_course(self.course1)
        self.assertEqual(len(self.bacc_instance.bacc[0]), 1)  # Assuming you added to session 1
        # Add more assertions if needed

    def test_look_for_conflict(self):
        # Test looking for conflicts
        # Add test data representing conflicting and non-conflicting courses
        # Call the look_for_conflict method
        # Assert the expected behavior
        # Example:
        # self.bacc_instance.add_course(self.course1)
        # self.bacc_instance.add_course(self.course2)
        # self.bacc_instance.look_for_conflict()
        # Add assertions as needed

    def test_show_credit(self):
        # Test showing credit
        # Add test data representing different credit scenarios
        # Call the show_credit method
        # Assert the expected output
        # Example:
        # self.bacc_instance.add_course(self.course1)
        # self.bacc_instance.show_credit()
        # Add assertions as needed

class TestIntoCourse(unittest.TestCase):
    def test_into_course(self):
        # Test the into_course function
        # Add test data representing different input types
        # Call the into_course function
        # Assert the expected output
        # Example:
        # result = into_course("IFT-4030")
        # self.assertIsInstance(result, Scrapper)  # Assuming Scrapper is the expected return type
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()

