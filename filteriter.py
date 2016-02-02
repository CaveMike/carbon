#!/usr/bin/env python3

class filteriter:
    def __init__( self, filter, obj ):
        self.filter = filter
        self.get = iter( obj ).__next__

    def __iter__( self ):
        return self

    def __next__( self ):
        while 1:
            obj = self.get()
            if self.filter( obj ):
                return obj

