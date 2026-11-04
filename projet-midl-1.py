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
    match f:
        case Var(_) | FF():
            return 1
        case Impl(a, b) | And(a, b) | Or(a, b):
            return compterFeuilleForm(a) + compterFeuilleForm(b)
        case Not(a):
            return compterFeuilleForm(a)
        case f:
            raise ValueError(f"Formule non reconnue : {f}")
    
    
def getVarFromForm(f: Form) -> list:
    """
    Fonction renvoyant la liste
    des variables d'une formule
    """
    match f:
        case Var(a):
            return [a]
        case FF():
            return []
        case And(a, b) | Or(a, b) | Impl(a, b):
            return list(set(getVarFromForm(a) + getVarFromForm(b)))
        case Not(a):
            return list(set(getVarFromForm(a)))
        case f:
            raise ValueError(f"Formule non reconnue : {f}")

def formToNNF(f: Form) -> Form:
    """
    Fonction mettant une formule
    en forme normale négative
    """
    match f:
        case Var(_) | FF() | Not(Var(_)) | Not(FF()):
            return f
        case And(a, b):
            return And(formToNNF(a), formToNNF(b))
        case Or(a, b):
            return Or(formToNNF(a), formToNNF(b))
        case Impl(a, b):
            return Or(formToNNF(Not(a)), formToNNF(b))
        case Not(Not(a)):
            return formToNNF(a)
        case Not(And(a, b)):
            return Or(formToNNF(Not(a)), formToNNF(Not(b)))
        case Not(Or(a, b)):
            return And(formToNNF(Not(a)), formToNNF(Not(f)))
        case Not(Impl(a, b)):
            return And(formToNNF(a), formToNNF(Not(b)))
        case f:
            raise ValueError(f"Impossible de transformer en NNF : {f}")
