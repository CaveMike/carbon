#!/usr/bin/env python
"""
Enumeration allows users to define a set of integers, alias these integers with
strings, and then use the Enumeration interchangeably with integers, strings,
and other values from the Enumeration.  Additionally, users may derived from the
Enumeration class and add additional methods.

Users that want to create an Enumeration, import the following:
    from enumeration import Enumeration

Users that want to derive and extend an Enumeration might want to import:
    from enumeration import Enumeration
    from enumeration import EnumException
    from enumeration import EnumItem

Heavily based on implementations by Will Ware, Michael Radziej, and Martin Miller at
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/67107
I started with the implementation by Will Ware.  Then incorporated the fixes
and feedback from Martin Miller.  Next I added most of the additional functionality
that Michael Radziej added.  Finally, I tweaked the implementation based on my own
experiences using the class.

Developed and tested using:
Python 2.5.1 (r251:54863, Apr 18 2007, 08:51:08) [MSC v.1310 32 bit (Intel)] on win32
"""
import unittest
import types

#===============================================================================
class EnumException(Exception): pass

#===============================================================================
class EnumItem(object):
    """
    EnumItems are simply a pair of items: a string and an int.  This class
    can be converted to a string or integer using the str() and int() methods
    respectively.

    TODO: Do __lt__(), __le__(), __gt__(), and __ge__() need to be implemented
    or are these derived from __cmp__()?
    """
    def __init__( self, enumeration, name, value ):
        self.name = name
        self.value = value

    def __cmp__( self, other ):
        # Convert the other parameter to an int.
        if type(other) == types.StringType:
            return cmp( self.name, other )
        elif type(other) == types.IntType:
            return cmp( self.value, other )
        elif type(other) == EnumItem:
            return cmp( self.value, other.value )
        else:
            return None
            #raise EnumException( 'Cannot compare with type, ' + str(type(other)) + '.' )

    def __eq__( self, other ):
        return self.__cmp__( other ) == 0

    def __ne__( self, other ):
        return self.__cmp__( other ) != 0

    def __nonzero__( self ):
        return True

    def __hash__(self):
        return self.value

    def __int__( self ):
        return self.value

    def __str__( self ):
        return self.name

    def __repr__( self ):
        return self.__str__()

