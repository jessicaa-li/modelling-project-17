
from nnf import Var, true, false
from lib204 import Encoding
from random import randint

num_pokemon = 3 # number of pokemon each party has
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
      player type C is weak against it (or that type C would be less effective on type A)
      thus we say foe type A implies player type B and not player type C
      """
      #FIRE is weak against water, ground, and rock; strong against grass and ice; fire is not very effective on fire
      E.add_constraint(make_implication(foe[i]["fire"], ((player[i]["water"] | player[i]["ground"] | player[i]["rock"]) & (player[i]["grass"] | player[i]["ice"] | player[i]["fire"]).negate())))

      # WATER is weak against grass and electric; strong against fire, ground, and rock; ice is weak against it; water is not very effective on water
      E.add_constraint(make_implication(foe[i]["water"], ((player[i]["grass"] | player[i]["electric"]) & (player[i]["fire"] | player[i]["ground"] | player[i]["rock"] | player[i]["ice"] | player[i]["water"]).negate())))

      # GRASS is weak against fire, ice, and flying; strong against water, ground, and rock; grass is not very effective on grass
      E.add_constraint(make_implication(foe[i]["grass"], ((player[i]["fire"] | player[i]["ice"] | player[i]["flying"]) & (player[i]["water"] | player[i]["ground"] | player[i]["rock"] | player[i]["grass"]).negate())))

      # ELECTRIC is ineffective against ground; strong against water and flying; electric is not very effective on electric
      E.add_constraint(make_implication(foe[i]["electric"], ((player[i]["ground"]) & (player[i]["water"] | player[i]["flying"] | player[i]["electric"]).negate())))

      # ICE is weak against fire, rock, and water; strong against grass, ground, and flying; ice is not very effective on ice
      E.add_constraint(make_implication(foe[i]["ice"], ((player[i]["fire"] | player[i]["rock"] | player[i]["water"]) & (player[i]["grass"] | player[i]["ground"] | player[i]["flying"] | player[i]["ice"]).negate())))

      # GROUND is weak against water, grass, and ice; ineffective against flying; strong against fire, and rock; immune to electric
      E.add_constraint(make_implication(foe[i]["ground"], ((player[i]["water"] | player[i]["grass"] | player[i]["ice"] | player[i]["flying"]) & (player[i]["fire"] | player[i]["electric"] | player[i]["rock"]).negate())))

      # FLYING is weak against electric, ice, and rock; strong against grass; immune to ground
      E.add_constraint(make_implication(foe[i]["flying"], ((player[i]["electric"] | player[i]["ice"] | player[i]["rock"]) & (player[i]["grass"] | player[i]["ground"]).negate())))

      # ROCK is weak against water, grass, and ground; strong against fire, ice, and flying
      E.add_constraint(make_implication(foe[i]["rock"], ((player[i]["water"] | player[i]["grass"] | player[i]["ground"]) & (player[i]["fire"] | player[i]["ice"] | player[i]["flying"]).negate())))
      
    return E

"""
Displaying the solution in an easy, readable way
"""
def display_solution(sol):
  print('Your foe\'s Pokémon:')
  for i in range (len(foe)): # iterate through foe's party
    print('Foe Pokémon %s' % str(i + 1) + '.', end=" ") # number in party
    full_type = ''
    for type_key in foe[i]: # iterate through types of that pokemon
      if foe[i][type_key] == true:
        if full_type == '':
          full_type += type_key
        else: # one type has already been displayed
          full_type += '-' + type_key
    print(full_type)
  print('Your Pokémon:')
  if not sol: # no solution was found; see our documentation
    print('No optimal Pokémon typing found. Give up now.')
  else: # valid solution
    for i in range(len(player)): # iterate through player's party
      print('Player Pokémon %s' % str(i  + 1) + '.', end=" ")
      full_type = ''
      for type_key in sol: 
        """first letter in each Var is the number describing the 
        Pokémon's place in the player's party. for aesthetic purposes,
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

def test_all_combos():
  # this assumes num_pokemon = 1
  for t in types:
    foe[0][t] = true
    T = optimal_battle_strategy()
    sol = T.solve()
    display_solution(sol)
    print('\n')
    foe[0][t] = false

  for i in range(len(types)-1):
    for j in range(i+1, len(types)):
      if (types[i] == "fire" and types[j] == "grass") or (types[i] == "grass" and types[j] == "fire"):
        print('invalid type combination\n')
      else:
        foe[0][types[i]] = true
        foe[0][types[j]] = true
        T = optimal_battle_strategy()
        sol = T.solve()
        display_solution(sol)
        print('\n')
        foe[0][types[i]] = false
        foe[0][types[j]] = false

if __name__ == "__main__":
    choice = input('Enter 0 to choose the foe\'s party, 1 to test all combos, or enter any other key to randomize the foe\'s party, or enter any other key : ')
    if choice == '0': # randomly selects the foe's pokemon
      for p in range(num_pokemon): # choose the foe pokemon
        print(f'Foe #{p+1}')
        type1 = None
        type2 = None
        while (type1 not in types):
          type1 = (input('Choose type 1: ')).lower()
        while (type2 not in types and type2 != 'single'):
          type2 = (input('Choose type 2 (type \'single\' for a single-type Pokémon): ')).lower()
        if (type1 == 'fire' and type2 == 'grass') or (type1 == 'grass' and type2 == 'fire'):
          print('This type combination does not exist in the world of Pokémon.')
          break 
        foe[p][type1] = true
        if type2 != 'single':
          foe[p][type2] = true
    elif choice == '1':
        if num_pokemon == 1:
          test_all_combos()
        else:
          print('Please set number of Pokémon to 1.')
    else:
      randomize_foe()

    if choice != '1':
      T = optimal_battle_strategy()
      sol = T.solve()
      display_solution(sol)
