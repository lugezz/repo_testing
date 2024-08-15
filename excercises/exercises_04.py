# Global variable

# Replace a global variable into a function

im_global = "Talleres"


def change_im_global(new_im_global):
    global im_global
    im_global = new_im_global


change_im_global("Talleres de Python")
print(im_global)


# I have 2 arrays (array_1) and (array_2) with numbers sorted and the values m and n for the length of each of these
# I want to create a function to merge it but not send a response, just change array_1 with the merged values
# If an array is empty it should  return an array including just the first elements of the other array

# For example:

# Case1 = [1, 2, 3, 0, 0, 0], [2, 5, 6], 6, 3
# Should return [1, 2, 2, 3, 5, 6]

# Case2 = [], [2, 5, 6], 0, 3
# Should return [2]

# Case3 = [1], [], 1, 0
# Should return [1]

def merge_array(array_1, array_2, m, n):
    if m == 0:
        array_1 = array_2
    elif n == 0:
        array_1 = array_1
    else:
        array_1 = array_1 + array_2
        array_1.sort()
    print(array_1)
