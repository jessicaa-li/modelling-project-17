
from nnf import Var
from lib204 import Encoding

"""
# Call your variables whatever you want
a = Var('a')
b = Var('b')
c = Var('c')
x = Var('x')
y = Var('y')
z = Var('z')
"""
num_pokemon = 3 # can change this to whatever
foe = []
player = []
types = ["fire", "water", "grass", "electric", "ground", "rock", "ice", "flying"] #idk if we actually need this


# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    for i in range(num_pokemon):
      # if foe is this type >> these types are strong and ~these types are weak against
      E.add_constraint(foe[i]["fire"] >> ((player[i]["water"] | player[i]["ground"] | player[i]["rock"]) & (~player[i]["grass"] & ~player[i]["ice"]))) # format; do this for the rest of the types
    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
