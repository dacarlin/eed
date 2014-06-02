from sys import argv
from re import findall
print(findall(r'\w+', argv[1]))
