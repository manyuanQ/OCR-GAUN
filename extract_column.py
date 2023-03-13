import pytesseract
from pdf2image import convert_from_path
import os
import re
from datetime import datetime
import pandas as pd

# Function to extract text from a PDF file
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

def extract_text_from_pdf(pdf_path):
    # Convert the PDF to a list of PIL Image objects
    images = convert_from_path(pdf_path)
    text_list = []
    # Loop through each page of the PDF and extract text using Tesseract
    for image in images:
        #print('image')
        raw_text = pytesseract.image_to_string(image)
        text_list.append(raw_text)
    # Combine text from all pages into a single string
    org_text = '\n'.join(text_list)
    #print(org_text)
    return org_text

date_pattern = r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
# Extract year (A) and date (J)
def extract_date(text):
    date_match = re.search(date_pattern, text)
    if date_match:
        date = date_match.group(0)
        date_obj = datetime.strptime(date, '%d %B %Y')
        # change mm/dd/yyyy format
        new_date = date_obj.strftime('%m/%d/%Y') #column J
        year = new_date[-4:] #column A
    else:
        year = date = 'N/A'
        print("No date found")
    return year, date


def remove_empty(text):
    if text == None:
        return 'N/A'
    text = text.replace('\n', ' ')
    text = text.strip()
    if text == '':
        return 'N/A'
    else:
        return text
    

council_pattern1 = r"(?<=session).*?(?=Agenda)"
council_pattern2 = r'([A-Z][A-Za-z]+\s)+(COUNCIL|Council)'

# Extract council/committe name (B)
def extract_council(text):
    match1 = re.search(council_pattern1, text, re.DOTALL)
    match2 = re.search(council_pattern2, text, re.DOTALL)
    council = 'N/A'
    # handle the council after session
    if match1:
        council = match1.group(0).strip()
    # handle the council before session
    if match2:
        council = match2.group(0).strip()
    if 'Economic and Social' in text:
        council = 'Economic and Social Council'
    if council == 'N/A':
        print("Council Name not found")
    return remove_empty(council)


session_pattern = r'(?P<session>[\w-]+\s*session)'
# Extract session (C)
def extract_session(text):
    #print(text)
    #print(remove_empty(text))
    match = re.search(session_pattern, text)
    if match:
        session = match.group("session")
    else:
        session = 'N/A'
        print("Session information not found.")
    return remove_empty(session)


country_pattern1 = r'^[A-Za-z]+ ?$'
country_pattern2 = r'^([A-Za-z]+, )*[A-Za-z]+ and [A-Za-z]+ ?$'
#r'^([A-Za-z]+$)|([A-Za-z]+, )*[A-Za-z]+( |_)and [A-Za-z]+' # ^([A-Za-z]+$)|[A-Za-z]+, *[A-Za-z]+'
#footnote_pattern2 = r'^([A-Z]+ ?)*$'
def helper_extractCountries(text):
    footnote = ''
    countries = ''
    # only one paragraph left -> country only, no footnote
    if len(text) == 1:
        countries = text[0]
        return countries, footnote
    
    for i in range(len(text)):
        #print(part)
        part = text[i].replace('\n', ' ')
        match1 = re.search(country_pattern1, part)
        temp = part.split(',')
        #match2 = re.search(country_pattern2, part)
        if part.isupper(): # older files, footnote is all uppercase, not working for new files
            footnote += part
        elif match1:
            countries += ' '.join(text[i:])
            break
        elif len(temp) >= 3:
            countries += ' '.join(text[i:])
            break
        else:
            footnote += part
    return countries, footnote


agenda_pattern = r'Agenda item (\d+)(?: \((\w+)\))?(?:\n\n)?' # match single agenda item
agendas_pattern = r'Agenda items (\d+ \(\w+\)? and \d+)'  # match agenda items
sp_agenda_pattern = r'Item (\d+) of the provisional agenda'
draft_pattern = r':? *([\w ]*|[\n]*)? ?draft' #': *([\w ]*)?draft'

# Extract Agenda item (D), Agenda detail (E), and countries (F)
def extract_agenda_countries(text):
    # match agenda item
    match1 = re.search(agenda_pattern, text)
    match2 = re.search(agendas_pattern, text)
    match3 = re.search(sp_agenda_pattern, text)
    start_index = 0
    if match1:           # handle single agenda item
        #print("single agenda")
        agenda_item_number = match1.group(1)
        agenda_item_letter = match1.group(2)
        if agenda_item_letter is not None:
            agenda_item = f"{agenda_item_number} ({agenda_item_letter})"
        else:
            agenda_item = agenda_item_number
        
        start_index = match1.end()
    elif match2:         # handle multiple agenda item
        #print("multiple agenda")
        agenda_item = match2.group(1)
        start_index = match2.end()
    elif match3 :  # handle special case:
        agenda_item = match3.group(1)
        start_index = match3.end()
    else:              
        print("Agenda not found")
    
    if start_index != 0:
        match3 = re.search(draft_pattern, text[start_index:], re.DOTALL)
        if match3:
            end_index = start_index + match3.start()
            content = text[start_index:end_index]
            #print(content)
            parts = content.split("\n\n")
            parts = [s for s in parts if s != '']
            #print(parts)
            agenda_detail = parts[0]
            for i in range(1, len(parts)):
                if parts[i].isupper():
                    agenda_detail += parts[i]
                else:
                    remain_parts = parts[i:]
                    break
            countries, footnote = helper_extractCountries(remain_parts)
        else:
            print('Agenda match3 error')
    
    return agenda_item, remove_empty(agenda_detail), remove_empty(countries), footnote


