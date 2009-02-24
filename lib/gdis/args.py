"Command-line argument support for gdis."
__all__ = ['parse_args']

from optparse import OptionParser

def floatable(str):
    "Test if the given string can be converted to a float."
    try:
        float(str)
        return True
    except ValueError:
        return False

def vararg_callback(option, opt_str, value, parser):
    "Support for option with 1 or more arguments (from optparse docs)"
    assert value is None
    value = list()

    for arg in parser.rargs:
        # stop on --foo like options
        if arg[:2] == "--" and len(arg) > 2:
            break
        # stop on -a, but not on -3 or -3.0
        if arg[:1] == "-" and len(arg) > 1 and not floatable(arg):
            break
        value.append(arg)

    del parser.rargs[:len(value)]
    setattr(parser.values, option.dest, value)

def parse_args():
    p = OptionParser()
    op = p.add_option

    op('-i', '--input', action='store', dest='input_filename')
    op('-a', '--addr', action='store', dest='address', default=None,
        help='Provide a load address, overriding one in the header if used.')
        
    op('-n', '--noheader', action='store_false', dest='use_header_address',
        help='Input file has no 2 byte load address header.')
        
    op('-b', '--basic', action='store_true', dest='basic_header',
        help='Try to parse a BASIC program header before ML.')
        
    op('-o', '--offset', type='int', dest='offset', default=0,
        help='Offset at which to start disassembly.')
        
    op('-d', '--data', default=None,
        help='A Python list of tuples that defines data blocks; will be moved to a config file format.')
        
    op('-c', '--comments', default=None,
        help='A Python list of ("address", "comment") tuples; will be moved to a config file format.')
    
    op('-s', '--symbols', dest='symbol_files', action='callback', callback=vararg_callback, default=())

    return p.parse_args()    
