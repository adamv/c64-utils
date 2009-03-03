# Demonstrate disassembly of a bootsector.
python -m gdis -i bootsector.prg --bootsector --data="[['C868', 5, 'Filename']]" --symbols kernal-table ports
