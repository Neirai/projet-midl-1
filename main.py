from datastructs import *
from projet_midl_1 import *
from tests import *

def main():
    print("==========================================")
    print("             Projet MIDL 1")
    print("      BRÉMOND Kylian & FRANÇOIS Elise")
    print("==========================================")

    while True:    
        print("\n1 - Exécuter la démo")
        print("2 - Exéctuer le fichier de tests")
        print("3 - Quitter\n")

        match input("Votre choix : "):
            case "1":
                print("Séquent issu du cours de Philosophie des Sciences")
                print("Hypothèses : n -> f, v -> f, n ∨ v, e -> ¬f")
                print("Conclusion : ¬e\n")
                
                n = Var("n")
                f = Var("f")
                v = Var("v")
                e = Var("e")
                
                sequent_demo = Seq([Impl(n,f),Impl(v,f),Or(n,v),Impl(e,Not(f))], Not(e))
                print("Recherche de preuve en cours...")
                
                etat_initial = [[sequent_demo]]
                resultat = dfs(next_proof_state, sol_proof_state, etat_initial)
                
                if resultat == [[]]:
                    print("Résultat : Le séquent est PROUVABLE.")
                else:
                    print("Résultat : Le séquent N'EST PAS prouvable.")
            
            case "2":
                run_tests()
                
            case "3":
                return

            case _:
                print("Choix invalide. Veuillez choisir un nombre parmi : 1, 2 ou 3.")

if __name__ == "__main__":
    main()