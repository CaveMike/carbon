#!/usr/bin/env python3
import math
import unittest

#-------------------------------------------------------------------------------
def is_sequence( arg ):
    return not hasattr(arg, 'strip') and hasattr(arg, '__getitem__') and hasattr(arg, '__iter__')

class TestIsSeq(unittest.TestCase):
    def test_string(self):
        self.assertFalse(is_sequence('test'))

    def test_tuple_string(self):
        self.assertTrue(is_sequence(('test', )))

    def test_tuple_strings(self):
        self.assertTrue(is_sequence(('test0', 'test1')))

    def test_list_string(self):
        self.assertTrue(is_sequence(['test', ]))

    def test_list_strings(self):
        self.assertTrue(is_sequence(['test0', 'test1']))

#-------------------------------------------------------------------------------
def is_sequence_or_set( arg ):
    return isinstance(arg, set) or is_sequence(arg)

class TestIsSeqOrSet(unittest.TestCase):
    def test_set_string(self):
        self.assertTrue(is_sequence_or_set(set('test', )))

    def test_set_strings(self):
        self.assertTrue(is_sequence_or_set(set(('test0', 'test1'))))

#-------------------------------------------------------------------------------
def getCaller():
    try:
        import inspect
        return inspect.stack()[2][0].f_locals['self']
    except:
        pass

    return None

#-------------------------------------------------------------------------------
def curry( f, *a, **kw ):
    """ From Python Cookbook, Second Edition, 2005, Section 16.4 """
    def curried( *more_a, **more_kw ):
        combined_kw = kw.copy()
        combined_kw.update( more_kw )
        return f( *(a + more_a), **combined_kw )
    return curried

#-------------------------------------------------------------------------------
def nestedproperty( c ):
    return c()

#-------------------------------------------------------------------------------
def containsAny( seq, aset ):
    for c in seq:
        if c in aset:
            return True
    return False

#-------------------------------------------------------------------------------
def containsWhitespace( s ):
    #return containsAny( s, [ ' ', '\t', '\r', '\n' ] )
    for c in s:
        if c in [ ' ', '\t', '\r', '\n' ]:
            return True
    return False

#-------------------------------------------------------------------------------
def invertDict( d ):
    return dict( [ (v,k) for k, v in d.items() ] )

#-------------------------------------------------------------------------------
def sortDict( adict ):
    keys = list(adict.keys())
    keys.sort()
    return list(map(adict.get, keys))

def always_true(*args, **kwargs):
    return True

def always_false(*args, **kwargs):
    return False

def always_constant(value, *args, **kwargs):
    return value

def to_func_list(*args):
    l = []

    # Add scalars or sequences.
    for arg in args:
        if is_sequence_or_set(arg):
            l.extend(arg)
        else:
            l.append(arg)

    # Make sure each item is a function.
    for i in range(0, len(l)):
        item = l[i]
        if not hasattr(item, '__call__'):
            l[i] = curry(always_constant, item)

    return l

class TestToFuncList(unittest.TestCase):
    def testEmpty(self):
        l = to_func_list()
        self.assertFalse(l)
        self.assertFalse(len(l))

    def testOneScalar(self):
        l = to_func_list(13)
        self.assertTrue(l)
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0](), 13)

    def testThreeScalars(self):
        l = to_func_list(13, 14, 15)
        self.assertTrue(l)
        self.assertEqual(len(l), 3)
        self.assertEqual(l[0](), 13)
        self.assertEqual(l[1](), 14)
        self.assertEqual(l[2](), 15)

    def testThreeLists(self):
        l = to_func_list([13, 14, 15], [16], [17, 18, 19, 20])
        self.assertTrue(l)
        self.assertEqual([f() for f in l], [13, 14, 15, 16, 17, 18, 19, 20])

    def testThreeMixed(self):
        l = to_func_list([13, 14, 15], 16, [17, 18, 19, 20])
        self.assertTrue(l)
        self.assertEqual([f() for f in l], [13, 14, 15, 16, 17, 18, 19, 20])

    def testThreeMixedWithParams(self):
        l = to_func_list([13, 14, 15], 16, [17, 18, 19, 20])
        self.assertTrue(l)
        self.assertEqual([f(1, 2, 3, d=4, e=5, f=6) for f in l], [13, 14, 15, 16, 17, 18, 19, 20])

class frange(object):
    def __init__(self, start, stop, step=1.0):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += self.step

def in_range(value, range):
    if range.start > value:
        return False

    if range.stop == math.inf:
        return True

    if range.stop <= value:
        return False

    # TODO: step is not checked if self.count == math.inf
    if (value - range.start) % range.step != 0:
        return False

    return True

if __name__ == '__main__':
    unittest.main()
