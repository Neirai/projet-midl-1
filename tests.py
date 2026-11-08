# Fichier entièrement généré par IA pour maximiser les tests

from projet_midl_1 import *
from datastructs import *

def run_tests():
    p = Var("p")
    q = Var("q")
    r = Var("r")

    print("\n=== Lancement des tests du prouveur ===")

    # Test 1 : Modus Ponens (p -> q, p |- q)
    s_mp = Seq([p, Impl(p, q)], q)
    res_mp = dfs(next_proof_state, sol_proof_state, [[s_mp]])
    print("Test 1 (Modus Ponens) :", res_mp == [[]])

    # Test 2 : Modus Tollens (p -> q, ¬q |- ¬p)
    s_mt = Seq([Impl(p, q), Not(q)], Not(p))
    res_mt = dfs(next_proof_state, sol_proof_state, [[s_mt]])
    print("Test 2 (Modus Tollens) :", res_mt == [[]])

    # Test 3 : Syllogisme disjonctif (p ∨ q, ¬p |- q)
    s_sd = Seq([Or(p, q), Not(p)], q)
    res_sd = dfs(next_proof_state, sol_proof_state, [[s_sd]])
    print("Test 3 (Syllogisme disjonctif) :", res_sd == [[]])

    # Test 4 : Loi du Tiers exclu ( |- p ∨ ¬p )
    s_te = Seq([], Or(p, Not(p)))
    res_te = dfs(next_proof_state, sol_proof_state, [[s_te]])
    print("Test 4 (Tiers exclu) :", res_te == [[]])

    # Test 5 : Transitivité de l'implication (p -> q, q -> r |- p -> r)
    s_trans = Seq([Impl(p, q), Impl(q, r)], Impl(p, r))
    res_trans = dfs(next_proof_state, sol_proof_state, [[s_trans]])
    print("Test 5 (Transitivité Implication) :", res_trans == [[]])

    # Test 6 : Formule invalide (p ∨ q |- p) -> Ne doit pas être prouvable
    s_inv = Seq([Or(p, q)], p)
    res_inv = dfs(next_proof_state, sol_proof_state, [[s_inv]])
    print("Test 6 (Formule invalide, échec attendu) :", res_inv == [])
    
    # Test 7 : Contradiction dans les hypothèses (p, ¬p |- q) -> Explosion
    s_explo = Seq([p, Not(p)], q)
    res_explo = dfs(next_proof_state, sol_proof_state, [[s_explo]])
    print("Test 7 (Principe d'explosion) :", res_explo == [[]])

if __name__ == "__main__":
    run_tests()
    