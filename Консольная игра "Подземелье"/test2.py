import re

type_1 = r'\w+-\w+'
type_2 = r'\w'
type_3 = r'\w+[^-]\w+'
type_4 = r'(\w+)(?:-|\w+]'



total = 0
strn = input()

matches_1 = re.findall(type_1, strn)
matches_2 = re.findall(type_2, strn)
matches_3 = re.findall(type_3, strn)
matches_4 = re.findall(type_4, strn)


print(matches_1, matches_2, matches_3)
print(matches_4)
