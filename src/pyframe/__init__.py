__version__ = "0.0.6"
try :
    import pyframe.constants as constants
    import pyframe.functions as functions
    import pyframe.classes as classes
    import pyframe.exception as exception
except Exception as e :
    print("PYFRAME ERROR: Impossible d'importer correctement la librairie")
    print("(",end="")
    print(e,end="")
    print(")")