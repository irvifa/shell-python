import os
import sys
import subprocess
from .commands import EchoCommand, ExitCommand, CdCommand, PwdCommand, TypeCommand

class Shell:
    def __init__(self):
        self.builtins = {
            'exit': ExitCommand(),
            'echo': EchoCommand(),
            'cd': CdCommand(),
            'pwd': PwdCommand(),
            'type': TypeCommand(self)
        }

    def run(self):
        while True:
            try:
                command = input("$ ").strip()
                if not command:
                    continue
                self.execute(command)
            except EOFError:
                break

    def execute(self, command):
        parts = command.split()
        cmd_name = parts[0]
        args = parts[1:]

        if cmd_name in self.builtins:
            self.builtins[cmd_name].execute(args)
        else:
            self.run_external_command(cmd_name, args)

    def run_external_command(self, cmd_name, args):
        try:
            subprocess.run([cmd_name] + args)
        except FileNotFoundError:
            print(f"{cmd_name}: command not found")

if __name__ == "__main__":
    shell = Shell()
    shell.run()
