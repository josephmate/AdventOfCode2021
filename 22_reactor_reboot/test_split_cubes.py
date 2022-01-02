from main import split_cubes

def test_only_intersection():
    a = ('on',  -10, 10, -10, 10, -10, 10)
    b = ('off', -10, 10, -10, 10, -10, 10)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off', -10, 10, -10, 10, -10, 10)
    assert a_split == []
    assert b_split == []


def test_only_above_and_below():
    a = ('on',  -10, 10,   0, 20, -10, 10)
    b = ('off', -10, 10, -20,  0, -10, 10)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off', -10, 10,   0,  0, -10, 10)
    assert a_split == [    ('on',  -10, 10,   1, 20, -10, 10)]
    assert b_split == [    ('off', -10, 10, -20, -1, -10, 10)]

def test_only_left_and_right():
    a = ('on',  -10, 10, -10, 10, 0, 20)
    b = ('off', -10, 10, -10, 10, -20, 0)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off', -10, 10, -10, 10,   0,  0)
    assert a_split == [    ('on',  -10, 10, -10, 10,   1, 20)]
    assert b_split == [    ('off', -10, 10, -10, 10, -20, -1)]


def test_only_forwards_and_backwards():
    a = ('on',  0, 20, -10, 10, -10, 10)
    b = ('off', -20, 0, -10, 10, -10, 10)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off',   0,  0, -10, 10, -10, 10)
    assert a_split == [    ('on',    1, 20, -10, 10, -10, 10)]
    assert b_split == [    ('off', -20, -1, -10, 10, -10, 10)]

def test_b_inside_a():
    a = ('on',  -10, 10, -10, 10, -10, 10)
    b = ('off', -9, 9, -9, 9, -9, 9)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off',   -9, 9, -9, 9, -9, 9)
    assert a_split == [
        ('on', -10, 10,  10,  10, -10,  10), # above
        ('on', -10, 10, -10, -10, -10,  10), # below
        ('on', -10, 10, -9,  9,  -10, -10), # left
        ('on', -10, 10, -9,  9,   10,  10), # right
        ('on', 10, 10, -9,  9,  -9,  9), # forward
        ('on', -10, -10, -9,  9,  -9,  9), # back
    ]
    assert b_split == []

def test_a_inside_b():
    a = ('off', -9, 9, -9, 9, -9, 9)
    b = ('on',  -10, 10, -10, 10, -10, 10)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('on',   -9, 9, -9, 9, -9, 9)
    assert a_split == []
    assert b_split == [
        ('on', -10, 10,  10,  10, -10,  10), # above
        ('on', -10, 10, -10, -10, -10,  10), # below
        ('on', -10, 10, -9,  9,  -10, -10), # left
        ('on', -10, 10, -9,  9,   10,  10), # right
        ('on', 10, 10, -9,  9,  -9,  9), # forward
        ('on', -10, -10, -9,  9,  -9,  9), # back
    ]