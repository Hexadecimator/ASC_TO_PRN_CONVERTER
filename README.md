# ASC_TO_PRN_CONVERTER
Convert the .ASC files PADs exports to .PRN files the MyChronic MY100 Pick and Place Machine can interpret




this is what .ASC file structure is expected by the program to look like before the program can manipulate it:


*********** START TEXT COPY ***************

!PADS-POWERPCB-V2007.0-MILS! DESIGN DATABASE ASCII FILE 1.0
*PART*       ITEMS

*REMARK* REFNM PTYPENM X Y ORI GLUE MIRROR ALT CLSTID CLSTATTR BROTHERID LABELS
*REMARK* .REUSE. INSTANCE RPART
*REMARK* VISIBLE XLOC YLOC ORI LEVEL HEIGTH WIDTH MIRRORED HJUST VJUST RIGHTREADING
*REMARK* FONTSTYLE FONTFACE

Z1              FIDUCIAL15-30 165   420   90.000 U N 0 -1 0 -1 1
VALUE           0           0   0.000 26       59.06        5.91 N CENTER CENTER ORTHO
Regular <Romansim Stroke Font>
Part Type
[.... ABOVE 4 LINES REPEAT AGAIN AND AGAIN FOR EVERY PART ON THE BOARD ....]

*END*     OF ASCII OUTPUT FILE

*********** END TEXT COPY  ***************

Note 1: The Z1 line will be repeated again for each component that is on the board

NOTE 2: Anything that is italicized is actually wrapped with asterisk characters, the GitHub editor just italicises them
