with open('day_05/input.txt', 'r') as input_file:
    data_input = input_file.read()

data = list(data_input.strip())

def cancel(a, b):
    if a.isupper() and b.islower() and a.upper() == b.upper():
        return True
    if a.islower() and b.isupper() and a.upper() == b.upper():
        return True

    return False

def react(data):
    i = 0
    while i < len(data):
        if i == 0:
            i += 1
            continue
        
        if cancel(data[i], data[i-1]):
            del data[i-1:i+1]
            i -= 1
            continue
        
        i += 1
    
    for i in range(1, len(data)):
        assert not cancel(data[i], data[i-1]), (i, data[i-1:i+1])

    return data

print(len(react(list(data))))

unit_types = set(x.lower() for x in data)

result = {}
for unit_type in unit_types:
    result[unit_type] = len(react(list(filter(lambda x: x != unit_type and x != unit_type.upper(), data))))

print(min(result.values()))