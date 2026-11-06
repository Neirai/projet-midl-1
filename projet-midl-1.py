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
    
    
def getVarFromForm(f: Form) -> list[str]:
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




#Start

def insert_forms(lf: list[Form], f: list[Form]) -> list[Form]:
    return list(set(lf + f))

def s_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s) :
        case ([], Seq(_, a)):
            return a != FF()
        case _:
            return False

def s_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([], Seq(g, a)):
            return [Seq(insert_forms(g, [Not(a)]), FF())]
        case _:
            return []

s_t_rule = Rule("s_t", s_t_appcond , s_t_action )

s1 = Seq([Var("p")], Var("q"))
print("Applicable ?", s_t_appcond([], s1))
res = s_t_action([], s1)
print("Resultat : ", end="")
for s in res:
    print(s)
    
    
#Aand

def not_both_in(a: list[Form], b: list[Form], g: list[Form]) -> bool:
<<<<<<< HEAD
    return (a not in g) or (b not in g)
=======
    return (a not in g) and (b not in g)
>>>>>>> e956e06f9da42ef8d3fcd02e5d89a207b045150f
    
    
def a_and_t_appcond (fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return (not_both_in (a, b, g))
        case _:
            return (False)
        
def a_and_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return [Seq(insert_forms(g, [a, b]), FF())]
        case _:
            return []
    
a_and_t_rule = Rule("a_and_t", a_and_t_appcond, a_and_t_action)
    
    
#Axiome C

def axc_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([a], Seq(g, FF())):
            return Not(a) in g
        case _:
            return False
        
def axc_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([a], Seq(g, FF())):
            return []
        case _:
            return []
        
axc_t_rule = Rule("axc_t", axc_t_appcond, axc_t_action)


#Negation

def n_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return a not in g
        case _:
            return False
        
def n_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return [Seq(insert_forms(g, a), FF())]
        case _:
            return []
        
<<<<<<< HEAD
n_t_rule = Rule("n_t", n_t_appcond, n_t_action)



# Partie 4.3.1

def is_applicable(fs: list[Form], s: Seq) -> bool:
    s_t = s_t_appcond(fs, s)
    a_and_t = a_and_t_appcond(fs, s)
    axc_t = axc_t_appcond(fs, s)
    n_t = n_t_appcond(fs, s)

    L = [s_t, a_and_t, axc_t, n_t]
    return L


def next_proof_state(ls: list[Seq]) -> list[list[Seq]]:
    L = []
    for fs in ls:
        lbool = is_applicable
=======
n_t_rule = Rule("n_t", n_t_appcond, n_t_action)
>>>>>>> e956e06f9da42ef8d3fcd02e5d89a207b045150f
