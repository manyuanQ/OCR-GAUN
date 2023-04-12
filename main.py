# import packages
import os
import pandas as pd
import ocr_extraction as oe
import text2column as tc
import process as pB


# Path to the folder containing the PDF files
pdf_folder = './Dataset'
# Path to the folder where the CSV files will be saved
csv_folder = './csv_folder'
# csv file column list
column_list = ['year', 'Council', 'Session', 'Agenda item', 'Agenda detail', 'cosponsored countries', 
               'body title number',	'body title detail', 'body text', 'date', 'file', 'filecountry', 'footnote', 'scanned']


# get input country name
input_country = input("Start to processing files from Country: ")

# Loop through each folder and PDF file and extract text
for country_folder in os.listdir(pdf_folder):
    # check if the country starts with the input country name
    if country_folder < input_country or country_folder > input_country + 'zzz':
        continue

    print('---------------' + country_folder + '---------------' )
    if not os.path.isdir(os.path.join(pdf_folder, country_folder)):
        continue
    
    rows = []
    # Loop through each file 
    for pdf_file in os.listdir(os.path.join(pdf_folder, country_folder)):
        # check if the file is pdf
        if not pdf_file.endswith('.pdf'):
            continue

        # check if this file is old-version
        year = int(pdf_file.split('_')[0])

        # skip files before 1994 for now
        if year < 1994:
            continue

        if year == 1998:
            df = pd.DataFrame(rows, columns = column_list)
            csv_path = os.path.join(csv_folder, f"{country_folder}_1994-{year-1}.csv")
            df.to_csv(csv_path, index = False) 
            break

        pdf_path = os.path.join(pdf_folder, country_folder, pdf_file).replace('\\', '/')
        print(pdf_path)

        if year >= 1994 and year <1998:
            row = pB.process9497(pdf_path, pdf_file, country_folder)
        else:
            row = pB.process98(pdf_path, pdf_file, country_folder)

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
    # visited_countries.append(country_folder)
    print('---------------' + country_folder + '---------------' )

