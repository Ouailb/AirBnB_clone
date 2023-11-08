#!/usr/bin/env python3
import cmd
import models
import re
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

""""this script uses the cmd module to create a basic shell like simple shell project"""
class HBNBCommand(cmd.Cmd):
    intro = 'Muchi muchi\n'
    prompt = '(hbnb) '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_mapping = {
            'all': self.do_all,
            'create': self.do_create,
            'show': self.do_show,
            'count':self.do_count,
            'destroy': self.do_destroy,
            'update': self.do_update,
        }



    def default(self, args):
        if args:
            splitter = re.split(r"\.", args)
            if len(splitter) == 2:
                class_name, part2 = splitter
                # print("class:", class_name)
            
                command = part2.split("(")[0]
                # print(command)
                # Extract text between parentheses and remove quotes
                match = re.search(r'\((["\'])(.*?)\1\)', part2)
                if match:
                    id = match.group(2)
                    # id = str(id)
                    # print("id :", id)

                    if command in self.command_mapping:
                        self.command_mapping[command](f"{class_name} {id}")
                        # print(result)
                    else:
                        print(f"** Method '{command}' doesn't exist in class '{class_name}' **")
                else:
                    class_obj = self.command_mapping.get(command)
                    if class_obj and callable(class_obj):
                        result = class_obj(class_name)
                        if result is not None:
                            print(result)
            else:
                print("Invalid format. There should be exactly one dot in the input string.")
        else:
            print("Nothing")



    # def default(self, args):
    #     if args:
    #         splitter = re.split(r"\.", args)
    #         if len(splitter) == 2:
    #             class_name, part2 = splitter
    #             command = part2.split("(")[0]
    #             match = re.search(r'\((.*?)\)', part2)

    #             if match:
    #                 id = match.group(1)
    #                 if "{" in id and "}" in id:
    #                     id = id.replace("'", '"')
    #                     self.command_mapping[command](f"{class_name} {id}")
    #                 else:
    #                     if "}" in args:
    #                         # Handle the case where arguments are a dictionary representation
    #                         self.command_mapping[command](f"{class_name} {id}", args)
    #                     else:
    #                         # Handle the old format with separate attributes and values
    #                         self.command_mapping[command](f"{class_name} {id}", args)
    #             else:
    #                 class_obj = self.command_mapping.get(command)
    #                 if class_obj and callable(class_obj):
    #                     result = class_obj(class_name)
    #                     if result is not None:
    #                         print(result)
    #         else:
    #             print("Invalid format. There should be exactly one dot in the input string.")
    #     else:
    #         print("Nothing")







    # def default(self, args):
    #     if args:
    #         splitter = re.split(r"\.", args)
    #         if len(splitter) == 2:
    #             part1, part2 = splitter
    #             print("class:", part1)
    #             print("Second Part:", part2)
    #             print("command",part2.split("(")[0])
    #             # Extract text between parentheses and remove quotes
    #             match = re.search(r'\((["\'])(.*?)\1\)', part2)
    #             if match:
    #                 id = match.group(2)
    #                 print("Text between parentheses:",id)

    #             else:
    #                 print("No text between parentheses found.")
    #         else:
    #             print("Invalid format. There should be exactly one dot in the input string.")
    #     else:
    #         print("Nothing")


    def do_quit(self, args):
        """Exit the program"""
        return True

    def emptyline(self):
        """last cmd"""
        pass
    
    def do_EOF(self, args):
        """Exit the program when EOF (Ctrl+D) is entered"""
        return True

    def do_help(self, arg):
        """Show help message for a specific command or list available commands"""
        super().do_help(arg)
    
   




    def do_create(self, args):
        """Create a new instance of BaseModel, save it, and print its id"""
        if not args:
            print("** class name missing **")
            return
        
        class_name = args.split()[0]
        if class_name in globals():
            obj_class = globals()[class_name]
            obj = obj_class()
            obj.save()
            # print(globals())
            print(obj.id)
        else:
            print("** class doesn't exist **")

    def do_count(self, args):
        """Count the number of instances of a class"""
        if not args:
            print("** class name missing **")
            return

        class_name = args
        if class_name in models.__all__:
            count = storage.count(class_name)
            print(count)
        else:
            print("** class doesn't exist **")

            






    def do_show(self, args):
        """Print the string representation of a City instance."""
        if not args:
            print("** class name missing **")
            return

        args_list = args.split()
        class_name = args_list[0]
        # print(args_list)
        # print(class_name)

        if len(args_list) > 1:
            obj_id = args_list[1]
            key = f"{class_name}.{obj_id}"

            if key in storage.all():
                print(storage.all()[key])
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")














            

    def do_destroy(self, args):
        """Delete an instance based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        
        args_list = args.split()
        class_name = args_list[0]

        if len(args_list) > 1:
            obj_id = args_list[1]
            key = f"{class_name}.{obj_id}"

            if key in storage.all():
                del storage.all()[key]
                storage.save()
            else:
                print("** no instance found **")
        else:
            print("** instance id missing **")

    def do_all(self, args):
        """Print string representations of all instances, or all instances of a specific class"""
        
        args_list = args.split()
        if len(args_list) > 0:
            class_name = args_list[0]

            if class_name in models.__all__:
                objs = [str(obj) for key, obj in storage.all().items() if key.split(".")[0] == class_name]
            else:
                print("** class doesn't exist **")
                return
        else:
            objs = [str(obj) for obj in storage.all().values()]

        print(objs)
     


    # def do_update(self, args):
    #     """Update an instance based on class name and id"""
    #     if not args:
    #         print("** class name missing **")
    #         return
    #     print(args)
    #     args = args.replace('"','')
    #     args = args.replace(',','')
    #     print(args)

    #     splitter = re.split(r" ", args)

    #     class_name = splitter[0]
    #     if not class_name:
    #         print("** class doesn't exist **")
    #         return
    #     print(class_name)

    #     arg = splitter[1:]
    #     print(arg)
    #     if len(arg) > 1:
    #         obj_id = arg[0]
    #         print(obj_id)
            
    #         if len(arg) > 2:
    #             key = f"{class_name}.{obj_id}"
    #             print(key)
    #             if key in storage.all():
    #                 obj = storage.all()[key]
    #                 print(arg[0])
    #                 attribute = arg[1]
    #                 print(attribute)
    #                 print(arg[2])
    #                 print(len(arg))

    #                 if len(arg) >= 3:
    #                     value = arg[2]
    #                     print(value)
    #                     try:
    #                         value = eval(value)
    #                     except (NameError, SyntaxError):
    #                         pass
    #                     print("attribute", attribute)
    #                     print("obj", obj)
    #                     print("value",value)
    #                     setattr(obj, attribute, value)
    #                     obj.save()
    #                 else:
    #                     print("** value missing **")
    #                     return
    #             else:
    #                 print("** no instance found **")
    #         else:
    #             print("** attribute name missing **")
    #             return
    #     else:
    #         print("** instance id missing **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()