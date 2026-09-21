import pytest
from array_list import ArrayList

def test_initialization():
    arr = ArrayList(initial_capacity=4)
    assert arr.get_capacity() == 4
    assert len(arr) == 0
    assert arr.is_empty() is True

def test_append():
    arr = ArrayList()
    arr.append(10)
    assert arr[0] == 10
    assert len(arr) == 1

def test_push():
    arr = ArrayList()
    arr.push(1)
    arr.push(2, 4, 5)
    assert arr[0] == 1 
    assert arr[3] == 5
    assert len(arr) == 4

def test_resize():
    arr = ArrayList(initial_capacity=2)
    arr.push(2, 3)
    assert arr.get_capacity() == 2
    
    arr.append(3)
    assert arr.get_capacity() == 3
    assert len(arr) == 3
    assert arr[2] == 3
    
    arr.push(1, 2)
    arr.pop()
    arr.pop()
    arr.pop()
    arr.pop()
    assert arr.get_capacity() == 3

def test_indexing():
    arr = ArrayList()
    arr.push("a", "b", "c")
    assert arr[0] == "a"
    assert arr[-1] == "c"
    
    arr[1] = "z"
    assert arr[1] == "z"

def test_prepend():
    arr = ArrayList()
    arr.append(2)
    arr.prepend(1)
    assert arr[0] == 1

def test_insert():
    arr = ArrayList()
    arr.push(1, 2, 3, 4)
    arr.insert(1, 99)
    assert arr[1] == 99
    assert len(arr) == 5
    
def test_pop():
    arr = ArrayList()
    arr.push(1, 2, 3, 4)
    val = arr.pop()
    assert val == 4
    assert len(arr) == 3

def test_delete():
    arr = ArrayList()
    arr.push(1, 2, 3, 4)
    arr.delete(0)
    assert arr[0] == 2
    assert len(arr) == 3

def test_remove():
    arr = ArrayList()
    arr.push(1, 2, 3, 3, 5)
    arr.remove(3)
    assert len(arr) == 3
    with pytest.raises(ValueError):
        arr.remove(6)

def test_index():
    arr = ArrayList()
    arr.push(1, 3, 2, 8, 6)
    assert arr.index(2) == 2
    
    assert arr.index(10) == -1
    
def test_index_error():
    arr = ArrayList()
    with pytest.raises(IndexError):
        _ = arr[0]
    
    with pytest.raises(IndexError):
        arr.pop()
    
    with pytest.raises(IndexError):
        arr.delete(0)
        
def test_clear():
    arr = ArrayList()
    arr.push(2, 3, 4, 5, 6)
    arr.clear()
    
    assert len(arr) == 0
    assert arr.get_capacity() == 8

def test_copy():
    arr = ArrayList()
    arr.push(1, 2, 3, 4, 5, 6, 7, 8)
    new_arr = arr.copy()
    assert arr == new_arr

def test_count():
    arr = ArrayList()
    arr.push(2, 3, 4, 4, 3, 2, 4)
    assert arr.count(4) == 3
    assert arr.count(8) == 0
    assert arr.count(3) == 2

def test_extend():
    arr = ArrayList()
    arr.push(1, 2, 3)
    arr.extend([4, 5, 6])
    assert len(arr) == 6
    
def test_bubble_sort():
    arr = ArrayList()
    sorted = ArrayList()
    sorted.push(-8, 0, 1, 2, 3, 4)
    arr.push(2, 4, 1, 3, -8, 0)
    arr.bubble_sort()
    assert arr == sorted

def test_insertion_sort():
    arr = ArrayList()
    sorted = ArrayList()
    sorted.push(-8, 0, 1, 2, 3, 4)
    arr.push(2, 4, 1, 3, -8, 0)
    arr.insertion_sort()
    assert arr == sorted

def test_selection_soot():
    arr = ArrayList()
    sorted = ArrayList()
    sorted.push(-8, 0, 1, 2, 3, 4)
    arr.push(2, 4, 1, 3, -8, 0)
    arr.selection_sort()
    assert arr == sorted
