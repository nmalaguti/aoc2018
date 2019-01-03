
r = [0] * 6
numbers = set()
last = -1

while True:

    if r[1] == 0:
        
        r[4] = 123
        r[1] += 1
    

    elif r[1] == 1:
        
        r[4] = r[4] & 456
        r[1] += 1
    

    elif r[1] == 2:
        
        r[4] = int(r[4] == 72)
        r[1] += 1
    

    elif r[1] == 3:
        
        r[1] = r[4] + r[1]
        r[1] += 1
    

    elif r[1] == 4:
        
        r[1] = 0
        r[1] += 1
    

    elif r[1] == 5:
        
        r[4] = 0
        r[1] += 1
    

    elif r[1] == 6:
        
        r[3] = r[4] | 65536
        r[1] += 1
    

    elif r[1] == 7:
        
        r[4] = 12670166
        r[1] += 1
    

    elif r[1] == 8:
        
        r[2] = r[3] & 255
        r[1] += 1
    

    elif r[1] == 9:
        
        r[4] = r[4] + r[2]
        r[1] += 1
    

    elif r[1] == 10:
        
        r[4] = r[4] & 16777215
        r[1] += 1
    

    elif r[1] == 11:
        
        r[4] = r[4] * 65899
        r[1] += 1
    

    elif r[1] == 12:
        
        r[4] = r[4] & 16777215
        r[1] += 1
    

    elif r[1] == 13:
        
        r[2] = int(256 > r[3])
        r[1] += 1
    

    elif r[1] == 14:
        
        r[1] = r[2] + r[1]
        r[1] += 1
    

    elif r[1] == 15:
        
        r[1] = r[1] + 1
        r[1] += 1
    

    elif r[1] == 16:
        
        r[1] = 27
        r[1] += 1
    

    elif r[1] == 17:
        
        r[2] = 0
        r[1] += 1
    

    elif r[1] == 18:
        
        r[3] = r[2] = r[3] // 256
        r[1] = 8
        continue
        
        r[5] = r[2] + 1
        r[1] += 1
    

    elif r[1] == 19:
        
        r[5] = r[5] * 256
        r[1] += 1
    

    elif r[1] == 20:
        
        r[5] = int(r[5] > r[3])
        r[1] += 1
    

    elif r[1] == 21:
        
        r[1] = r[5] + r[1]
        r[1] += 1
    

    elif r[1] == 22:
        
        r[1] = r[1] + 1
        r[1] += 1
    

    elif r[1] == 23:
        
        r[1] = 25
        r[1] += 1
    

    elif r[1] == 24:
        
        r[2] = r[2] + 1
        r[1] += 1
    

    elif r[1] == 25:
        
        r[1] = 17
        r[1] += 1
    

    elif r[1] == 26:
        
        r[3] = r[2]
        r[1] += 1
    

    elif r[1] == 27:
        
        r[1] = 7
        r[1] += 1
    

    elif r[1] == 28:
        
        if last == -1:
            print(r[4])
        if r[4] in numbers:
            print(last)
            exit()
        last = r[4]
        numbers.add(last)
        
        r[2] = int(r[4] == r[0])
        r[1] += 1
    

    elif r[1] == 29:
        
        r[1] = r[2] + r[1]
        r[1] += 1
    

    elif r[1] == 30:
        
        r[1] = 5
        r[1] += 1
    

    else:
        exit()