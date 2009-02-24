# Demonstrate disassembly of a mixed BASIC/ML program.
python -m gdis -b --symbols kernal-table ports -i PRODOS.prg --offset 23 --data="[['02D5', 3, 'Filename']]"
