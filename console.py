#!/usr/bin/python3
import re
import cmd
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place

classes = {
    'BaseModel': BaseModel, 
    'User': User,
    'Amenity': Amenity, 
    'City': City, 
    'State': State,
    'Place': Place,
    'Review': Review
        }

def IsValidClass(args, _id=False):
    """Runs checks on args to validate classname entry.
    """

    if len(args) < 1:
        print("** class name missing **")
        return False
    if args[0] not in classes.keys():
        print("** class doesn't exist **")
        return False
    if len(args) < 2 and _id:
        print("** instance id missing **")
        return False
    return True



def IsValid_attr(args):
    """Runs checks on args to validate classname attributes and values.
    """
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True


def is_float(x):
    """Checks if `x` is float.
    """
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(x):
    """Checks if `x` is int.
    """
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def parse_str(arg):
    """Parse `arg` to an `int`, `float` or `string`.
    """
    parsed = re.sub("\"", "", arg)

    if is_int(parsed):
        return int(parsed)
    elif is_float(parsed):
        return float(parsed)
    else:
        return arg

class HBNBCommand(cmd.Cmd):
    """console"""       

    prompt = "(hbnb) "



    def precmd(self, line):
        """Defines instructions to execute before <line> is interpreted.
        """
        if not line:
            return '\n'

        pattern = re.compile(r"(\w+)\.(\w+)\((.*)\)")
        match_list = pattern.findall(line)
        # print(match_list)
        if not match_list:
            return super().precmd(line)

        match = match_list[0]
        # print(match)
        if not match[2]:
            if match[1] == "count":
                instance_objs = storage.all()
                print(len([
                    counter for _, counter in instance_objs.items()
                    if type(counter).__name__ == match[0]]))
                return "\n"
            return f"{match[1]} {match[0]}"
        else:
            args = match[2].split(", ")
            # print(args)
            if len(args) == 1:
                return "{} {} {}".format(
                    match[1], match[0],
                    re.sub("[\"\']", "", match[2]))
            else:
                match_dict = re.findall(r"{.*}", match[2])
                if (match_dict):
                    return "{} {} {} {}".format(
                        match[1], match[0],
                        re.sub("[\"\']", "", args[0]),
                        re.sub("\'", "\"", match_dict[0]))
                return "{} {} {} {} {}".format(
                    match[1], match[0],
                    re.sub("[\"\']", "", args[0]),
                    re.sub("[\"\']", "", args[1]), args[2])


    
    def do_create(self, arg):
        """create a new instance.
        """
        args = arg.split()
        if not IsValidClass(args):
            return

        new_obj = classes[args[0]]()
        new_obj.save()
        print(new_obj.id)

 

    def do_show(self, arg):
        """Prints the string representation of an instance.
        """
        args = arg.split()
        if not IsValidClass(args, _id=True):
            return

        instance_objs = storage.all()
        key = f"{args[0]}.{args[1]}" # args[0] => class.id
        # print(key)
        _instance = instance_objs.get(key, None)
        if _instance is None:
            print("** no instance found **")
            return
        print(_instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.
        """
        args = arg.split()
        if not IsValidClass(args, _id=True):
            return

        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        # print(key)
        _instance = objs.get(key, None)
        if _instance is None:
            print("** no instance found **")
            return

        del objs[key]
        storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances.
        """
        args = arg.split()
        all_objs = storage.all()

        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in all_objs.items()])
            return
        if args[0] not in classes.keys():
            print("** class doesn't exist **")
            return
        else:
            print(["{}".format(str(v))
                  for _, v in all_objs.items() if type(v).__name__ == args[0]])
            return

    def do_update(self, arg: str):
        """Updates an instance based on the class name and id.
        """
        args = arg.split(maxsplit=3)
        if not IsValidClass(args, _id=True):
            return

        instance_objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        _instance = instance_objs.get(key, None)
        if _instance is None:
            print("** no instance found **")
            return

        match_dict = re.findall(r"{.*}", arg)
        if match_dict:
            payload = None
            try:
                payload: dict = json.loads(match_dict[0])
            except Exception:
                print("** invalid syntax")
                return
            for k, v in payload.items():
                setattr(_instance, k, v)
            storage.save()
            return
        if not IsValid_attr(args):
            return
        first_attr = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if first_attr:
            setattr(_instance, args[2], first_attr[0])
        else:
            value_list = args[3].split()
            setattr(_instance, args[2], parse_str(value_list[0]))
        storage.save()





    def do_help(self, arg):
        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)

    def do_EOF(self, line):
        """manage EOF (ctr+d).
        """
        print("")
        return True

    def do_quit(self, arg):
        """exit the console.
        """
        return True

    def emptyline(self):
        """
        delete the history of last command
        """
        pass













    
if __name__ == "__main__":
    HBNBCommand().cmdloop()