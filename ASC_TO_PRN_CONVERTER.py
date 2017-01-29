import csv

#####################################################################################################

def convert_ASC_to_dirty_CSV():
    # Convert ASC to dirty (unformatted) CSV
    with open('ORIGINAL_ASC.asc', 'r') as infile, open('ASC_to_CSV.csv', 'w') as outfile:
        for line in infile:
            # 'fields' is an array that will be filled with whatever is currently
            # in the "line" string (from the for loop). the .split() method essentially
            # looks at a string and converts every value separated by whitespace into a unique
            # element and appends that element to the 'fields' array.
            # the .join() function turns an array of strings ('fields', in this case)
            # to a single string, where each element will now be separated by a comma
            # (a comma because of the ',' part of the "','.join(fields)" code)        
            fields = line.split()
            # "{}" is what will be replaced by the .format() function. Every row in the 'fields'
            # array will be changed from space-delimited to comma-delimited and then inserted
            # in the "{}" part and then a "\n" newline operator is appended to the end of each row
            outfile.write('{}\n'.format(','.join(fields)))

#####################################################################################################

def clean_the_dirty_csv():
    # Read the file in to a list called readerObj
    dirtyCSVRows = []
    csvFileObj = open('ASC_to_CSV.csv')
    readerObj = csv.reader(csvFileObj)
    for row in readerObj:
        # Skip lines 2, 3, and 5
        if (readerObj.line_num == 2) or (readerObj.line_num == 3) or (readerObj.line_num == 5):
            continue
        # Now create the SUPER list from this reader object which essentially copies 
        # the contents of the whole CSV file into a list(array) in memory called "cleanCSVRows[]"
        dirtyCSVRows.append(row)
    csvFileObj.close()

    
    row_count = 0 # row_count is essentially just a counter in the upcoming for loop
    deletion_index = [] # deletion_index is a generic array we're going to use to clean bad elements out of our other arrays
    for row in dirtyCSVRows:
        for field in row:
            ## Get rid of any trash elements left behind from the ASC generator
            if "*REMARK*" in field:
                row.remove(field)
                    
            # The first row will always be a header row and the only
            # information we want to keep from here is the first cell
            # which contains the unit information (INCHES, MILLs or Millimeters)
            if (row == dirtyCSVRows[0]) and ("!PADS-" not in field):
                deletion_index.append(field)
                # the following IF statement checks if we're done reading all the data from 
                # the first line
                if row.index(field) == len(row)-1:
                    # now that deletion_index is fully populated for first row, use it to purge bad elements
                    for element in deletion_index:
                        row.remove(element)

        # for each row, delete the unused columns (GLUE(5), ALT(7), CLSTID(8), CLSTATTR(9), BROTHERID(10), LABELS(11))
        if (row_count >= 1):
            # delete the columns backwards so we can hard-code the row orders
            del row[11] # delete LABEL data   
            del row[10] # delete BROTHERID data
            del row[9]  # delete CLSTATTR data
            del row[8]  # delete CLSTID data
            del row[7]  # delete ALT data
            del row[5]  # delete GLUE data
        
        # Increment the counter object        
        row_count += 1
    
    
    # Now we need to create a cleanCSVRows array that will be the dirtyCSVRows array but in the correct order
    cleanCSVRows = []
    
    row_count = 0
    for row in dirtyCSVRows:
        # first re-arrange the elements and store them in a temp array and then
        # append that temp array to cleanCSVRows
        # at this point we know we have 6 columns in this order: REFNM, PTYPNM, X, Y, ORI, MIRROR
        if row_count >= 1: 
            # re-arrange columns in this order: X(2->0), Y(3->1), ORI(4->2), PTYPENM(1->3), REFNM(0->4), MIRROR(5->5)
            row[0], row[1], row[2], row[3], row[4], row[5] = row[2], row[3], row[4], row[1], row[0], row[5]
        
        # Now that the columns are re-sorted, append the clean data to our cleanCSVRows list
        # and get ready to write that cleanCSVRows list to a CSV file named "ASC_to_CSV.csv"
        cleanCSVRows.append(row)
        row_count += 1
                
    # Write out the list to a CSV file
    csvFileObj = open('ASC_to_CSV.csv', 'w', newline='')
    csvWriter = csv.writer(csvFileObj)  
    for row in cleanCSVRows:
        csvWriter.writerow(row)
    csvFileObj.close()

