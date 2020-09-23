import pyframe.base
import pyframe.utils


# Handling exceptions
class Error(Exception):  # La classe d'erreur de base
    pass


class WindowError(Error):  # Erreur de fenêtre
    def __init__(self, message):
        self.message = message


class ArgumentError(Error):  # Erreur d'argument
    def __init__(self, message, subject):
        self.message = message
        self.subject = subject
