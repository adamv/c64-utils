; I/O ports

; VIC-II
; Prefix "VIC"
SP0X    = $D000 ; Sprite 0 Horizontal Position
SP0Y    = $D001 ; Sprite 0 Vertical Position
SP1X    = $D002 ; Sprite 1 Horizontal Position
SP1Y    = $D003 ; Sprite 1 Vertical Position
SP2X    = $D004 ; Sprite 2 Horizontal Position
SP2Y    = $D005 ; Sprite 2 Vertical Position
SP3X    = $D006 ; Sprite 3 Horizontal Position
SP3Y    = $D007 ; Sprite 3 Vertical Position
SP4X    = $D008 ; Sprite 4 Horizontal Position
SP4Y    = $D009 ; Sprite 4 Vertical Position
SP5X    = $D00a ; Sprite 5 Horizontal Position
SP5Y    = $D00b ; Sprite 5 Vertical Position
SP6X    = $D00c ; Sprite 6 Horizontal Position
SP6Y    = $D00d ; Sprite 6 Vertical Position
SP7X    = $D00e ; Sprite 7 Horizontal Position
SP7Y    = $D00f ; Sprite 7 Vertical Position
MSIGX   = $D010 ; Most Significant Bits of Sprite Horizontal Positions
SCROLY  = $D011 ; Vertical Fine Scrolling and Control Register
RASTER  = $D012 ; Read Current Raster Scan Line / Write Line to Compare for Raster IRQ
LPENX   = $D013 ; Light Pen Horizontal Position
LPENY   = $D014 ; Light Pen Vertical Position
SPENA   = $D015 ; Sprite Enable Register
SCROLX  = $D016 ; Horizontal Fine Scrolling and Control Register
YXPAND  = $D017 ; Sprite Vertical Expansion Register
VMCSB   = $D018 ; VIC-II Chip Memory Control Register
VICIRQ  = $D019 ; VIC Interrupt Flag Register
IRQMASK = $D01A ; IRQ Mask Register
SPBGPR  = $D01B ; Sprite-to-Foreground Display Priority Register
SPMC    = $D01C ; Sprite Multicolor Registers
XXPAND  = $D01D ; Sprite Horizontal Expansion Register
SPSPCL  = $D01E ; Sprite-to-Sprite Collision Register
SPBGCL  = $D01F ; Sprite-to-Foreground Collision Register
EXTCOL  = $D020 ; Border Color
BGCOL0  = $D021 ; Background Color 0
BGCOL1  = $D022 ; Background Color 1
BGCOL2  = $D023 ; Background Color 2
BGCOL3  = $D024 ; Background Color 3
SPMC0   = $D025 ; Sprite Multicolor Register 0
SPMC1   = $D026 ; Sprite Multicolor Register 1
SP0COL  = $D027 ; Sprite 0 Color
SP1COL  = $D028 ; Sprite 1 Color
SP2COL  = $D029 ; Sprite 2 Color
SP3COL  = $D02A ; Sprite 3 Color
SP4COL  = $D02B ; Sprite 4 Color
SP5COL  = $D02C ; Sprite 5 Color
SP6COL  = $D02D ; Sprite 6 Color
SP7COL  = $D02E ; Sprite 7 Color
; End Prefix

; CIA #1
; Prefix "CIA1"
CIAPRA  = $DC00 ; Data Port Register A
CIAPRB  = $DC01 ; Data Port Register B
CIDDRA  = $DC02 ; Data Direction Register A
CIDDRB  = $DC03 ; Data Direction Register B
TMALO   = $DC04 ; Timer A low byte
TMAHI   = $DC05 ; Timer A high byte
TMBLO   = $DC06 ; Timer B low byte
TMBHI   = $DC07 ; Timer B high byte
TODTEN  = $DC08 ; Time of Day Clock: 10ths of Seconds
TODSEC  = $DC09 ; Time of Day Clock: Seconds
TODMIN  = $DC0A ; Time of Day Clock: Minutes
TODHRS  = $DC0B ; Time of Day Clock: Hours
CIASDR  = $DC0C ; Serial Data Port
CIAICR  = $DC0D ; Interrupt Control Register
CIACRA  = $DC0E ; Control Register A
CIACRB  = $DC0F ; Control Register B
; End Prefix


; CIA #2
; Prefix "CIA2"
CI2PRA  = $DD00 ; Data Port Register A
CI2PRB  = $DD01 ; Data Port Register B
C2DDRA  = $DD02 ; Data Direction Register A
C2DDRB  = $DD03 ; Data Direction Register B
TI2ALO  = $DD04 ; Timer A low byte
TI2AHI  = $DD05 ; Timer A high byte
TI2BLO  = $DD06 ; Timer B low byte
TI2BHI  = $DD07 ; Timer B high byte
TO2TEN  = $DD08 ; Time of Day Clock: 10ths of Seconds
TO2SEC  = $DD09 ; Time of Day Clock: Seconds
TO2MIN  = $DD0A ; Time of Day Clock: Minutes
TO2HRS  = $DD0B ; Time of Day Clock: Hours
CI2SDR  = $DD0C ; Serial Data Port
CI2ICR  = $DD0D ; Interrupt Control Register
CI2CRA  = $DD0E ; Control Register A
CI2CRB  = $DD0F ; Control Register B
; End Prefix
