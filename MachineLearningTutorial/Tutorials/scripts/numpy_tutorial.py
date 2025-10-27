import numpy as np


list1 = [1, 2, 3, 4, 5]
# print(list1)
# print(list1[0])

list2 = ["John Elder", 41, list1, True]
# print(list2)
# print(list2[1])

# Numpy -- Numeric Python
# ndarray = n-dimensional array

np1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(np1)
print(np1.shape)

np2 = np.arange(10)
print(np2)
print(type(np2))

# step
np3 = np.arange(0, 10, 2)
print(np3)

# zeros
np4 = np.zeros(10)
print(np4)

# multidimensional zeros
np5 = np.zeros([2, 10])
print(np5)

# Full
np6 = np.full((10), 6)
print(np6)

# multidimensional full
np7 = np.full((2, 10), 6)
print(np7)

# convert python lists to np
my_list = [1, 2, 3, 4, 5]
np8 = np.array(my_list)
print(np8)


# np1 slicing numpy arrays
np1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
np1 = np.arange(1, 10)
# return 2,3, 4, 6
print(np1[1:5])

# return from sth. till the end of the array
print(np1[3:])

# return negative slices
print(np1[-3:-1])

# steps
print(np1[1:5])
print(np1[1:5:2])

# steps on the entire array
print(np1[::2])
print(np1[::3])

# slice a 2-d array
np2 = np.array([[1,2,3,4,5], [6,7,8,9,10]])
print(np2[1, 2])

# slice a 2-d array
print(np2[0:1, 1:3])

print(np2[:, 1:3])
print('---')
print(np2[0:2, 1:3])

# numpy universal function
np1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
print(np1)

# square root of each element
print(np.sqrt(np1))

np1 = np.array([-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# absolute value
print(np.absolute(np1))

# np1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# exponential
print(np.exp(np1))

# min/max
print(np.max(np1))
print(np.min(np1))

# sign positive or negative
print(np.sign(np1))

# trig sin cos log
print(np.sin(np1))
print(np.cos(np1))
# print(np.log(np1))

# copy vs. view
np1 = np.array([0, 1, 2, 3, 4, 5])

# create a view
np2 = np1.view()
print(f"Original NP1 {np1}")
print(f"Original NP2 {np2}")

np1[0] = 41
print(f"Original NP1 {np1}")
print(f"Original NP2 {np2}")

np1 = np.array([0, 1, 2, 3, 4, 5])
# create a copy
np2 = np1.copy()

print(f"original np1 {np1}")
print(f"original np2 {np2}")

np2[0] = 41

print(f"changed np1 {np1}")
print(f"changed np2 {np2}")

# shape
# create 1-d array
np1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
print(np1)
print(np1.shape)

# create a 2-d array and get shape
np2 = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]])
print(np2)
print(np2.shape)

np3 = np1.reshape(3, 4)
print(np3)

np4 = np1.reshape(3, 2, 2)
print(np4)
print(np4.shape)

# flatten to 1-d
np5 = np4.reshape(-1)
print(np5)
print(np5.shape)
print(np5.view())


# 1-d
np1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
for x in np1:
    print(x)

# 2-d
np2 = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
for x in np2:
    print(x)
    for y in x:
        print(y)

# 3-d
np3 = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
for x in np3:
    for y in x:
        for z in y:
            print(z)

# use np.nditer()
for x in np.nditer(np3):
    print(x)

# np.sort() is different when it comes to multiple dimensional array for the sort in python
# np.sort() Numerical
np1 = np.array([6, 7, 4, 9, 0, 2, 1])
print(np.sort(np1))

# Alphabetical
np2 = np.array(['John', 'Tina', 'Aaron', 'Zed'])
print(np2)
print(np.sort(np2))

# booleans
np3 = np.array([True, False, False, True])
print(np3)
print(np.sort(np3))

# return a copy not change the original
print(np1)
print(np.sort(np1))
print(np1)

# 2-d
np4 = np.array([[6,7, 1, 9], [8, 5, 3, 0]])
print(np4)
print(np.sort(np4))


# search
np1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 3])
print(np1)
x = np.where(np1 == 3)
print(x)
print(x[0])
print(np1[x[0]])

# return even items
y = np.where(np1 % 2 == 0)
print(np1[y])

# return odd items
z = np.where(np1 % 2 == 1)
print(z[0])

np1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

x = [True, True, False, False, False, False, False, False, False, False]
print(np1)
print(np1[x])

filtered = []
for thing in np1:
    if thing % 2 == 0:
        filtered.append(True)
    else:
        filtered.append(False)
print(np1)
print(filtered)
print(np1[filtered])

# shortcut for filter
filtered = np1 % 2 == 1
print(filtered)
print(np1[filtered])
