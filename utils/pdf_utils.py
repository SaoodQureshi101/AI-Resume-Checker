from PyPDF2 import PdfReader


def extract_text_from_pdf(file_obj):
    """Extract text from a file-like PDF object and return concatenated text."""
    try:
        reader = PdfReader(file_obj)
        pages = []
        for p in reader.pages:
            text = p.extract_text()
            if text:
                pages.append(text)
        return "\n".join(pages)
    except Exception:
        return ""
