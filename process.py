import ocr_extraction as oe
import text2column as tc

def process9497(pdf_path, pdf_file, country_folder):
    pdf_text = oe.extract_text_from_pdf(pdf_path, 70)
    text_columns = tc.text_to_column(pdf_text)
    row = text_columns[:-1] + [pdf_file[:-4], country_folder] + text_columns[-1:] #add column K and L
    return row

def process98(pdf_path, pdf_file, country_folder):
    pdf_text_old = oe.extract_text_from_pdf(pdf_path, 70)
    text_columns = tc.text_to_column(pdf_text_old)
    if row[-2] == 'N/A':
        pdf_text_new = oe.extract_text_from_pdf(pdf_path, 75)
        _, date = tc.get_date_new(pdf_text_new)
        row[-2] = date

    row = text_columns[:-1] + [pdf_file[:-4], country_folder] + text_columns[-1:] #add column K and L
    return row
