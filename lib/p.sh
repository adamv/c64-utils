# Demonstrate disassembly of a mixed BASIC/ML program.
python -m gdis -b --symbols kernal-table ports p.s -i PRODOS.prg --offset 23 --data="[['02D3', 3, 'Filename']]" --comments="[['02f5', 'Set memory configuration.'], ['02fd', 'Continue with 2.0.'], ['02d6', 'BASIC will automatically start executing here after LOAD as part of the READY routine.']]"
