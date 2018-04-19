# External
import shlex  # lexical analysis for splitting command like shell
import subprocess  # module for running sub processes from python


class Process:

    def __init__(self):
        pass

    @staticmethod
    def execute(command):
        process = subprocess.Popen(shlex.split(command),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()
        if process.returncode:
            raise ProcessException(process.returncode)
        return out


class ProcessException(Exception):

    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
