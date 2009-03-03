# Demonstrate disassembly of a bootsector.
python -m gdis -i bootsector.prg --bootsector --data="[['0B77', 5, 'Filename'], ['0B27', 9, 'Unknown']]" --symbols kernal-128 ports wasteboot.s --comments="[['0b14', 'Relocate code from the boot-sector to 0x8000, to run after GO64.'], ['0B5E', 'Load filename from relocated address.']]"
