; Kernal vectors

; Prefix "Vector"
CINT    = $ff81 ; Initialize screen editor and video chip
IOINIT  = $ff84 ; Initialize I/O devices
RAMTAS  = $ff87 ; Initialize RAM, tape buffer, screen
RESTOR  = $ff8a ; Restore deafult I/O vectors
VECTOR  = $ff8d ; Read/set I/O vector table
SETMSG  = $ff90 ; Set Kernal message control flag
SECOND  = $ff93 ; Send secondary address after LISTEN
TKSA    = $ff96 ; Send secondary address after TALK
MEMTOP  = $ff99 ; Read/set top of memory pointer
MEMBOT  = $ff9c ; Read/set bottom of memory pointer
SCNKEY  = $ff9f ; Scan the keyboard
SETTMO  = $ffa2 ; Set time-out flag for IEEE bus
ACPTR   = $ffa5 ; Input byte from serial bus
CIOUT   = $ffa8 ; Output byte to serial bus
UNTLK   = $ffab ; Command serial bus device to UNTALK
UNLSN   = $ffae ; Command serial bus device to UNLISTEN
LISTEN  = $ffb1 ; Command serial bus device to LISTEN
TALK    = $ffb4 ; Command serial bus device to TALK
READST  = $ffb7 ; Read I/O status word
SETLFS  = $ffba ; Set logical file parameters
SETNAM  = $ffbd ; Set filename parameters
OPEN    = $ffc0 ; Open a logical file
CLOSE   = $ffc3 ; Close a logical file
CHKIN   = $ffc6 ; Define an input channel
CHKOUT  = $ffc9 ; Define an output channel
CLRCHN  = $ffcc ; Restore default devices
CHRIN   = $ffcf ; Input a character
CHROUT  = $ffd2 ; Output a character
LOAD    = $ffd5 ; Load (RAM) from a device
SAVE    = $ffd8 ; Save (RAM) to a device
SETTIM  = $ffdb ; Set the software clock
RDTIM   = $ffde ; Read the software clock
STOP    = $ffe1 ; Check the STOP key
GETIN   = $ffe4 ; Get a character (aka GETKEY)
CLALL   = $ffe7 ; Close all files
UDTIM   = $ffea ; Update the software clock
SCREEN  = $ffed ; Read the number of screen rows and columns
PLOT    = $fff0 ; Read/set the position of cursor on screen
IOBASE  = $fff3 ; Read the base address of I/O devices
; End Prefix
