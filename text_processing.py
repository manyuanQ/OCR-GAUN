import re
from datetime import datetime


date_pattern = r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
# Extract year (A) and date (J)
def extract_date(text):
    """
    Extracts the year and date from the given text.

    Args:
        text (str): The text to extract the date from.

    Returns:
        tuple: A tuple containing the year (str) and date (str) in the format 'mm/dd/yyyy'.
    """
    date_match = re.search(date_pattern, text)
    if date_match:
        date = date_match.group(0)
        date_obj = datetime.strptime(date, '%d %B %Y')
        # change to mm/dd/yyyy format
        formatted_date = date_obj.strftime('%m/%d/%Y') #column J
        year = formatted_date[-4:] #column A
    else:
        year = date = 'N/A'
        print("No date found")
    return year, formatted_date


def remove_empty(text):
    """
    Removes empty spaces and newlines from the given text and returns 'N/A' if the resulting text is empty.

    Args:
        text (str): The text to remove empty spaces and newlines from.

    Returns:
        str: The cleaned text or 'N/A' if the resulting text is empty.
    """
    if not text:
        return 'N/A'
    cleaned_text = ' '.join(text.split())
    return cleaned_text if cleaned_text else 'N/A'
    

council_pattern1 = r"(?<=session).*?(?=Agenda)"
council_pattern2 = r'([A-Z][A-Za-z]+\s)+(COUNCIL|Council)'

# Extract council/committee name (B)
def extract_council(text):
    """
    Extracts the council or committee name from the given text.

    Args:
        text (str): The text to extract the council or committee name from.

    Returns:
        str: The extracted council or committee name, or 'N/A' if not found.
    """
    match1 = re.search(council_pattern1, text, re.DOTALL)
    match2 = re.search(council_pattern2, text, re.DOTALL)
    council = 'N/A'
    
    # Handle the council after session
    if match1:
        council = match1.group(0).strip()
    
    # Handle the council before session
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
    """
    Extracts the session information from the given text.

    Args:
        text (str): The text to extract the session information from.

    Returns:
        str: The extracted session information, or 'N/A' if not found.
    """
    match = re.search(session_pattern, text)
    if match:
        session = match.group("session")
    else:
        session = 'N/A'
        print("Session information not found.")
    return remove_empty(session)


country_pattern = r'^[A-Za-z]+(, [A-Za-z]+)*( and [A-Za-z]+)?$'

def helper_extract_countries(text):
    """
    Extracts countries and footnotes from the given text.

    Args:
        text (list): The list of text lines to extract countries and footnotes from.

    Returns:
        tuple: A tuple containing countries (str) and footnotes (str).
    """
    footnote = ''
    countries = ''
    
    if len(text) == 1:
        countries = text[0]
        return countries, footnote
    
    for i in range(len(text)):
        part = text[i].replace('\n', ' ')
        match = re.search(country_pattern, part)
        temp = part.split(',')
        
        if part.isupper():
            footnote += part
        elif match:
            countries += ' '.join(text[i:])
            break
        elif len(temp) >= 3:
            countries += ' '.join(text[i:])
            break
        else:
            footnote += part
    return countries, footnote

agenda_pattern = r'Agenda item (\d+)(?: \((\w+)\))?(?:\n\n)?'
agendas_pattern = r'Agenda items (\d+ \(\w+\)? and \d+)'
sp_agenda_pattern = r'Item (\d+ ?)(?: \((\w+)\) ?)?of the provisional agenda'
draft_pattern = r':? *([\w ]*|[\n]*)? ?draft'

