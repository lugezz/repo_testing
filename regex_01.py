import re

str = 'Python is a programming language'
# Search using regex
x = re.search('language$', str)
print(x is None)

x = re.search('languag2$', str)
print(x is None)

x = re.search('gol|language|futbol$', str)
print(x is None)
