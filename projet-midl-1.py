from datastructs import *

######################################
#                                    #
#           Projet MIDL 1            #
#   BRÉMOND Kylian & FRANÇOIS Elise  #
#                                    #
######################################

def compterFeuilleForm(f: Form) -> int:
    """
    Fonction comptant le nombre de variables
    et constantes ("feuilles") d'une formule
    """
    nb = 0
    match f:
        case Var(a):
            return nb + 1
        case FF():
            return nb + 1
        case Impl(a,b):
            return compterFeuilleForm(a) + compterFeuilleForm(b)
        case And(a,b):
            return compterFeuilleForm(a) + compterFeuilleForm(b)
        case Or(a,b):
            return compterFeuilleForm(a) + compterFeuilleForm(b)
        case Not(a):
            return compterFeuilleForm(a)
        case f:
            raise ValueError("[NO IDEA YET]")
        
    