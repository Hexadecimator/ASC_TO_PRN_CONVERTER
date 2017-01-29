# ASC_TO_PRN_CONVERTER
Convert the .ASC files PADs exports to .PRN files the MyChronic MY100 Pick and Place Machine can interpret




this is what .ASC file structure is expected by the program to look like before the program can manipulate it:


*********** START TEXT COPY ***************

!PADS-POWERPCB-V2007.0-MILS! DESIGN DATABASE ASCII FILE 1.0

*PART*     ITEMS

*REMARK*  REFNM PTYPENM X Y ORI GLUE MIRROR ALT CLSTID CLSTATTR BROTHERID LABELS

Z1              FIDUCIAL15-30 1875  -70   90.000 U N 0 -1 0 -1 1

*********** END TEXT COPY  ***************

Note 1: The Z1 line will be repeated again for each component that is on the board

NOTE 2: "PART" and "REMARK" are italicized because that's what happens when you put an asterisk by a word in the GitHub editor, the "PART" and "REMARK" items are actually "(asterisk)PART(asterisk)" and "(asterisk)REMARK(asterisk)"
