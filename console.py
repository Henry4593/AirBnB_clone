#!/usr/bin/python3
'''**hbnb command line interpreter**
This module defines the `HBNBCommand` class, which implements
an interactive shell for managing instances of various models
in the application. The shell allows users to create,
read, update, and delete instances using intuitive commands.
'''
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parser(line):
    """Parses a line of text based on curly braces and square brackets.

    Args:
      text_line (str): The line of text to be parsed retrieved from user input

    Returns:
      list: A list containing parsed elements from the line.
    """
    curly_braces = re.search(r"\{(.*?)\}", line)
    brackets = re.search(r"\[(.*?)\]", line)
    if curly_braces is None:
        if brackets is None:
            return [element.strip(",") for element in split(line)]
        else:
            lexer = split(line[:brackets.span()[0]])
            retl = [element.strip(",") for element in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(line[:curly_braces.span()[0]])
        retl = [element.strip(",") for element in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    '''**HBNBCommand class**
    Inherits from `cmd.Cmd` to provide an interactive shell for
    managing instances of models in the application. Supports commands
    for creating, reading, updating, and deleting instances.

    Attributes:
        prompt (str): Command prompt displayed to the user.

    '''

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Ignores empty lines."""
        pass

    def default(self, line):
        """Method to take care of following commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        <class name>.update(<id>, <dictionary representation)

        Description:
            Creates a list representations of functional models
            Then use the functional methods to implement user
            commands, by validating all the input commands
        """
        args_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match is not None:
            arg_line = [line[:match.span()[0]], line[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_line[1])
            if match is not None:
                command = [arg_line[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in args_dict.keys():
                    call = "{} {}".format(arg_line[0], command[1])
                    return args_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Quits command interpreter with keyboard stroke `ctrl+d`
            or EOF signal
         Args:
            line(args): user input from the terminal
        """
        print("")
        return True

    def do_create(self, line):
        """Creates a new instance of a class and prints its ID.
            "usage: <command name> <class name>"
            "EX. create User"
        Args:
            line (str): User input containing the class name.
        Returns:
            None
        """
        arg_line = parser(line)
        if len(arg_line) == 0:
            print("** class name missing **")
        elif arg_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_line[0])().id)
            storage.save()

    def do_show(self, line):
        """Prints the string representation of an instance.
            "example. show User 1234-1234-1234"
        Args:
            line (str): User input containing class and ID.

        Returns:
            None
        """
        arg_line = parser(line)
        obj_dict = storage.all()
        if len(arg_line) == 0:
            print("** class name missing **")
        elif arg_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_line) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_line[0], arg_line[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_line[0], arg_line[1])])

    def do_destroy(self, line):
        """Deletes an instance of a certain class.

        Args:
            line(args): to enter with command: <class name> <id>
            Example: 'destroy User 1234-1234-1234'

        """
        arg_line = parser(line)
        obj_dict = storage.all()
        if len(arg_line) == 0:
            print("** class name missing **")
        elif arg_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_line) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_line[0], arg_line[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_line[0], arg_line[1])]
            storage.save()

    def do_all(self, line):
        """Shows all instances, or instances of a certain class

        Args:
            line(args): enter with command (optional): <class name>
            Example: 'all' OR 'all User'

        """
        arg_line = parser(line)
        if len(arg_line) > 0 and arg_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(arg_line) > 0 and arg_line[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(arg_line) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_count(self, line):
        """This function counts the number of instances of a specific class
        within a data storage.

        Args:
          self (Any): The object reference on which the method is called
          cls_name (str): The name of the class to be counted (as a string).

        Returns:
          int: The number of instances of the specified class found in the
            storage.
        """
        arg_line = parser(line)
        count = 0
        for obj in storage.all().values():
            if arg_line[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating an attribute

        Args:
            line(args): receives the commands:
            <class name> <id> <attribute name> "<attribute value>"
            Example: 'update User 1234-1234-1234 my_name "Bob"'

        """
        arg_line = parser(line)
        obj_dict = storage.all()

        if len(arg_line) == 0:
            print("** class name missing **")
            return False
        if arg_line[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_line) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_line[0], arg_line[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_line) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_line) == 3:
            try:
                type(eval(arg_line[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arg_line) == 4:
            obj = obj_dict["{}.{}".format(arg_line[0], arg_line[1])]
            if arg_line[2] in obj.__class__.__dict__.keys():
                val_type = type(obj.__class__.__dict__[arg_line[2]])
                obj.__dict__[arg_line[2]] = val_type(arg_line[3])
            else:
                obj.__dict__[arg_line[2]] = arg_line[3]
        elif type(eval(arg_line[2])) == dict:
            obj = obj_dict["{}.{}".format(arg_line[0], arg_line[1])]
            for key, value in eval(arg_line[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[key])
                        in {str, int, float}):
                    val_type = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = val_type(value)
                else:
                    obj.__dict__[key] = value
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