#===============================================================================
class Enumeration(object):
    """
    This implementation is a double-dictionary where one dictionary
    correlates strings to integers and the other correlates integers to strings.
    The dictionaries return EnumItem objects which can be used transparently as either
    Strings or Ints.
    """
    def __init__( self, enumList, firstValue = 0 ):
        super( Enumeration, self ).__init__()
        self.nextUniqueValue = firstValue
        self.nameToValue = {}
        self.valueToName = {}

        try:
            # If the enumList is a string, then split it up into a list.
            if type(enumList) == types.StringType:
                enumList = enumList.split()

            # First, iterate for the entires that have both names and values.
            for item in enumList:
                if type(item) == types.TupleType:
                    # If the entry is a tuple, then it is a name followed by a value.
                    name, value = item
                    self.addItem( name, value )

            # Then, iterate for the rest of the entries and assign them unique values.
            for item in enumList:
                if type(item) != types.TupleType:
                    value = self.generateUniqueValue()
                    self.addItem( item, value )

        except EnumException:
            self.nextUniqueValue = None
            self.nameToValue = None
            self.valueToName = None
            raise

    def addItem( self, name, value ):
        # Validate input parameters.
        if type(name) != types.StringType:
            raise EnumException( 'The enumeration name, ' + str(name) + ', is not a string.' )

        if type(value) != types.IntType:
            raise EnumException( 'The enumeration value, ' + str(value) + ', for name, ' + str(name) + ', is not an integer.' )

        if name in self.nameToValue:
            raise EnumException( 'The enumeration name, ' + str(name) + ', is not unique.' )

        if value in self.valueToName:
            raise EnumException( 'The enumeration value, ' + str(value) + ', for name, ' + str(name) + ', is not unique.' )

        item = EnumItem( self, name, value )
        self.nameToValue[name] = item
        self.valueToName[value] = item

    def generateUniqueValue( self ):
        # Find the next available value.
        while self.nextUniqueValue in self.valueToName:
            self.nextUniqueValue += 1

        n = self.nextUniqueValue
        self.nextUniqueValue += 1
        return n

    def fromInt( self, value ):
        return self.valueToName[value]

    def fromStr( self, name, exact = False ):
        """ fromStr() attempts first to find an enumeration with the extact string, name.

            If that fails, and the exact parameter is true, then fromStr() attempts to
            find an enumeration that starts with the string, name, when compared without
            case-sensitivity.  This additional search is useful when convering user-input
            to enumerations.
        """
        if self.nameToValue.has_key( name ):
            return self.nameToValue[name]
        elif not exact:
            for item in self.nameToValue.iterkeys():
                # Do a case-insensitive string comparison.
                n = item.lower().find( name.lower() )

                # If the parameter is the start of the item, then return the item.
                if n == 0:
                    return self.nameToValue[item]

        raise EnumException( 'Cannot match, ' + str(name) + ', with one of ' + str([ str(key) for key in self.nameToValue.iterkeys()]) + '.' )

    def __len__( self ):
        return len(self.nameToValue)

    def __contains__( self, key ):
        if type(key) == types.StringType:
            return key in self.nameToValue
        elif type(key) == types.IntType:
            return key in self.valueToName
        elif type(key) == EnumItem:
            return key.value in self.valueToName
        else:
            raise EnumException( 'Invalid key, ' + str(key) + ', of type, ' + str(type(key)) + ', used in __contains__.' )

    def __getattr__( self, name ):
        if not self.nameToValue.has_key(name):
            raise AttributeError( 'Name, ' + str(name) + ', not found in enumeration.' )

        return self.nameToValue[name]

    def __getitem__( self, key ):
        if type(key) == types.StringType:
            return self.nameToValue[key]
        else:
            return self.valueToName[key]

    def __iter__( self ):
        for item in self.nameToValue.iteritems():
            yield item

    def iterkeys( self ):
        for name in self.nameToValue.iterkeys():
            yield name

    def itervalues( self ):
        for value in self.nameToValue.itervalues():
            yield value

    def irange( self, begin, end ):
        if type(begin) == types.StringType:
            begin = self.nameToValue[begin]

        if type(end) == types.StringType:
            end = self.nameToValue[end]

        return [ self.valueToName[i] for i in range( int(begin), int(end) + 1 ) ]

    def __str__( self ):
        return ', '.join( [ str(name) for name in self.nameToValue.iterkeys() ] )

    def __repr__( self ):
        return ', '.join( [ str(name) + ':' + str(value) for (name, value) in self.nameToValue.iteritems() ] )

