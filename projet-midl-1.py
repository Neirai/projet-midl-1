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
    
    
def getVarFromForm(f: Form) -> list:
    """
    Fonction renvoyant la liste
    des variables d'une formule
    """
    L, L_right = [], []
    
    match f:
        case Var(a):
            L.append(a)
            return L
        case FF():
            return L
        case And(a,b) | Or(a,b) | Impl(a,b):
            L = getVarFromForm(a)
            L_right = getVarFromForm(b)
            for elem in L_right:
                if elem not in L:
                    L.append(elem)
        case Not(a):
            L = getVarFromForm(a)
        case f:
            raise ValueError("[NO INSPO]")
    return L
    