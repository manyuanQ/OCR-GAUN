# import packages
import os
import pandas as pd
import text_extraction as te
import text_classificatin as tc


# Path to the folder containing the PDF files
pdf_folder = './Dataset'
# Path to the folder where the CSV files will be saved
csv_folder = './csv_folder'
# csv file column list
column_list = ['year', 'Council', 'Session', 'Agenda item', 'Agenda detail', 'cosponsored countries', 
               'body title number',	'body title detail', 'body text', 'date', 'file', 'filecountry', 'footnote', 'scanned']

# record countries
visited_countries = ['Afghanistan', 'Albania', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Barbados', 'Benin', 'Bhutan']
# Loop through each folder and PDF file and extract text
for country_folder in os.listdir(pdf_folder):
    # check if the country is unvisited
    if country_folder in visited_countries:
        continue
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

        #nfile = int(pdf_file[5:-4])
        if year < 1994 or year > 1998:
            continue

        if year == 1998:
            df = pd.DataFrame(rows, columns = column_list)
            csv_path = os.path.join(csv_folder, f"{country_folder}_1994-{year-1}.csv")
            df.to_csv(csv_path, index = False) 
            break

        pdf_path = os.path.join(pdf_folder, country_folder, pdf_file).replace('\\', '/')
        print(pdf_path)

        # try:
        pdf_text = te.extract_text_from_pdf(pdf_path)
        text_columns = tc.classify_text_to_column(pdf_text)
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
        # except:
        #     print(f"Error extracting text from {pdf_path}")
        #     continue
    # Write the rows to the CSV file
    # df = pd.DataFrame(rows, columns = column_list)
    # df.to_csv(csv_path, index = False)  
    visited_countries.append(country_folder)
    print('---------------' + country_folder + '---------------' )

