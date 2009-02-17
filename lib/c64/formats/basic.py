# Module for de-tokenizing C64 BASIC programs.
# http://www.atarimagazines.com/compute/issue70/088_1_Loading_And_Linking_Commodore_Programs.php

def split_words(d):
    return [x.split() for x in d.splitlines()]

class Basic(object):
    def __init__(self, bytes, has_header=True):
        """Initialize a Basic object from the given bytes."""
        
        # Skip the first two "program location" bytes if there is a header.
        # Might want to verify that they are $01,$80 -> $0801
        if has_header:
            self.bytes = bytes[2:]
        else:
            self.bytes = bytes

    def list(self):
        return ""

TOKENS = """
80	end
81	for
82	next
83	data
84	input#
85	input
86	dim
87	read
88	let
89	goto
8a	run
8b	if
8c	restore
8d	gosub
8e	return
8f	rem
90	stop
91	on
92	wait
93	load
94	save
95	verify
96	def
97	poke
98	print#
99	print
9a	cont
9b	list
9c	clr
9d	cmd
9e	sys
9f	open
a0	close
a1	get
a2	new
a3	tab(
a4	to
a5	fn
a6	spc(
a7	then
a8	not
a9	step
aa	+
ab	-
ac	*
ad	/
ae	^
af	and
b0	or
b1	>
b2	=
b3	<
b4	sgn
b5	int
b6	abs
b7	usr
b8	fre
b9	pos
ba	sqr
bb	rnd
bc	log
bd	exp
be	cos
bf	sin
c0	tan
c1	atn
c2	peek
c3	len
c4	str$
c5	val
c6	asc
c7	chr$
c8	left$
c9	right$
ca	mid$
cb	go
ff	pi
""".strip()

TOKEN_MAP = dict( (int(x[0],16), x[1]) for x in split_words(TOKENS) )
print TOKEN_MAP
