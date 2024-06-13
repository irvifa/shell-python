import os
import subprocess
import sys

class Command:
    def execute(self, args):
        pass

class EchoCommand(Command):
    def execute(self, args):
        if args and args[0] == '-n':
            print(' '.join(args[1:]), end='')
        else:
            print(' '.join(args))

class ExitCommand(Command):
    def execute(self, args):
        status = int(args[0]) if args else 0
        sys.exit(status)

class CdCommand(Command):
    def execute(self, args):
        if len(args) != 1:
            print("cd: invalid number of arguments")
            return
        path = os.path.expanduser(args[0])
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")

class PwdCommand(Command):
    def execute(self, args):
        if args:
            print("pwd: too many arguments")
            return
        print(os.getcwd())

class TypeCommand(Command):
    def __init__(self, shell):
        self.shell = shell

    def execute(self, args):
        if len(args) != 1:
            print("type: invalid number of arguments")
            return

        cmd_name = args[0]

        if cmd_name in self.shell.builtins:
            print(f"{cmd_name} is a shell builtin")
        else:
            result = subprocess.run(['which', cmd_name], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{cmd_name} is {result.stdout.strip()}")
            else:
                print(f"{cmd_name}: not found")
