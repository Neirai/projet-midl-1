from datastructs import *

#######################
#       KYLIAN        #
#######################


f = Impl(Impl(Var("a"), Var("c")), Impl(Var("a"), Var("b")))
print(f.left.right)

g = Not(Var("n"))
match g:
    case Not(a):
        print(a)
    case g:
        print("x")



def compterFeuilleForm(f: Form) -> int:
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
            raise ValueError("Error")
        
print(f)
print(compterFeuilleForm(f))
print(g)
print(compterFeuilleForm(g))


def test(f: Form):
    
    L, L_right = [], []
    
    match f:
        case Var(a):
            L.append(a)
            return L
        case FF():
            return L
        case And(a,b) | Or(a,b) | Impl(a,b):
            L = test(a)
            L_right = test(b)
            for elem in L_right:
                if elem not in L:
                    L.append(elem)
        case Not(a):
            L = test(a)
        case f:
            raise ValueError("[NO INSPO]")
    return L
        
print(test(f))
print(test(g))

#######################
#       ELISE         #
#######################