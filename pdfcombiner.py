#####Description########
#This script will find all pdfs in its directory and merge them into a new pdf called combinedpdf.
#If this file already exists, a digit will be appended to it (ex. combinedpdf, combinedpdf1, combinedpdf2...)
#Any .pdf files that follow the naming scheme for the new pdf will not be merged to avoid data duplication
#If there are no pdfs in the folder, an error text file will be written to the script's directory and the script will gracefully exit.
#Written by Zain Nasrullah
########################

import os, PyPDF2, traceback, datetime, re

#reads the directory
Files = os.listdir()

#specifies combined pdf file name
newPDF = "combinedpdf"

#if no pdf files exist in the current directory, write an error log text file and quit
if not '.pdf' in str(Files):
    try:
        raise Exception("No .pdf files exist in this folder")
    except:
        print("An error has occured, writing to a text file named Error_log.txt")
        error = open('Error_log.txt', 'a')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error.write(time + '\n' + traceback.format_exc() + '\n')
        error.close()
        quit()

#initialize writer        
writer = PyPDF2.PdfFileWriter()

#Check whether pdf currently exists and append accordingly
regex = re.compile(newPDF + r'(\d)?.pdf')
Exists = regex.findall(str(Files))

if Exists != [] and Exists == ['']:
    Append = 1
elif Exists != []:
    Append = int(Exists[-1])+1
else:
    Append = ''

#create the new pdf
newPDFName = newPDF + str(Append)+ '.pdf'     
OutputPDF = open(newPDFName, 'wb')

print("Combining the following .pdf files:\n")

#loops through a three step process for each; a previously merged pdf (by naming convention) will not be merged
for pdf in Files:
    if pdf.endswith('.pdf') and newPDF not in pdf:

        #open and read 
        pdfopen = open(pdf, 'rb')
        print('\t'+pdf)
        reader = PyPDF2.PdfFileReader(pdfopen)

        #iterate through pages and add to writer
        for page in range(reader.numPages):
            writer.addPage(reader.getPage(page))

        #write to the new pdf and then close
        writer.write(OutputPDF)
        pdfopen.close()
        
OutputPDF.close()

#printing out some help text for the user
print('')
if Append != '':
    print('A version of ' + newPDF + ' already exists,' \
           ' iterating to the next available digit.')
    
print ("The files were combined into " + newPDFName)
