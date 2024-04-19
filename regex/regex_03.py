from pprint import pprint
import re

date_pattern = r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}|Yesterday|Today|[0-9] days ago'
date_pattern2 = r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"
# date_pattern3 = date_pattern += 'Yesterday|Today'
this_str = 'New Contact 01/20 1/20/2023 Hey new but Yesterday lalalla es Today kskddkllkdklad'
this_str += '2 days ago soy ultima parte'

splitted_str = re.split(date_pattern, this_str)

pprint(splitted_str)

ll = ['a', 'b']
print(len(ll))
