__author__ = 'Vi'


from board import Move


l = [1, 2, 3, 4]
m = list(map(lambda x: x + 1, l))
print(m)

ls = [list(range(4)) for x in range(4)]
print(ls)
ls = [list(map(lambda x: 1, row)) for row in ls]
print(ls)
