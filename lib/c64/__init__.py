
def struct_doc(format):
    return ''.join(x.partition('#')[0].strip() for x in format.splitlines())
