#!/usr/bin/env python3

#-------------------------------------------------------------------------------
def makeIdentifier( rawIdentifier, replacement = '' ):
    #FIXME: I assume there is a better way to do this.
    s = []

    for c in rawIdentifier:
        if ( c == '_' ) or ( c >= 'a' and c <= 'z' ) or ( c >= 'A' and c <= 'Z' ) or ( c >= '0' and c <= '9' ):
            s += c
        else:
            s += replacement

    return ''.join(s)

#-------------------------------------------------------------------------------
def importName( moduleName, name, log = None ):
    if log:
        log.info( 'Trying to import module: ' + moduleName + ', name: ' + name + '.' )

    try:
        module = __import__( moduleName, globals(), locals(), [name] )
    except ImportError as e:
        if log:
            log.info( 'Failed to import module: ' + moduleName + ', name: ' + name + '.' )
        return None

    if hasattr( module, name ):
        if log:
            log.info( 'Importing module: ' + moduleName + ', name: ' + name + '.' )
        return getattr( module, name )

    return None

#-------------------------------------------------------------------------------
def importExtension( extensionName, modulePrefix = None ):
    # Covert the extensionName so that it only includes validate characters.
    extensionName = extensionName.replace( '/', '_' )
    extensionName = extensionName.replace( '-', '_' )
    extensionName = extensionName.replace( '+', '_' )

    # Convert the moduleName so that it fits the convention.
    moduleName = extensionName.lower()
    if modulePrefix:
        moduleName = modulePrefix + '.' + moduleName

    # Convert the object name so that it fits the convention.
    name = extensionName
    name = name.replace( '_', ' ' )
    name = name.title()
    name = name.replace( ' ', '' )

    return importName( moduleName, name )

