import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Takes the path to a PDF file.
    Returns all the text inside it as a single string.
    """
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:                    # some pages may be blank
                text += page_text + "\n"

    return text.strip()