import re

"""
Write a Python program to find the sequences of one upper case letter followed
by lower case letters.
"""


def text_match(text):
    patterns = '[A-Z]+[a-z]+$'
    if re.search(patterns, text):
        return 'Found a match!'
    else:
        return 'Not matched!'


print(text_match("AaBbGg"))
print(text_match("Python"))
print(text_match("python"))
print(text_match("PYTHON"))
print(text_match("aA"))
print(text_match("Aa"))


"""
Write a Python program to check for a number at the end of a string.
"""


def end_num(string):
    text = re.compile(r".*[0-9]$")
    if text.match(string):
        return True
    else:
        return False


print(end_num('abcdef'))
print(end_num('abcdef6'))


"""
Write a Python program to find all adverbs and their positions in a given
sentence.
"""


text = "Clearly, he has no excuse for such behavior."
for m in re.finditer(r"\w+ly", text):
    print('%d-%d: %s' % (m.start(), m.end(), m.group(0)))


"""
A vowel is a syllabic speech sound pronounced without any stricture in the
vocal tract.Vowels are one of the two principal classes of speech sounds,
the other being the consonant.

Write a Python program that checks whether a word stars and ends with a vowel
in a given string. Return true if a word matches the condition; otherwise,
return false.

Sample Data:
("Red Orange White") -> True
("Red White Black") -> False
("abcd dkise eosksu") -> True
"""


def test(text):
    return bool(re.findall('[/^[aeiou]$|^([aeiou]).*\1$/', text))


text = "Red Orange White"
print("Original string:", text)
print("Check beginning and end of a word in the said string with a vowel:")
print(test(text))
text = "Red White Black"
print("\nOriginal string:", text)
print("Check beginning and end of a word in the said string with a vowel:")
print(test(text))
text = "abcd dkise eosksu"
print("\nOriginal string:", text)
print("Check beginning and end of a word in the said string with a vowel:")
print(test(text))
