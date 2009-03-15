"""Code to handle conversions of bytes to PETSCII codes.

http://en.wikipedia.org/wiki/PETSCII
"""
__all__ = ['quote_petscii', 'petscii_str']

# Map of various CBM control codes to names.
CONTROL_MAP = {
      5: "{white}",
     14: "{lowercase}",
     17: "{down}",
     18: "{rvson}",
     19: "{home}",
     20: "{delete}",
     28: "{red}",
     29: "{right}",
     30: "{green}",
     31: "{blue}",
     92: "{pound}",
     94: "{uparr}",
     95: "{leftarr}",
    126: "{pi}",
    129: "{orange}",
    133: "{F1}",
    134: "{F3}",
    135: "{F5}",
    136: "{F7}",
    137: "{F2}",
    138: "{F4}",
    139: "{F6}",
    140: "{F8}",
    141: "{shift-enter}",
    142: "{uppercase}",
    144: "{black}",
    145: "{up}",
    146: "{rvsoff}",
    147: "{clr}",
    148: "{ins}",
    149: "{brown}",
    150: "{lred}",
    151: "{grey1}",
    152: "{grey2}",
    153: "{lgreen}",
    154: "{lblue}",
    155: "{grey3}",
    156: "{purple}",
    157: "{left}",
    158: "{yellow}",
    159: "{cyan}",
    160: "{shift-space}",
}

def quote_petscii(c):
    if not isinstance(c, int):
        c = ord(c)
    
    if 32 <= c <= 95:
        return chr(c)
    else:
        return CONTROL_MAP.get(c, "{$%02x}" % (c))

def petscii_str(s):
    return ''.join(quote_petscii(ord(c)) for c in s)
