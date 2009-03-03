; Kernal vectors for C128

MMU_REGS = $ff00 ; MMU register, visible in all banks

GO64 = $E24B ; Code to enter C64 mode

; Prefix "Kernal"
RAMTAS = $fd50 ; Perform RAM test and set pointers to top and bottom of RAM
RESTOR = $fd15 ; Restore RAM vectors for default I/O routines
IOINIT = $fda3 ; Initialize CIA I/O devices
CINT = $ff5b ; Initialize screen editor and VIC chip
BAS_TO_RAM = $e453 ; Copy BASIC vectors to RAM
INIT = $e3bf ; Initialize BASIC
; End Prefix

; Prefix "Vector"
SPIN_SPOUT = $ff47 ; Set serial ports for fast input or output
CLOSE_ALL  = $ff4a ; Close all files to a device
C64MODE    = $ff4d ; Enter 64 mode
DMA_CALL   = $ff50 ; Send command to DMA device
BOOT_CALL  = $ff53 ; Boot a program from disk
PHOENIX    = $ff56 ; Initialize fuction ROM cartridges
LKUPLA     = $ff59 ; Look up logical file number in file tables
LKUPSA     = $ff5c ; Look up secondary address in file tables
SWAPPER    = $ff5f ; Switch between 40- and 80- column displays
DLCHR      = $ff62 ; Initialize character set for 80-column display
PFKEY      = $ff65 ; Assign a string to a function key
SETBNK     = $ff68 ; Set banks for I/O operations
GETCFG     = $ff6b ; Get byte to configure MMU for any bank
JSRFAR     = $ff6e ; Jump to a subroutine in any bank, with return to the calling bank
JMPFAR     = $ff71 ; Jump to a routine in any bank, with no return to the calling bank
INDFET     = $ff74 ; Load a byte from an address (offset of Y) in any bank
INDSTA     = $ff77 ; Store a byte to an address (offset of Y) in any bank
INDCMP     = $ff7a ; Compare a byte to the contents of an address (offset of Y) in any bank
PRIMM      = $ff7d ; Print the string in memory immediately following the JSR to this routine

; Include C64 kernal table...
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
