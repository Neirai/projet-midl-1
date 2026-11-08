from datastructs import *
from typing import TypeVar

# ========================================= #
#                                           #
#               PROJET MIDL 1               #
#       BRÉMOND Kylian & FRANÇOIS Elise     #
#                                           #
# ========================================= #

# ---------------------------------------------------------------------- #
#           4.1 : Réprésentation et manipulation de formules             #
# ---------------------------------------------------------------------- #

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
    Fonction renvoyant la liste des variables
    d'une formule (sans doublons)
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
    en forme normale négative (NNF)
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
            return And(formToNNF(Not(a)), formToNNF(Not(b)))
        case Not(Impl(a, b)):
            return And(formToNNF(a), formToNNF(Not(b)))
        case f:
            raise ValueError(f"Impossible de transformer en NNF : {f}")



# ---------------------------------------------------------------------- #
#                       4.2 : Codage de règles                           #
# ---------------------------------------------------------------------- #

# --- Fonctions utilitaires ---

def not_both_in(a: list[Form], b: list[Form], g: list[Form]) -> bool:
    """Vérifie qu'au moins l'une des deux formules n'est pas dans la liste."""
    return (a not in g) or (b not in g)

def insert_forms(lf: list[Form], f: Form) -> list[Form]:
    """Ajoute une formule dans une liste de formules si elle n'y est pas déjà présente"""
    new_list = lf.copy()
    if f not in new_list:
        new_list.append(f)
    return new_list


# --- Règle (S) ---

def s_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle (S) s'applique (la conclusion n'est pas déjà ⊥)"""
    match (fs, s) :
        case ([], Seq(_, a)):
            return a != FF()
        case _:
            return False

def s_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle (S) : déplace la conclusion dans les antécédents avec une négation."""
    match (fs, s):
        case ([], Seq(g, a)):
            return [Seq(insert_forms(g, Not(a)), FF())]
        case _:
            return []

s_t_rule = Rule("s_t", s_t_appcond , s_t_action )


# --- Axiome F ---

def axf_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si l'axiome F s'applique (présence de ⊥ dans les antécédents)."""
    match (fs, s):
        case ([], Seq(g, FF())):
            return FF() in g
        case _:
            return False

def axf_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique l'axiome F : ferme la branche de la preuve en renvoyant une liste vide."""
    match (fs, s):
        case ([], Seq(g, FF())):
            return []
        case _:
            return []

axf_t_rule = Rule("axf_t", axf_t_appcond, axf_t_action)
    
    
# --- Axiome C ---

def axc_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si l'axiome C s'applique (présence de A et ¬A dans les antécédents)."""
    match (fs, s):
        case ([a], Seq(g, FF())):
            return Not(a) in g
        case _:
            return False
        
def axc_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique l'Axiome C : ferme la branche de la preuve."""
    match (fs, s):
        case ([a], Seq(g, FF())):
            return []
        case _:
            return []
        
axc_t_rule = Rule("axc_t", axc_t_appcond, axc_t_action)


# --- Négation ---

def n_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle de double négation s'applique (¬¬A dans les antécédents)."""
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return a not in g
        case _: 
            return False
        
def n_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle de double négation : ajoute A aux antécédents."""
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return [Seq(insert_forms(g, a), FF())]
        case _:
            return []
        
n_t_rule = Rule("n_t", n_t_appcond, n_t_action)


# --- Alpha AND --- 
    
def a_and_t_appcond (fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Alpha AND s'applique (a ∧ b dans les antécédents)"""
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return (not_both_in (a, b, g))
        case _:
            return (False)
        
def a_and_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Alpha AND : ajoute a et b aux antécédents"""
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return [Seq(insert_forms(insert_forms(g, a), b), FF())]
        case _:
            return []
    
a_and_t_rule = Rule("a_and_t", a_and_t_appcond, a_and_t_action)


# --- Beta AND ---

def b_and_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Beta AND s'applique (¬(a ∧ b) dans les antécédents)"""
    match (fs, s):
        case ([Not(And(a, b))], Seq(g, FF())):
            return Not(a) not in g and Not(b) not in g
        case _:
            return False

