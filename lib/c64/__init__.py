
def blocks(bytes, block_size, offset=0, max=0):
    i = offset
    found = 0
    while i < len(bytes) and (not max or found<max):
        yield bytes[i:i+block_size]
        found += 1
        i += block_size

def struct_doc(format):
    return ''.join(x.partition('#')[0].strip() for x in format.splitlines())
