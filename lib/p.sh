# Demonstrate disassembly of a mixed BASIC/ML program.
python -m gdis -b --symbols kernal-table ports p.s -i PRODOS.prg --offset 23 --data="[['02D3', 3, 'Filename']]"
