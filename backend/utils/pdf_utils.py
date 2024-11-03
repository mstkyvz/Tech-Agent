from pypdf import PdfReader
import io
from utils.utils import clean_text

async def process_pdf_file(file):
    contents = await file.read()
    try:
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)
        text = "\n\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return clean_text(text)
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return ""