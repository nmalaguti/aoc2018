from cached_property import cached_property

# data_input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
with open('day_08/input.txt', 'r') as input_file:
    data_input = input_file.read().strip()
data = [int(n) for n in data_input.split()]

class Node:
  
    def __init__(self, data):
        data_iter = iter(data)
        num_children = next(data_iter)
        num_metadata = next(data_iter)

        self.children = [
            Node(data_iter) for _ in range(num_children)
        ]

        self.metadata = [
            next(data_iter) for _ in range(num_metadata)
        ]

    def __repr__(self):
        return "Node({}, {})".format(self.metadata, self.children)

    @cached_property
    # @property
    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(self._value())
            
    def _value(self):
        for m in self.metadata:
            if m == 0 or m > len(self.children):
                yield 0
            else:
                yield self.children[m - 1].value

def walk(node):
    yield from node.metadata
    for child in node.children:
        yield from walk(child)

root = Node(data)
# print(root)

print(sum(walk(root)))
print(root.value)