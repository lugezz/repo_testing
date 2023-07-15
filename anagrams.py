def are_anagrams(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()

    if len(s1)!=len(s2):
        return False

    if sorted(s1)==sorted(s2):
        return True
    else:
        return False


print (are_anagrams("Cachula","Lucacha"))
print (are_anagrams("garden","danger"))
print (are_anagrams("nameless","salesmen"))
print (are_anagrams("gardenos","dangeras"))