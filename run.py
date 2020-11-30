
from nnf import Var, true, false
from lib204 import Encoding
from random import randint

num_pokemon = 1 # number of pokemon each party has
foe = [] # the foe's party of pokemon
player = [] # the player's party of pokemon
# different pokemon types
types = ["fire", "water", "grass", "electric", "ice", "ground", "flying", "rock"] 

# initializing variables
""" each pokemon is a dictionary of types, whether the key is true if the pokemon
is of that type, and the key is false if the pokemon is not of that type
"""
for i in range(num_pokemon):
  foe_mon = {}
  player_mon = {}
  for j in range(len(types)): #initialize each type of each pokemon
    foe_mon[types[j]] = false
    # our variables are the types of the player's pokemon
    # taking the format '#number_type'
    player_mon[types[j]] = Var(str(i) + '_' + types[j]) 
  # add pokemon to the party
  foe.append(foe_mon)
  player.append(player_mon)

"""function for making implications
"""
def make_implication(left, right):
  return (left.negate() | right)

"""
This function returns 'exclusion,' a disjunction of all 
types that aren't in included_types
"""
def exclude_types(pokemon, included_types):
  exclusion = false 
  for t in types: # iterate through all types
    if t not in included_types: # check if current type should be excluded
      exclusion |= pokemon[t]
  return exclusion 

# our theory
def optimal_battle_strategy():
    E = Encoding()
    for i in range(num_pokemon):
      # whether dual type or not
      dual_foe = false
      dual_player = false
      
      # all the possible dual types for both foe and player pokemon
      #if a pokemon is type A and type B, it can't be any other type
      for t in range(len(types)):
        for y in range(t+1, len(types)):
          if y != t: # check to see if the types being compared aren't the same
            dual_foe |= (foe[i][types[t]] & foe[i][types[y]] & (exclude_types(foe[i], [types[t], types[y]])).negate()) # exclude types that aren't t or y
            dual_player |= player[i][types[t]] & player[i][types[y]] & (exclude_types(player[i], [types[t], types[y]])).negate()
      
      # all type possibilities (can have 2 and nothing else OR 1 and nothing else)
      # if single typed, a pokemon is type A and can't be any other type
      foe_type = dual_foe
      player_type = dual_player
      for t in range(len(types)):
        foe_type |= (foe[i][types[t]] & (exclude_types(foe[i], [types[t]])).negate())
        player_type |= (player[i][types[t]] & (exclude_types(player[i], [types[t]])).negate())
      E.add_constraint(foe_type)
      E.add_constraint(player_type) 

      # nonexisting type combination (fire-grass)
      E.add_constraint((player[i]["fire"] & player[i]["grass"]).negate())
      E.add_constraint((foe[i]["fire"] & foe[i]["grass"]).negate())
      
      """if a foe is type A, then player type B is strong against it and
      player type C is weak against it
      thus we say foe type A implies player type B and not player type C
      """
      #FIRE is weak against water, ground, and rock; strong against grass and ice
      E.add_constraint(make_implication(foe[i]["fire"], ((player[i]["water"] | player[i]["ground"] | player[i]["rock"]) & (player[i]["grass"].negate() & player[i]["ice"].negate()))))

      # WATER is weak against grass and electric; strong against fire, ground, and rock
      E.add_constraint(make_implication(foe[i]["water"], ((player[i]["grass"] | player[i]["electric"]) & (player[i]["fire"].negate() & player[i]["ground"].negate() & player[i]["rock"].negate()))))

      # GRASS is weak against fire, ice, and flying; strong against water, ground, and rock
      E.add_constraint(make_implication(foe[i]["grass"], ((player[i]["fire"] | player[i]["ice"] | player[i]["flying"]) & (player[i]["water"].negate() & player[i]["ground"].negate() & player[i]["rock"].negate()))))

      # ELECTRIC is ineffective against ground; strong against water and flying
      E.add_constraint(make_implication(foe[i]["electric"], ((player[i]["ground"]) & (player[i]["water"].negate() & player[i]["flying"].negate()))))

      # ICE is weak against fire and rock; strong against grass, ground, and flying
      E.add_constraint(make_implication(foe[i]["ice"], ((player[i]["fire"] | player[i]["rock"]) & (player[i]["grass"].negate() & player[i]["ground"].negate() & player[i]["flying"].negate()))))

      # GROUND is weak against water, grass, and ice; ineffective against flying; strong against fire, and rock; immune to electric
      E.add_constraint(make_implication(foe[i]["ground"], ((player[i]["water"] | player[i]["grass"] | player[i]["ice"] | player[i]["flying"]) & (player[i]["fire"].negate() & player[i]["electric"].negate() & player[i]["rock"].negate()))))

      # FLYING is weak against electric, ice, and rock; strong against grass; immune to ground
      E.add_constraint(make_implication(foe[i]["flying"], ((player[i]["electric"] | player[i]["ice"] | player[i]["rock"]) & (player[i]["grass"].negate() & player[i]["ground"].negate()))))

      # ROCK is weak against water, grass, and ground; strong against fire, ice, and flying
      E.add_constraint(make_implication(foe[i]["rock"], ((player[i]["water"] | player[i]["grass"] | player[i]["ground"]) & (player[i]["fire"].negate() & player[i]["ice"].negate() & player[i]["flying"].negate()))))
      
    return E

"""
Displaying the solution in an easy, readable way
"""
def display_solution(sol):
  print('Your foe\'s Pokemon:')
  for i in range (len(foe)): # iterate through foe's party
    print('Foe Pokemon %s' % str(i + 1) + '.', end=" ") # number in party
    full_type = ''
    for type_key in foe[i]: # iterate through types of that pokemon
      if foe[i][type_key] == true:
        if full_type == '':
          full_type += type_key
        else: # one type has already been displayed
          full_type += '-' + type_key
    print(full_type)
  print('Your Pokemon:')
  if not sol: # no solution was found; see our documentation
    print('Your foe is too powerful. Give up now.')
  else: # valid solution
    for i in range(len(player)): # iterate through player's party
      print('Player Pokemon %s' % str(i  + 1) + '.', end=" ")
      full_type = ''
      for type_key in sol: 
        """first letter in each Var is the number describing the 
        pokemon's place in the player's party. for aesthetic purposes,
        we will display just the type name without the #_ in front of it
        """ 
        if (type_key[0] == str(i)): 
          if sol[type_key]: 
            if full_type == '':
              full_type += type_key[2:] 
            else: # one type has already been displayed
              full_type += '-' + type_key[2:]
      print(full_type)

# randomize the foe's party
def randomize_foe():
  for pokemon in foe:
      # choose random number of types (1 or 2)
      num_types = randint(1, 2)
      # choose random type
      type1 = types[randint(0, len(types) - 1)]
      pokemon[type1] = true
      if num_types == 2: # choose 2nd random type if 2 types were selected
        type2 = types[randint(0, len(types) - 1)]
        if type1 == types[0]: # fire grass is not an existing type combination
          while type2 == types[2]:
            type2 = types[randint(0, len(types) - 1)]
        elif type1 == types[2]:
          while type2 == types[0]:
            type2 = types[randint(0, len(types) - 1)]
        pokemon[type2] = true

if __name__ == "__main__":
    randomize_foe() # if not putting in pokemon yourself, randomize the foe's party
    T = optimal_battle_strategy()
    sol = T.solve()
    display_solution(sol)
    
