# ASC_TO_PRN_CONVERTER
Convert the .ASC files PADs exports to .PRN files the MyChronic MY100 Pick and Place Machine can interpret




this is what the .ASC file structure is expected by the program to look like before the program can manipulate it:


*********** START TEXT COPY ***************

!PADS-POWERPCB-V2007.0-MILS! DESIGN DATABASE ASCII FILE 1.0
*PART*       ITEMS

*REMARK* REFNM PTYPENM X Y ORI GLUE MIRROR ALT CLSTID CLSTATTR BROTHERID LABELS

Z1              FIDUCIAL15-30 1875  -70   90.000 U N 0 -1 0 -1 1
.
.
.

*********** END TEXT COPY  ***************

note that the file is not expected to have dots at the bottom, that is just meant to show that this will now repeat the same pattern 1 time for each component on the board (Z1 would be component #1)
