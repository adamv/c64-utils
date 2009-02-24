def format_bytes(bytes, bytes_per_line=32):
    rows = list()
    
    row = list()
    for i, x in enumerate(bytes):
        row.append("%02x" % ord(x))

        if (i+1) % bytes_per_line == 0:
            rows.append(' '.join(row))
            row = list()
    
    if row:
        rows.append(' '.join(row))
        
    return '\n'.join(rows)
