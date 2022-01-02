from main import split_cubes

def test_only_intersection():
    a = ('on',  -10, 10, -10, 10, -10, 10)
    b = ('off', -10, 10, -10, 10, -10, 10)
    (intersection, a_split, b_split) = split_cubes(a,b)

    assert intersection == ('off', -10, 10, -10, 10, -10, 10)
    assert len(a_split) == 0
    assert len(b_split) == 0