def split_text(text):
    # delete extracted text
    split_text = re.split(draft_pattern, text, flags=re.IGNORECASE)
    #print(split_text)
    #print(len(split_text))
    part1_text = split_text[0]
    part2_text = split_text[2:]
    part2_text = '\n\n'.join(part2_text)
    return part1_text, part2_text


text_head_pattern = r'(The General Assembly,|The Commission on Human Rights,|The Human Rights Council |The Economic and Social Council,|1\.)'
number_title_pattern = r'^\s*(\d{4})?/?\W*(.*)'

# Extract body title number (G) and body title （H）
def extract_body_title(text):
    title_body_text = re.split(text_head_pattern, text)
    body = ' '.join(title_body_text[1:])
    title_text = title_body_text[0]
    title_text = title_text.replace('\n', ' ')
    
    match1 = re.search(r'[A-Z\d]', title_text)
    if match1:
        index = match1.start()
        title_text = title_text[index-1:]
        match2 = re.match(number_title_pattern, title_text)
        if match2:
            title_number = match2.group(1)
            title = match2.group(2)
    else:
        title_number = 'N/A'
        title = 'N/A'

    if remove_empty(title) == remove_empty(title_text) and len(title) > 400:
        #print(True)
        match3 = re.search(r"[A-Z].*?[A-Z]", title)
        if match3:
            index = match3.end(0) - 1
            body = title[index:]
            body = body.replace("  ", "\n\n")
            title = title[:index]
        #print(title)
    title = remove_empty(title)
    if len(title.split('/')) == 3:
        title = 'N/A'

    return remove_empty(title_number), title, body

footnote_pattern = r'^(\*|\d(?![./])|\d{1}/)\s.*'

# Extract body text (I) and footnote (M)
def extract_body(text):
    # extract the text content from the second non-empty paragraph
    body_text = ''
    footnote = []
    footnote_idx = 1
    paragraphs = text.split('\n\n')
    #print(paragraphs)
    
    for paragraph in paragraphs:
        #for line in paragraph.split('\n'):
            # exclude lines containing specific patterns
        paragraph = paragraph.replace("\n", " ")
        #print(paragraph)
        match = re.search(footnote_pattern, paragraph)
        if match:
            if match.group(0)[0] == '*':
                footnote.append(match.group(0))
            elif match.group(0)[0] == str(footnote_idx):
                footnote.append(match.group(0))
                footnote_idx += 1
        else:
            # if len(paragraph) > 50 or paragraph == "The General Assembly,":
            #     body_text += paragraph.strip() + ' '
            # else:
            if len(paragraph) == 0:
                continue
            if (paragraph[0] == str(footnote_idx) and paragraph[1] == '/') or paragraph[0] == "*":
                footnote_idx += 1
                footnote.append(paragraph) 
            if not re.search(r'(\d{2}-\d{5}|[A-Za-z]/\d{2}/[A-Za-z]\.\d|[A-Za-z ]+Please recycle|Page \d{1})', paragraph):
                body_text += paragraph.strip() + ' '
    #print(footnote)
    footnote = ' '.join(footnote)
    return body_text, footnote

# Function to classify text into column A to N
def classify_text_to_column(text):
    result = []
    #print(text)

    # Split based on : draft, which is the end of countries
    part1_text, part2_text = split_text(text)
    
    # Get year(A) and date(J)
    #print('A,J')
    year, date = extract_date(part1_text)
    
    # Get council/committe name (B)
    #print('B')
    council = extract_council(part1_text)

    # Get session (C)
    #print('C')
    session = extract_session(part1_text)

    # Get agenda item (D), agend detail (E), and countries (F)
    #print('D, E, F')
    agenda_item, agenda_detail, countries, footnote1 = extract_agenda_countries(text)

    # Get title number (G) and title body (H)
    #print('G, H')
    title_number, title_text, body = extract_body_title(part2_text)

    # Get Body text (I) and footnote(M)
    #print('I, M')
    body_text, footnote2 = extract_body(body)
    footnote = footnote1 + footnote2
    
    # Add into result list
    result = [year, council, session, agenda_item, agenda_detail, countries, title_number, title_text, body_text, date, footnote]
    
    return result