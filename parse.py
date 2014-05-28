from sys import argv
mutations = argv[1]
mutations = mutations.strip() 
print("Stripped:", mutations)

# len('A1000A'), AKA biggest single mutant, is 6
# len('A1A A1A'), AKA smallest double mutant, is 7
if len(mutations) < 7:
  # it's a single mutant 
  print("It's a single mutant, way:", mutations)
else:
  if "+" in mutations:
    print("There's a plus")
    mutations = mutations.split("+")
  if "," in mutations:
    print("It's commas")
    mutations = mutations.split(",")
  if " " in mutations:
    print("Space-delimited")
    mutations = mutations.split(" ")

mutations = [ mutation.strip() for mutation in mutations ]
print(mutations)


