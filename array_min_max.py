pole = [3, 2, 7, 10, 0, 5, -10, 4, 6]
min = pole[0]
max = pole[0]

for i in range(0, len(pole), 2):
    if pole[i] < pole[i+1]:
        if pole[i] < min: min = pole[i]
        if pole[i+1] > max: max = pole[i+1]
    else:
        if pole[i] > max: max = pole[i]
        if pole[i+1] < min: min = pole[i+1]


for n in pole:
    if n < min: min = n
    if n > max: max = n