#!/usr/bin/env python
import types
import unittest

def seqToString( seq, conjuction = 'and', default = (), separator = ',', whitespace = ' ' ):
    if not seq and default:
        seq = default

    if len(seq) == 0:
        return ''
    elif len(seq) == 1:
        return str(seq[0])
    elif len(seq) == 2:
        return str(seq[0]) + str(whitespace) + str(conjuction) + str(whitespace)  + str(seq[1])
    else:
        if type(seq) == types.TupleType:
            seq = [ item for item in seq ]

        seq[len(seq) - 1] = str(conjuction) + str(whitespace) + seq[len(seq) - 1]
        separator = separator + whitespace
        return separator.join( seq )

class TestSeqToString(unittest.TestCase):
    def verify( self, result, seq, conjuction = 'and', default = None, separator = ',', whitespace = ' ' ):
        s = seqToString( seq, conjuction, default, separator, whitespace )
        #print str(s)
        assert( s == result )

    def runTest( self ):
        ## Tuple
        # Various lengths
        self.verify( result = '', seq = () )
        self.verify( result = 'a', seq = ('a') )
        self.verify( result = 'a and b', seq = ('a', 'b') )
        self.verify( result = 'a, b, and c', seq = ('a', 'b', 'c') )
        self.verify( result = 'a, b, c, and d', seq = ('a', 'b', 'c', 'd') )

        # Default
        self.verify( result = 'a, b, c, and d', seq = None, default = ('a', 'b', 'c', 'd') )

        # Conjuction
        self.verify( result = 'a, b, c, or d', seq = ('a', 'b', 'c', 'd'), conjuction = 'or'  )

        # Seperator
        self.verify( result = 'a. b. c. and d', seq = ('a', 'b', 'c', 'd'), separator = '.'  )

        # Whitespace
        self.verify( result = 'a,_b,_c,_and_d', seq = ('a', 'b', 'c', 'd'), whitespace = '_'  )

        ## List
        self.verify( result = 'a, b, c, and d', seq = ['a', 'b', 'c', 'd'] )

        # Default
        self.verify( result = 'a, b, c, and d', seq = None, default = ['a', 'b', 'c', 'd'] )

if __name__ == "__main__":
    unittest.main()

