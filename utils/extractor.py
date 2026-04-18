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

def extract_sections(text):
    """
    Splits resume text into sections based on known headings.
    Returns a dict of section_name -> section_text.
    """
    sections = {
        "education": "",
        "skills": "",
        "projects": "",
        "general": ""
    }

    # Keywords that identify each section
    section_markers = {
        "education": ["education", "academic"],
        "skills": ["skills", "technical skills", "skills summary"],
        "projects": ["projects", "project experience"],
    }

    current_section = "general"

    for line in text.split("\n"):
        line_lower = line.lower().strip()

        # Check if this line is a section heading
        matched_section = None
        for section, markers in section_markers.items():
            if any(marker in line_lower for marker in markers):
                matched_section = section
                break

        if matched_section:
            current_section = matched_section
        else:
            sections[current_section] += line + "\n"

    return sections