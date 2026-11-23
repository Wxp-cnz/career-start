import ex07_fibonacci


def test_first_five():
    assert ex07_fibonacci.fibonacci_list(5) == [1, 1, 2, 3, 5]
    
def test_len_twenty():
    assert len(ex07_fibonacci.fibonacci_list(20)) == 20

def test_last_two():
    assert ex07_fibonacci.fibonacci_list(20)[-2:] == [4181,6765]
def test_return_one():
    assert ex07_fibonacci.fibonacci_list(1) == [1]