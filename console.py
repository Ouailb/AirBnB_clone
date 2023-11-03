#!/usr/bin/env python3
import cmd
import models
from models import storage
from datetime import datetime
from models.base_model import BaseModel
""""this script uses the cmd module to create a basic shell like simple shell project"""
class HBNBCommand(cmd.Cmd):
    intro = 'Muchi muchi\n'
    prompt = '(hbnb) '

    def do_quit(self, args):
        """Exit the program"""
        return True

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
            print(obj.id)
        else:
            print("** class doesn't exist **")

    
    def do_show(self, args):
        """Print the string representation of an instance based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        
        args_list = args.split()
        class_name = args_list[0]

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
     


    def do_update(self, args):
        """Update an instance based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        try:
            args_list = args.split()
            class_name = args_list[0]

            if len(args_list) > 1:
                obj_id = args_list[1]

                if len(args_list) > 2:
                    key = f"{class_name}.{obj_id}"
                    if key in storage.all():
                        obj = storage.all()[key]
                        attribute = args_list[2]

                        if len(args_list) > 3:
                            value = args_list[3]
                            try:
                                value = eval(value)
                            except (NameError, SyntaxError):
                                pass

                            setattr(obj, attribute, value)
                            obj.save()
                        else:
                            print("** value missing **")
                            return
                    else:
                        print("** no instance found **")
                        return
                else:
                    print("** attribute name missing **")
                    return
            else:
                print("** instance id missing **")
        except Exception as e:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
