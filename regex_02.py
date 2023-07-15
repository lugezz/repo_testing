import re

date_pattern = r"(.+?)[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"
this_str = 'New Contact 01/20 1/20/2023 Hey new'
pattern = re.search(date_pattern, this_str)

print(pattern.group(1))