#===============================================================================
class TestEnumeration(unittest.TestCase):
    def verifyEntry( self, enumeration, name, value ):
        assert( enumeration.fromStr( name ) == name )
        assert( enumeration.fromStr( name ) == value )

        # Use just the first few characters to find the string, then compare.
        assert( enumeration.fromStr( name[:4] ) == name )
        assert( enumeration.fromStr( name[:4] ) == value )

        # Make sure the comparison is case-insensitive.
        assert( enumeration.fromStr( name.lower() ) == name )
        assert( enumeration.fromStr( name.upper() ) == value )

        assert( enumeration.fromInt( value ) == name )
        assert( enumeration.fromInt( value ) == value )

        assert( enumeration[name] == value )
        assert( enumeration[value] == name )

        assert( value == enumeration[name] )
        assert( name == enumeration[value] )

        assert( name in enumeration )
        assert( value in enumeration )

    def runTest( self ):
        Insect = Enumeration( 'ANT APHID BEE BEETLE BUTTERFLY MOTH HOUSEFLY WASP CICADA GRASSHOPPER COCKROACH DRAGONFLY', 100 )

        assert( len(Insect) == 12 )

        assert( Insect.ANT         == 100 )
        assert( Insect.APHID       == 101 )
        assert( Insect.BEE         == 102 )
        assert( Insect.BEETLE      == 103 )
        assert( Insect.BUTTERFLY   == 104 )
        assert( Insect.MOTH        == 105 )
        assert( Insect.HOUSEFLY    == 106 )
        assert( Insect.WASP        == 107 )
        assert( Insect.CICADA      == 108 )
        assert( Insect.GRASSHOPPER == 109 )
        assert( Insect.COCKROACH   == 110 )
        assert( Insect.DRAGONFLY   == 111 )

        assert( len( Insect.irange( 'ANT', 'ANT'       ) ) == 1  )
        assert( len( Insect.irange( 'ANT', 'HOUSEFLY'  ) ) == 7  )
        assert( len( Insect.irange( 'ANT', 'DRAGONFLY' ) ) == 12 )

        assert( len( Insect.irange( 100, 100 ) ) == 1  )
        assert( len( Insect.irange( 100, 103 ) ) == 4  )
        assert( len( Insect.irange( 100, 111 ) ) == 12 )

        #print str(Insect)
        assert( str(Insect) )

        #print repr(Insect)
        assert( repr(Insect) )

        #for (name, value) in Insect:
        #   print name, value

        #for name in Insect.iterkeys():
        #   print name

        #for value in Insect.itervalues():
        #   print value


        self.verifyEntry( Insect, 'ANT',         100 )
        self.verifyEntry( Insect, 'APHID',       101 )
        self.verifyEntry( Insect, 'BEE',         102 )
        self.verifyEntry( Insect, 'BEETLE',      103 )
        self.verifyEntry( Insect, 'BUTTERFLY',   104 )
        self.verifyEntry( Insect, 'MOTH',        105 )
        self.verifyEntry( Insect, 'HOUSEFLY',    106 )
        self.verifyEntry( Insect, 'WASP',        107 )
        self.verifyEntry( Insect, 'CICADA',      108 )
        self.verifyEntry( Insect, 'GRASSHOPPER', 109 )
        self.verifyEntry( Insect, 'COCKROACH',   110 )
        self.verifyEntry( Insect, 'DRAGONFLY',   111 )

        Volkswagen = Enumeration( [
            'JETTA',
            'RABBIT',
            'BEETLE',
            ('THING', 400),
            'PASSAT',
            'GOLF',
            ('CABRIO', 700),
            ('EURO_VAN', 1),
            'CLASSIC_BEETLE',
        ] )

        assert( len(Volkswagen) == 9 )

        assert( Volkswagen.JETTA          == 0   )
        assert( Volkswagen.RABBIT         == 2   )
        assert( Volkswagen.BEETLE         == 3   )
        assert( Volkswagen.THING          == 400 )
        assert( Volkswagen.PASSAT         == 4   )
        assert( Volkswagen.GOLF           == 5   )
        assert( Volkswagen.CABRIO         == 700 )
        assert( Volkswagen.EURO_VAN       == 1   )
        assert( Volkswagen.CLASSIC_BEETLE == 6   )

        self.verifyEntry( Volkswagen, 'JETTA',          0   )
        self.verifyEntry( Volkswagen, 'RABBIT',         2   )
        self.verifyEntry( Volkswagen, 'BEETLE',         3   )
        self.verifyEntry( Volkswagen, 'THING',          400 )
        self.verifyEntry( Volkswagen, 'PASSAT',         4   )
        self.verifyEntry( Volkswagen, 'GOLF',           5   )
        self.verifyEntry( Volkswagen, 'CABRIO',         700 )
        self.verifyEntry( Volkswagen, 'EURO_VAN',       1   )
        self.verifyEntry( Volkswagen, 'CLASSIC_BEETLE', 6   )

        #print str(Volkswagen)
        assert( str(Volkswagen) )

        #print repr(Volkswagen)
        assert( repr(Volkswagen) )

        #for (name, value) in Volkswagen:
        #   print name, value

        #for name in Volkswagen.iterkeys():
        #   print name

        #for value in Volkswagen.itervalues():
        #   print value

if __name__ == '__main__':
    unittest.main()