def b_and_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Beta AND : sépare la preuve en deux séquents (un avec ¬a, l'autre avec ¬b)"""
    match (fs, s):
        case ([Not(And(a, b))], Seq(g, FF())):
            return [Seq(insert_forms(g, Not(a)), FF()), Seq(insert_forms(g, Not(b)), FF())]
        case _:
            return []

b_and_t_rule = Rule("b_and_t", b_and_t_appcond, b_and_t_action)


# --- Alpha OR ---

def a_or_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Alpha OR s'applique (¬(a ∧ b) dans les antécédents)"""
    match (fs, s):
        case ([Not(Or(a, b))], Seq(g, FF())):
            return not_both_in(Not(a), Not(b), g)
        case _:
            return False

def a_or_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Alpha OR : ajoute ¬a et ¬b aux antécédents"""
    match(fs, s):
        case ([Not(Or(a, b))], Seq(g, FF())):
            return [Seq(insert_forms(insert_forms(g, Not(a)), Not(b)), FF())]
        case _:
            return []

a_or_t_rule = Rule("aor_t", a_or_t_appcond, a_or_t_action)


# --- Beta OR ---

def b_or_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Beta OR s'applique : (a ∨ b dans les antécédents)"""
    match (fs, s):
        case ([Or(a, b)], Seq(g,  FF())):
            return a not in g and b not in g
        case _:
            return False

def b_or_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Beta OR : sépare la preuve en deux séquents (un avec a, l'autre avec b)"""
    match (fs, s):
        case ([Or(a, b)], Seq(g,  FF())):
            return [Seq(insert_forms(g, a), FF()), Seq(insert_forms(g, b), FF())]
        case _:
            return []

b_or_t_rule = Rule("bor_t", b_or_t_appcond, b_or_t_action)


# --- Alpha Impl ---

def a_impl_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Alpha Impl s'applique (¬(a -> b) dans les antécédents)"""
    match (fs, s):
        case ([Not(Impl(a, b))], Seq(g, FF())):
            return not_both_in(a, Not(b), g)
        case _:
            return False

def a_impl_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Alpha Impl : ajoute a et ¬b dans les antécédents"""
    match (fs, s):
        case ([Not(Impl(a, b))], Seq(g, FF())):
            return [Seq(insert_forms(insert_forms(g, a), Not(b)), FF())]
        case _:
            return []

a_impl_t_rule = Rule("a_impl_t", a_impl_t_appcond, a_impl_t_action)


# --- Beta Impl ---

def b_impl_t_appcond(fs: list[Form], s: Seq) -> bool:
    """Vérifie si la règle Beta Impl s'applique (a -> b dans les antécédents)"""
    match(fs, s):
        case ([Impl(a, b)], Seq(g, FF())):
            return Not(a) not in g and b not in g
        case _:
            return False

def b_impl_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    """Applique la règle Beta Impl : sépare la preuve en deux séquents (un avec ¬a, l'autre avec b)"""
    match (fs, s):
        case ([Impl(a, b)], Seq(g, FF())):
            return [Seq(insert_forms(g, Not(a)), FF()), Seq(insert_forms(g, b), FF())]
        case _:
            return []
        
b_impl_t_rule = Rule("b_impl_t", b_impl_t_appcond, b_impl_t_action)



# ---------------------------------------------------------------------- #
#                       4.3 : Application de règles                      #
# ---------------------------------------------------------------------- #

# Liste de toutes les règles 
rules = [
    s_t_rule, axf_t_rule, axc_t_rule, n_t_rule, 
    a_and_t_rule, b_and_t_rule, a_or_t_rule, b_or_t_rule, 
    a_impl_t_rule, b_impl_t_rule
]

def next_proof_state(ps: ProofStateV0) -> list[ProofStateV0]:
    """
    Génère les possibilités de preuve du premier séquent
    d'une liste à partir de l'état courant. 
    """
    
    # sécurité si la liste donnée est vide
    if ps == []:
        return ps
    
    seq = ps[0]
    nextProofState = []
    
    # règles ne prenant pas d'hypothèses en paramètres ((S), (AxF))
    for rule in rules[:2]:
        if rule.appcond([], seq):
            ProofStateV1 = rule.action([], seq) + ps[1:]
            nextProofState.append(ProofStateV1)
   
   # autres règles
    for hyp in seq.hyps:
        for rule in rules[2:]:
            if rule.appcond([hyp], seq):
                ProofStateV1 = rule.action([hyp], seq) + ps[1:]
                nextProofState.append(ProofStateV1)
                                
    return nextProofState

# ---------------------------------------------------------------------- #
#                       4.4 : Recherche de preuves                       #
# ---------------------------------------------------------------------- #

PS = TypeVar("PS")

def dfs (nexts: Callable [[PS], list[PS]],
        sol: Callable [[PS], bool],
        states: list[PS]) -> list[PS]:
        
        if states == []:
            return ([])
        else:
            if sol(states [0]):
                return [states [0]]
            # si vous souhaitez continuer la recherche , decommentez :
            # return [states [0]] + dfs(nexts , sol , nexts(states [0]) + states [1:])
            else:
                return dfs(nexts , sol , nexts(states [0]) + states [1:])


def sol_proof_state(ps: ProofStateV0) -> bool:
    """
    verifie que toutes les preuves globales du sequent de depart ont ete prouvées
    """
    return ps == []
            