from main import get_intersection
from main import is_intersecting

def test_same():
    # same rectangle should be the intersection
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
    )

def test_back():
    # expanding one of the rectangles up/down/left/right/forward/back should
    # return the smaller rectangle
    assert (
        get_intersection(
            ('off', -12, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -12, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )

    assert (
        is_intersecting(
            ('off', -12, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),   
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -12, 10, -10, 10, -10, 10),   
        )
    )

def test_forward():
    assert (
        get_intersection(
            ('off', -10, 12, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 12, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 12, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 12, -10, 10, -10, 10),    
        )
    )

def test_down():
    assert (
        get_intersection(
            ('off', -10, 10, -12, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -12, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -12, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -12, 10, -10, 10),   
        )
    )

def test_up():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 12, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 12, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 12, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 10), 
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 12, -10, 10),   
        )
    )

def test_left():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -12, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -12, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -12, 10), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -12, 10),  
        )
    )

def test_right():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 12), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 12),  
        )
        ==  ('on',  -10, 10, -10, 10, -10, 10)   
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 12), 
            ('on',  -10, 10, -10, 10, -10, 10),  
        )
    )
    assert (
        is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, -10, 12),   
        )
    )

def test_in_front():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  11, 21, -10, 10, -10, 10),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  11, 21, -10, 10, -10, 10),  
        )
    )

def test_behind():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -21, -11, -10, 10, -10, 10),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -21, -11, -10, 10, -10, 10),   
        )
    )

def test_above():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, 11, 21, -10, 10),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, 11, 21, -10, 10), 
        )
    )

def test_below():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -21, -11, -10, 10),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -21, -11, -10, 10),  
        )
    )

def test_to_the_right():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, 11, 21),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, 11, 21),  
        )
    )

def test_to_the_left():
    assert (
        get_intersection(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, 11, 21),  
        )
        ==  None   
    )
    assert (
        not is_intersecting(
            ('off', -10, 10, -10, 10, -10, 10), 
            ('on',  -10, 10, -10, 10, 11, 21),  
        )
    )