def extract_agenda_countries(text):
    """
    Extracts agenda item, agenda detail, countries, and footnotes from the given text.

    Args:
        text (str): The text to extract the information from.

    Returns:
        tuple: A tuple containing agenda item (str), agenda detail (str), countries (str), and footnotes (str).
    """
    single_agenda_match = re.search(agenda_pattern, text)
    multiple_agenda_match = re.search(agendas_pattern, text)
    special_agenda_match = re.search(sp_agenda_pattern, text)
    start_index = 0

    if single_agenda_match:
        agenda_item_number = single_agenda_match.group(1)
        agenda_item_letter = single_agenda_match.group(2)
        agenda_item = f"{agenda_item_number} ({agenda_item_letter})" if agenda_item_letter else agenda_item_number
        start_index = single_agenda_match.end()
    elif multiple_agenda_match:
        agenda_item = multiple_agenda_match.group(1)
        start_index = multiple_agenda_match.end()
    elif special_agenda_match:
        agenda_item_number = special_agenda_match.group(1)
        agenda_item_letter = special_agenda_match.group(2)
        agenda_item = f"{agenda_item_number} ({agenda_item_letter})" if agenda_item_letter else agenda_item_number
        start_index = special_agenda_match.end()
    else:
        print("Agenda not found")
        agenda_item = 'N/A'

    countries = 'N/A'
    footnote = 'N/A'
    agenda_detail = 'N/A'
    if start_index != 0:
        match3 = re.search(draft_pattern, text[start_index:], re.DOTALL)
        if match3:
            end_index = start_index + match3.start()
            content = text[start_index:end_index]
            parts = content.split("\n\n")
            parts = [s for s in parts if s != '']
            if len(parts) == 1:
                parts = content.split("\n")
            parts = [s for s in parts if s != '']
            agenda_detail = parts[0]
            remain_parts = parts[1:]
            for i in range(1, len(parts)):
                if parts[i].isupper():
                    agenda_detail += parts[i]
                else:
                    remain_parts = parts[i:]
                    break
            countries, footnote = helper_extract_countries(remain_parts)
        else:
            print('Agenda match3 error')
            countries = 'N/A'
            footnote = 'N/A'
            agenda_detail = 'N/A'

    return agenda_item, remove_empty(agenda_detail), remove_empty(countries), footnote


def split_text(text):
    """
    Splits the given text into two parts based on the draft_pattern.

    Args:
        text (str): The text to be split.

    Returns:
        tuple: A tuple containing the two parts of the split text.
    """
    # Delete extracted text
    split_text = re.split(draft_pattern, text, flags=re.IGNORECASE)
    
    part1_text = split_text[0]
    part2_text = split_text[2:]
    part2_text = '\n\n'.join(part2_text)
    
    return part1_text, part2_text


text_head_pattern = r'(The General Assembly,|The Commission on Human Rights,|The Human Rights Council |The Economic and Social Council,|1\.)'
number_title_pattern = r'^\s*(\d{4})?/?\W*(.*)'

def extract_body_title(text):
    """
    Extracts body title number (G), body title (H), and body text from the given text.

    Args:
        text (str): The text to extract the information from.

    Returns:
        tuple: A tuple containing body title number (str), body title (str), and body text (str).
    """
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
        match3 = re.search(r"[A-Z].*?[A-Z]", title)
        if match3:
            index = match3.end(0) - 1
            body = title[index:]
            body = body.replace("  ", "\n\n")
            title = title[:index]
    title = remove_empty(title)
    if len(title.split('/')) == 3:
        title = 'N/A'

    return remove_empty(title_number), title, body

footnote_pattern = r'^(\*|\d(?![./])|\d{1}/)\s.*'

def extract_body(text):
    """
    Extracts body text (I) and footnote (M) from the given text.

    Args:
        text (str): The text to extract the body text and footnote from.

    Returns:
        tuple: A tuple containing the body text (str) and footnote (str).
    """
    body_text = ''
    footnote = []
    footnote_idx = 1
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.replace("\n", " ")
        match = re.search(footnote_pattern, paragraph)
        if match:
            if match.group(0)[0] == '*':
                footnote.append(match.group(0))
            elif match.group(0)[0] == str(footnote_idx):
                footnote.append(match.group(0))
                footnote_idx += 1
        else:
            if len(paragraph) == 0:
                continue
            elif len(paragraph) >= 2:
                if (paragraph[0] == str(footnote_idx) and paragraph[1] == '/') or paragraph[0] == "*":
                    footnote_idx += 1
                    footnote.append(paragraph) 
            if not re.search(r'(\d{2}-\d{5}|[A-Za-z]/\d{2}/[A-Za-z]\.\d|[A-Za-z ]+Please recycle|Page \d{1})', paragraph):
                body_text += paragraph.strip() + ' '
    footnote = ' '.join(footnote)
    return body_text, footnote
