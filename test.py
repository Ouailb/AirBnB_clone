import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand  # Replace 'your_module' with the actual module containing HBNBCommand

class TestHBNBCommand(unittest.TestCase):
    # def test_valid_class_and_method(self):
    #     line = "User.all()"
    #     expected_output = "[<models.user.User object at 0x7f8e3c6a5a90>]"
    #     with patch('sys.stdout', new=StringIO()) as fake_out:
    #         HBNBCommand().default(line)
    #         self.assertEqual(fake_out.getvalue().strip(), expected_output)

    def test_valid_class_invalid_method(self):
        line = "User.invalid_method()"
        expected_output = "** Method 'invalid_method' doesn't exist in class 'User' **"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            HBNBCommand().default(line)
            self.assertEqual(fake_out.getvalue().strip(), expected_output)

if __name__ == '__main__':
    unittest.main()
