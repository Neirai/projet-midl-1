from datastructs import *

#######################
#       KYLIAN        #
#######################


f = Impl(Impl(Var("a"), FF()), Impl(Not(Var("b")),FF()))
print(f.left.right)

def peutbaisersitas17ans(age: int) -> str:
    match age:
        case 15 | 16 | 17 | 18:
            return "OK."
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14:
            return "Trop jeune. Oulala !"
        case 19:
            return "Vraiment la limite hein !!"
        case _:
            return "Trop vieux. #michto"

for i in range(1,25):
    print(peutbaisersitas17ans(i))

#######################
#       ELISE         #
#######################