# Code a Mutable array with automatic resizing
from collections.abc import Iterable
import ctypes

# A memory level implementation of a resizable array
class ArrayList:
    # Array initialization
    def __init__(self, initial_capacity=8):
        self.capacity = initial_capacity
        self.size = 0
        self.storage = self._allocate(self.capacity)
    
    def __iter__(self):
        base_ptr = self._get_pointer(self.storage)
        for i in range(self.size):
            yield base_ptr[i]
    
    def __eq__(self, other):
        if not isinstance(other, ArrayList):
            return False
        
        if len(self) != len(other):
            return False
        
        return all(a == b for a, b in zip(self, other))
        
    # Get the pointer of the stored value
    def _get_pointer(self, storage_block):
        return ctypes.cast(storage_block, ctypes.POINTER(ctypes.py_object))
    
    # Allocate storage
    def _allocate(self, capacity):
        return (capacity * ctypes.py_object)()
    
    # When the storage reaches capacity, allocate new storage and transfer data to new array. Achieving the resizing effect.
    def _resize(self, new_capacity):
        new_storage = self._allocate(new_capacity)
        src_ptr = self._get_pointer(self.storage)
        dst_ptr = self._get_pointer(new_storage)
        for i in range(self.size):
            dst_ptr[i] =(src_ptr[i])
        self.storage = new_storage
        self.capacity = new_capacity
    
    # Transform negative index to usable index
    def _normalize_index(self, index):
        if index < 0:
            index = index + self.size
        return index
    
    # Get item from array
    def __getitem__(self, index):
        normalized_index = self._normalize_index(index)
        if normalized_index < 0 or normalized_index >= self.size:
            raise IndexError("Index out of bounds")
        
        base_ptr = self._get_pointer(self.storage)
        target_ptr = base_ptr[normalized_index]
        return target_ptr
    
    # Set item in array
    def __setitem__(self, index, item):
        normalized_index = self._normalize_index(index)
        if normalized_index < 0 or normalized_index >= self.size:
            raise IndexError("Index out of bounds")
        
        base_ptr = self._get_pointer(self.storage)
        base_ptr[normalized_index] = item
        
    # Get number of items in array
    def __len__(self):
        return self.size
    
    # Return total capacity of the array
    def get_capacity(self):
        return self.capacity
    
    # Returns true if array is empty
    def is_empty(self):
        return self.size == 0
    
    # Returns item at the index attached
    def at(self, index):
        return self.__getitem__(index)
    
    # Add item to end of array
    def append(self, item):
        if self.size == self.capacity:
            new_capacity = int(self.capacity * 1.5)
            self._resize(new_capacity)
        
        base_ptr = self._get_pointer(self.storage)
        base_ptr[self.size] = item
        self.size += 1
    
    # Attaches an item to the front of an array
    def prepend(self, item):
        if self.size == self.capacity:
            new_capacity = int(self.capacity * 1.5)
            self._resize(new_capacity)
        
        base_ptr = self._get_pointer(self.storage)
        for i in range(self.size - 1, -1, -1):
            base_ptr[i + 1] = base_ptr[i]
        
        base_ptr[0] = item
        self.size += 1
        
    # Append multiple items to an array
    def push(self, *args):
        for i in args:
            self.append(i)
            
    # Insert an element at a particular index
    def insert(self, index, item):
        normalized_index = self._normalize_index(index)
        if self.size == self.capacity:
            new_capacity = int(self.capacity * 1.5)
            self._resize(new_capacity)
        
        base_ptr = self._get_pointer(self.storage)
        for i in range(self.size - 1, -1, -1):
            if i >= normalized_index:
                base_ptr[ i + 1] = base_ptr[i]

        base_ptr[normalized_index] = item
        
        self.size += 1
    
    # Remove the last item from the array. Optional resize capacity.
    def pop(self):
        if self.size == 0:
            raise IndexError("Pop from empty list")
        
        base_ptr = self._get_pointer(self.storage)
        item = base_ptr[self.size - 1]
        base_ptr[self.size - 1] = None
        self.size -= 1
        
        if self.size * 4 < self.capacity and self.capacity > 4:
            self._resize(int(self.capacity / 2))
        return item
    
    # Delete item at particular index
    def delete(self, index):
        normalized_index = self._normalize_index(index)
        if normalized_index < 0 or normalized_index >= self.size:
            raise IndexError("Index out of bounds")
        base_ptr = self._get_pointer(self.storage)
        
        for i in range(normalized_index, self.size - 1):
            base_ptr[i]  = base_ptr[i + 1]
        base_ptr[self.size -1] = None
        self.size -= 1
        
    # Remove item that matches value attached. Removes multiple items matching the value
    def remove(self, item):
            found = False
            base_ptr = self._get_pointer(self.storage)
            write_index = 0
            
            for i in range(self.size):
                if base_ptr[i] == item:
                    found = True
                else:
                    base_ptr[write_index] = base_ptr[i]
                    write_index += 1
                    
            if not found:
                raise ValueError(f"{item} not in array")
                
            for i in range(write_index, self.size):
                base_ptr[i] = None
                
            self.size = write_index
        
    # Find value and returns first index with that value. Returns -1 if not found
    def index(self, item):
        base_ptr = self._get_pointer(self.storage)
        
        for i in range(self.size):
            if base_ptr[i] == item:
                return i
        
        return -1
    
    def print(self):
        base_ptr = self._get_pointer(self.storage)
        for i in range(self.size):
            print(base_ptr[i])
        pass
    
    def clear(self):
        self.capacity = 8
        self.size = 0
        self.storage = self._allocate(self.capacity)
        
    def copy(self):
        base_ptr = self._get_pointer(self.storage)
        new_arr = ArrayList(self.capacity)
        for i in range(self.size):
            new_arr.append(base_ptr[i])
        return new_arr
    
    def count(self, item):
        base_ptr = self._get_pointer(self.storage)
        item_count = 0
        for i in range(self.size):
            if base_ptr[i] == item:
                item_count += 1
        return item_count
    
    def extend(self, items: Iterable):
        try:
            additional_size = len(items)
            required_capacity = self.size + additional_size
            if required_capacity > self.capacity:
                new_capacity = max(int(self.capacity * 1.5), required_capacity)
                self._resize(new_capacity)
        except (TypeError, AttributeError):
            pass
        for item in items:
            self.append(item)
    
    def sort(self, reverse = False):
        pass
    
    def bubble_sort(self):
        base_ptr = self._get_pointer(self.storage)
        flag = True
        while flag:
            flag = False
            for i in range(1, self.size):
                if base_ptr[i - 1] > base_ptr[i]:
                    flag = True
                    base_ptr[i-1], base_ptr[i] = base_ptr[i], base_ptr[i-1]
    
    def insertion_sort(self):
        base_ptr = self._get_pointer(self.storage)
        n = self.size
        for i in range(1, n):
            for j in range(i, 0, -1):
                if base_ptr[j-1] > base_ptr[j]:
                    base_ptr[j-1], base_ptr[j] = base_ptr[j], base_ptr[j-1]
                else:
                    break
    
    def selection_sort(self):
        base_ptr = self._get_pointer(self.storage)
        for i in range(self.size):
            min_index = i
            for j in range(i + 1, self.size):
                if base_ptr[j] < base_ptr[min_index]:
                    min_index = j
            base_ptr[i], base_ptr[min_index] = base_ptr[min_index], base_ptr[i]
    
    def merge_sort(self):
        base_ptr = self._get_pointer(self.storage)
        n = self.size
        if n == 1:
            return
        
        m = n // 2
        L = base_ptr[:m]
        R = base_ptr[m:]
        
        L = self.merge_sort(L)
        R = self.merge_sort(R)
        l, r = 0, 0
        L_len = len(L)
        R_len = len(R)
        
        sorted = [0] * n
        i = 0
        
        while l < L_len and r < R_len:
            if L[l] < R[r]:
                sorted[i] = L[l]
                l += 1
            else:
                sorted[i] = R[r]
                r += 1
            
            i += 1
        
        