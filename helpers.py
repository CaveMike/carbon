#!/usr/bin/env python
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
    return dict( [ (v,k) for k, v in d.iteritems() ] )

#-------------------------------------------------------------------------------
def sortDict( adict ):
    keys = adict.keys()
    keys.sort()
    return map(adict.get, keys)

if __name__ == '__main__':
    unittest.main()
