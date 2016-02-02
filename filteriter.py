#!/usr/bin/env python

class filteriter:
    def __init__( self, filter, obj ):
        self.filter = filter
        self.get = iter( obj ).next

    def __iter__( self ):
        return self

    def next( self ):
        while 1:
            obj = self.get()
            if self.filter( obj ):
                return obj

