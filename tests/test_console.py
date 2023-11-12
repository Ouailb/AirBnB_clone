#!/usr/bin/python3
"""Defines unittests for console.py.
"""
from io import StringIO
import os
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Unittest Airbnb clone <console>"""

    def setUp(self):
        pass

    def tearDown(self) -> None:
        """Resets FileStorage data."""
        storage._FileStorage__objects = {}
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_emptyline_no_state_modification(self):
        command = HBNBCommand()
        command.emptyline()
        assert command.prompt == "(hbnb) "

    def test_emptyline_no_errors(self):
        command = HBNBCommand()
        try:
            command.emptyline()
        except Exception as e:
            self.fail(f"emptyline raised an unexpected exception: {e}")

    def test_simple(self):
        """Tests basic commands.
        """

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            self.assertEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
            self.assertEqual(f.getvalue(), "\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual(f.getvalue(), "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("?")
            self.assertIsInstance(f.getvalue(), str)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIsInstance(f.getvalue(), str)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? create")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Create a new class instance and print its id.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Create a new class instance and print its id.")

        with patch('sys.stdout', new=StringIO()) as f:
            ts = "Display string representations of all instances of a class."
            HBNBCommand().onecmd("? all")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), ts)

        with patch('sys.stdout', new=StringIO()) as f:
            ts = "Display string representations of all instances of a class."
            HBNBCommand().onecmd("help all")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), ts)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? show")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Display string representation of an instance")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Display string representation of an instance")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? update")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "update data of an instance after created")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "update data of an instance after created")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? destroy")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Delete an instance")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(), "Delete an instance")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? quit")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Quit command to exit the program.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "Quit command to exit the program.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("? help")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "To get help on a command, type help <topic>.")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help help")
            self.assertIsInstance(f.getvalue(), str)
            self.assertEqual(f.getvalue().strip(),
                             "To get help on a command, type help <topic>.")

    def test_valid_attributes_and_values(self):
        arg = "User 1234 {\"name\": \"John\", \"age\": 25}"
        cmd_obj = HBNBCommand()
        cmd_obj.do_update(arg)
        instance_objs = storage.all()
        key = "User.1234"
        _instance = instance_objs.get(key, None)
        assert _instance.name == "John"
        assert _instance.age == 25

    def test_valid_attributes_and_empty_value(self):
        arg = "User 1234 {\"name\": \"\", \"age\": }"
        cmd_obj = HBNBCommand()
        cmd_obj.do_update(arg)
        instance_objs = storage.all()
        key = "User.1234"
        _instance = instance_objs.get(key, None)
        assert _instance.name == ""
        assert _instance.age is None

    def test_valid_attributes_and_value_with_spaces(self):
        arg = "User 1234 {\"name\": \"John Doe\", \"age\": 25}"
        cmd_obj = HBNBCommand()
        cmd_obj.do_update(arg)
        instance_objs = storage.all()
        key = "User.1234"
        _instance = instance_objs.get(key, None)
        assert _instance.name == "John Doe"
        assert _instance.age == 25

    def test_invalid_class_name(self):
        arg = "InvalidClass 1234 {\"name\": \"John\", \"age\": 25}"
        cmd_obj = HBNBCommand()
        cmd_obj.do_update(arg)
        instance_objs = storage.all()
        key = "InvalidClass.1234"
        _instance = instance_objs.get(key, None)
        assert _instance is None

    def test_no_argument_passed(self):
        command = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command.do_all("")
            expected_output = ["{}".format(str(v)) for _, v in
                               storage.all().items()]
            assert fake_out.getvalue().strip() == str(expected_output)

    def test_valid_class_name_passed(self):
        command = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command.do_all("User")
            expected_output = ["{}".format(str(v))
                               for _, v in storage.all().items()
                               if type(v).__name__ == "User"]
            assert fake_out.getvalue().strip() == str(expected_output)

    def test_valid_class_name_passed_no_instances(self):
        command = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command.do_all("Review")
            expected_output = []
            assert fake_out.getvalue().strip() == str(expected_output)

    def test_invalid_argument_passed(self):
        command = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command.do_all("User InvalidArgument")
            expected_output = "** class doesn't exist **"
            assert fake_out.getvalue().strip() == expected_output

    def test_delete_instance_successfully(self):
        args = "User 1234-5678-9012"
        command = HBNBCommand()
        command.do_destroy(args)
        instance_objs = storage.all()
        key = "User.1234-5678-9012"
        assert key not in instance_objs

    def test_delete_instance_with_multiple_instances(self):
        args1 = "User 1234-5678-9012"
        args2 = "User 9876-5432-1098"
        command = HBNBCommand()
        command.do_destroy(args1)
        instance_objs = storage.all()
        key1 = "User.1234-5678-9012"
        key2 = "User.9876-5432-1098"
        assert key1 not in instance_objs
        assert key2 in instance_objs

    def test_delete_instance_with_specific_id(self):
        args1 = "User 1234-5678-9012"
        args2 = "User 9876-5432-1098"
        command = HBNBCommand()
        command.do_destroy(args1)
        instance_objs = storage.all()
        key1 = "User.1234-5678-9012"
        key2 = "User.9876-5432-1098"
        assert key1 not in instance_objs
        assert key2 in instance_objs


if __name__ == "__main__":
    unittest.main()