#####################################################################################################

def convert_clean_csv_to_PRN():
    # TODO: everything
    # F1 through F7 go like this:
    # F1 - Title of the layout file in the MY100 machine
    # F2 - Description of the layout file in the MY100 machine
    # U  - This is the units (MILs, INCHES, or Millimeters)
    # F3 - 3 F3 lines for each board fiducial (board fiducial components start with Z)
    # F4 - hard code to 0 0
    # F5 - hard code to 0 0
    # F6 - hard code to 0 0
    # F7 - hard code to 0 0
    # !! From here on F8 and F9 repeat 1 time for each component on the board
    # F8 - [X POS] [Y POS] [ORI+000] [0N] [N] [PTYPENM]
    # F9 - [REFNM]

    # Read the file in to a list called readerObj
    cleanCSVRows = []
    csvFileObj = open('ASC_to_CSV.csv')
    readerObj = csv.reader(csvFileObj)
    for row in readerObj:
        cleanCSVRows.append(row)
    csvFileObj.close()
    

    # Create 2 cleanPRNRows arrays, one for mirrored parts and one for non-mirrored parts
    cleanPRNRows_M = []
    cleanPRNRows_NO_M = []

 
    # Grab the title for the document to use in F1
    doc_title = input("Enter board name: ")
    # Grab the description for the document to use in F2
    doc_desc = input("Enter board description: ")

 
    # Find the 3 fiducials for mirrored FID:
    fid_array_M = []
    n = 0
    for row in cleanCSVRows:
        if n == 0:
            n = 1
            continue        
        fid_temp = "default"
        if ("Z" in row[4]) and (row[5] == "M"):
            fid_temp = str(row[0]) + " " + str(row[1])
            fid_array_M.append(fid_temp)
    
    # Find the 3 fiducials for NON-mirrored FID:
    fid_array_NO_M = []
    n = 0
    for row in cleanCSVRows:
        if n == 0:
            n = 1
            continue
        
        fid_temp = "default"
        if ("Z" in row[4]) and (row[5] == "N"):
            fid_temp = str(row[0]) + " " + str(row[1])
            fid_array_NO_M.append(fid_temp)             

   
    # Create the header for the mirrored array:
    for idx in range(0,8):
        line_text = "Mdefault"
        # F1
        if idx == 0:
            line_text = "F1 " + doc_title.replace(" ","_") + "_MIRRORED"
            cleanPRNRows_M.append(line_text)
            continue
        # F2
        if idx == 1:
            line_text = "F2 " + doc_desc.replace(" ","_")
            cleanPRNRows_M.append(line_text)
            continue
        # U
        if idx == 2:
            #firstCSVRow = cleanCSVRows[0]
            if "MILS" in cleanCSVRows[0]:
                line_text = "U MILS"
                cleanPRNRows_M.append(line_text)
                continue
            elif "INCHES" in cleanCSVRows[0]:
                line_text = "U INCHES"
                cleanPRNRows_M.append(line_text)
                continue
            elif "Millimeters" in cleanCSVRows[0]:
                line_text = "U Millimeters"
                cleanPRNRows_M.append(line_text)
                continue                 
            else:
                line_text = "U Could_Not_Determine"
                cleanPRNRows_M.append(line_text)
                continue
        # F3
        if idx == 3:
            for fid_idx in range(0,len(fid_array_M)):
                line_text = "F3 " + str(fid_array_M[fid_idx])
                cleanPRNRows_M.append(line_text)
                continue
        # F4
        if idx == 4 or idx == 5 or idx == 6 or idx == 7:
            line_text = "F" + str(idx) + " 0 0"
            cleanPRNRows_M.append(line_text)
            continue
    
    # Create the header for the NON-mirrored array:
    for idx in range(0,8):
        line_text = "N_Mdefault"
        # F1
        if idx == 0:
            line_text = "F1 " + doc_title.replace(" ","_") + "_NON_MIRRORED"
            cleanPRNRows_NO_M.append(line_text)
            continue
        # F2
        if idx == 1:
            line_text = "F2 " + doc_desc.replace(" ","_")
            cleanPRNRows_NO_M.append(line_text)
            continue
        # U
        if idx == 2:
            print(cleanCSVRows[0])
            if "MILS" in cleanCSVRows[0]:
                line_text = "U MILS"
                cleanPRNRows_NO_M.append(line_text)
                continue
            elif "INCHES" in cleanCSVRows[0]:
                line_text = "U INCHES"
                cleanPRNRows_NO_M.append(line_text)
                continue
            elif "Millimeters" in cleanCSVRows[0]:
                line_text = "U Millimeters"
                cleanPRNRows_NO_M.append(line_text)
                continue                 
            else:
                line_text = "U Could_Not_Determine"
                cleanPRNRows_NO_M.append(line_text)
                continue
        # F3
        if idx == 3:
            for fid_idx in range(0,len(fid_array_NO_M)):
                line_text = "F3 " + str(fid_array_NO_M[fid_idx])
                cleanPRNRows_NO_M.append(line_text)
                continue
        # F4
        if idx == 4 or idx == 5 or idx == 6 or idx == 7:
            line_text = "F" + str(idx) + " 0 0"
            cleanPRNRows_NO_M.append(line_text)
            continue
   
    
    # Now populate all the component information for MIRRORED
    n = 0
    for row in cleanCSVRows:
        line_text = "Mdefault"
        if n == 0 or n == 1:
            # We don't care about the first or second lines
            n += 1
            continue
        
        if row[5] == "N":
            # Don't care about non-mirrored parts
            n += 1
            continue
        
        if row[5] == "M":
            line_text = "F8 " + str(row[0]) + " " + str(row[1]) + " " + str(row[2].replace(".","")) + " 0N N " + str(row[3])
            cleanPRNRows_M.append(line_text)
            line_text = "F9 " + str(row[4])
            cleanPRNRows_M.append(line_text)
            continue
        n += 1
    
    # Now populate all the component information for NON MIRRORED
    n = 0
    for row in cleanCSVRows:
        line_text = "NO_Mdefault"
        if n == 0 or n == 1:
            # We don't care about the first or second lines
            n += 1
            continue
        
        if row[5] == "M":
            # Don't care about non-mirrored parts
            n += 1
            continue
        
        if row[5] == "N":
            line_text = "F8 " + str(row[0]) + " " + str(row[1]) + " " + str(row[2].replace(".","")) + " 0N N " + str(row[3])
            cleanPRNRows_NO_M.append(line_text)
            line_text = "F9 " + str(row[4])
            cleanPRNRows_NO_M.append(line_text)
            continue
        n += 1

    # Finally, now that the files are populated, give them their escape characters:
    cleanPRNRows_M.append("E")
    cleanPRNRows_NO_M.append("E")
    
                
    file_name = doc_title.replace(" ","_") + "_MIRRORED.prn"
    M_PRN_file = open(file_name, "w")
    for row in cleanPRNRows_M:
        M_PRN_file.write(row + "\n")
    M_PRN_file.close()
    
    print(file_name + " has been created and deposited in the program's root folder")

    file_name = doc_title.replace(" ","_") + "_NON_MIRRORED.prn"
    NO_M_PRN_file = open(file_name, "w")
    for row in cleanPRNRows_NO_M:
        NO_M_PRN_file.write(row + "\n")
    NO_M_PRN_file.close()    

    print(file_name + " has been created and deposited in the program's root folder")

def main():
    convert_ASC_to_dirty_CSV()
    clean_the_dirty_csv()
    convert_clean_csv_to_PRN()

main()




































