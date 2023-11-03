#!/usr/bin/env python3
import cmd
import subprocess
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



if __name__ == '__main__':
    HBNBCommand().cmdloop()
