import re

# listilla = [
#     'cachulaescachula.wd5.com.myworkday/', 
#     'wd4', 
#     'noanda.cachulaescachula.com.myworkday/',
#     'cachulaescachula.wd2.com.myworkday/'
# ]

# for it in listilla:
#     tmp = re.split("\.wd[1-6]", it)
#     if len(tmp)> 0:
#         print (tmp)
    

listilla = [
    'cachula.careers.smartrecruiters.com/rocketero', 
    'careers.smartrecruiters.com/ulala', 
    'noanda.cachulaescachula.com.myworkday/',
    'careers.smartrecruiters.com/lalal/peroper'
]

var = "careers.smartrecruiters.com"

for it in listilla:
    tmp = re.split("careers.smartrecruiters.com/", it)
    if len(tmp)> 1:
        print (tmp[1].split("/")[0])
    