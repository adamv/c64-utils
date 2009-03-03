# Demonstrate disassembly of a bootsector.
python -m gdis -i bootsector.prg --bootsector --data="[['0B68', 5, 'Filename']]" --symbols kernal-128 ports
