"This module contains a mapping for CBM Basic 2.0 tokens."
__all__ = ['TOKEN_MAP', 'CONTROL_MAP']

# http://www.viceteam.org/plain/cbm_basic_tokens.txt

def split_words(d):
    return [x.split() for x in d.splitlines()]

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


CONTROL_MAP = {
      5: "{white}",
     14: "{lower}",
     17: "{down}",
     18: "{rvson}",
     19: "{home}",
     20: "{delete}",
     28: "{red}",
     29: "{right}",
     30: "{green}",
     31: "{blue}",
    129: "{orange}",
    133: "{F1}",
    134: "{F3}",
    135: "{F5}",
    136: "{F7}",
    137: "{F2}",
    138: "{F4}",
    139: "{F6}",
    140: "{F8}",
    142: "{upper}",
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
    159: "{cyan}"
}	
