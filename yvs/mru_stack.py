import sys
from collections import OrderedDict


# A Most Recently Used (MRU) stack implementation using OrderedDict; the key
# characteristic is that when a key that already exists in the stack is added
# again, it is moved to the top of the stack. If the stack exceeds the maximum
# size, the oldest entry is purged
class MRUStack:
    # Initialize the MRUStack with an initial set of elements and an optional
    # maximum number of entries to keep before purging
    def __init__(self, sequence, maxsize=sys.maxsize):
        self.maxsize = maxsize
        self.stack = OrderedDict()
        for element in sequence[:maxsize]:
            if element in self.stack:
                self.stack.move_to_end(element)
            else:
                self.stack[element] = None

    # Adds the specified key to the stack; if the key already exists, the
    # existing entry is moved to the top of the stack. Otherwise, the new entry
    # is added to the top of the stack like normal.
    def add(self, key):
        if key in self.stack:
            self.stack.move_to_end(key)
        else:
            self.stack[key] = None
            if len(self.stack) > self.maxsize:
                self.stack.popitem(last=False)

    # Remove the specified key from the stack, if it exists; if the key does not
    # exist, the method does nothing
    def remove(self, key):
        if key in self.stack:
            del self.stack[key]

    # Return true if a key exists in the stack; otherwise, return false
    def __contains__(self, key):
        return key in self.stack

    # Iterate over the keys in the stack in MRU order
    def __iter__(self):
        return iter(self.stack)

    # Retrieve the number of entries in the stack
    def __len__(self):
        return len(self.stack)

    # Construct a string representation of the stack
    def __repr__(self):
        return f"{self.__class__.__name__}({list(self.stack)})"
