# import packages
import os
import pandas as pd
import extract_column as ec

# Path to the folder containing the PDF files
pdf_folder = './Dataset'
# Path to the folder where the CSV files will be saved
csv_folder = './csv_folder'
# csv file column list
column_list = ['year', 'Council', 'Session', 'Agenda item', 'Agenda detail', 'cosponsored countries', 
               'body title number',	'body title detail', 'body text', 'date', 'file', 'filecountry', 'footnote', 'scanned']


# Loop through each folder and PDF file and extract text
for country_folder in os.listdir(pdf_folder):
    print('---------------' + country_folder + '---------------' )
    if not os.path.isdir(os.path.join(pdf_folder, country_folder)):
        continue
    
    rows = []
    count = 0
    # Loop through each file 
    #csv_year = 1994
   
    for pdf_file in os.listdir(os.path.join(pdf_folder, country_folder)):
        if not pdf_file.endswith('.pdf'):
            continue
        # check if this file is old-version
        year = int(pdf_file.split('_')[0])
        if year < 1995:
            continue

        pdf_path = os.path.join(pdf_folder, country_folder, pdf_file).replace('\\', '/')
        print(pdf_path)
        # try:
        pdf_text = ec.extract_text_from_pdf(pdf_path)
        text_columns = ec.classify_text_to_column(pdf_text)
        row = text_columns[:-1] + [pdf_file[:-4], country_folder] + text_columns[-1:] #add column K and L
        
        # check if year was extracted correctlys
        if row[0] != year:
            row[0] = year
        
        # scanned (N), cannot know 
        if int(year) > 1990:
            scanned = 'yes'
        else:
            scanned = 'no'
        row.append(scanned)

        rows.append(row)
        # count += 1
        # if count == 5:
        #     break
        #print(rows)
        if year == 1996:
            df = pd.DataFrame(rows[:-1], columns = column_list)
            csv_path = os.path.join(csv_folder, f"{country_folder}_{year-1}.csv")
            df.to_csv(csv_path, index = False) 
            break
        # except:
        #     print(f"Error extracting text from {pdf_path}")
        #     continue
    break
    # Write the rows to the CSV file
    df = pd.DataFrame(rows, columns = column_list)
    df.to_csv(csv_path, index = False)  

