
from nnf import Var, true, false
from lib204 import Encoding

num_pokemon = 3 # can change this to whatever
foe = []
player = []
types = ["fire", "water", "grass", "electric", "ice", "ground", "flying", "rock"] 

# initializing variables
# each pokemon is a dictionary of types
for i in range(num_pokemon):
  foe_mon = {}
  player_mon = {}
  for i in range(len(types)):
    foe_mon[types[i]] = Var(False)
    player_mon[types[i]] = Var(False)
  foe.append(foe_mon)
  player.append(player_mon)

def make_implication(left, right):
  return (left.negate() | right)

def exclude_types(pokemon, type1, type2):
  exclusion = false # for disjunctions initialize as false and conjunctions initialize as true
  for i in range(len(types)):
    if types[i] != type1 and types[i] != type2:
      exclusion |= pokemon[types[i]]
  return exclusion 

# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    for i in range(num_pokemon): # constraints for EACH pokemon

      #dual typing
      for i in range(num_pokemon):
        # whether dual type or not
        dual_foe = true
        dual_player = true

        #format
        for t in range(len(types)):
          for y in range(len(types)):
            if y != t:
              dual_foe &= foe[i][types[t]] & foe[i][types[y]] & (exclude_types(foe[i], types[t], types[y])).negate()
              dual_player &= player[i][types[t]] & player[i][types[y]] & (exclude_types(player[i], types[t], types[y])).negate()
        
        # type possibilities (1 or 2)
        foe_type = dual_foe
        player_type = dual_player
        for t in range(len(types)):
          foe_type |= (foe[i][types[t]] & (exclude_types(foe[i], types[t], None)))
          player_type |= (player[i][types[t]] & (exclude_types(player[i], types[t], None)))
        E.add_constraint(foe_type)
        E.add_constraint(player_type) 

      # if foe is this type >> (.negate() |) these player types are strong and ~these player types are weak against
      # FIRE
      #E.add_constraint(make_implication(foe[i]["fire"], (player[i]["water"] | player[i]["ground"] | player[i]["rock"]) & (~player[i]["grass"] & ~player[i]["ice"])))
      E.add_constraint(foe[i]["fire"].negate() | ((player[i]["water"] | player[i]["ground"] | player[i]["rock"]) & (~player[i]["grass"] & ~player[i]["ice"])))
      # WATER
      E.add_constraint(foe[i]["water"].negate() | ((player[i]["grass"] | player[i]["electric"]) & (~player[i]["fire"] & ~player[i]["ground"] & ~player[i]["rock"])))
      # GRASS
      E.add_constraint(foe[i]["grass"].negate() | ((player[i]["fire"] | player[i]["ice"] | player[i]["flying"]) & (~player[i]["water"] & ~player[i]["ground"] & ~player[i]["rock"])))
      # ELECTRIC
      E.add_constraint(foe[i]["electric"].negate() | ((player[i]["ground"]) & (~player[i]["water"] & ~player[i]["flying"])))
      # ICE
      E.add_constraint(foe[i]["ice"].negate() | ((player[i]["fire"] | player[i]["rock"]) & (~player[i]["grass"] & ~player[i]["ground"] & ~player[i]["flying"])))
      # GROUND
      E.add_constraint(foe[i]["ground"].negate() | ((player[i]["water"] | player[i]["grass"] | player[i]["ice"]) & (~player[i]["fire"] & ~player[i]["electric"] & ~player[i]["rock"])))
      # FLYING
      E.add_constraint(foe[i]["flying"].negate() | ((player[i]["electric"] | player[i]["ice"] | player[i]["rock"]) & (~player[i]["grass"])))
      # ROCK
      E.add_constraint(foe[i]["rock"].negate() | ((player[i]["water"] | player[i]["grass"] | player[i]["ground"]) & (~player[i]["fire"] & ~player[i]["ice"] & ~player[i]["flying"])))  
      
    return E


if __name__ == "__main__":

    T = example_theory()
    print("it works :)")
    """
    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
    """
