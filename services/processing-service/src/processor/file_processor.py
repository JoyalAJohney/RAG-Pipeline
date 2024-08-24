import PyPDF2
from io import BytesIO
from ..exceptions.exception import UnsupportedFileFormatError


# Reads a PDF file and yields the text of each page
def read_pdf(file_content):
    pdf = PyPDF2.PdfReader(BytesIO(file_content))
    for page_num, page in enumerate(pdf.pages, 1):
        yield page_num, page.extract_text()


def split_into_chunks(text, chunk_size=1000, overlap=100):
    chunks = []
    for i in range(0, len(text), chunk_size-overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks


def process_pdf(file_content):
    chunks = []
    for page_num, page_text in read_pdf(file_content):
        page_chunks = split_into_chunks(page_text)
        for chunk_num, chunk in enumerate(page_chunks, 1):
            chunks.append({
                'content': chunk,
                'page_num': page_num,
                'chunk_num': chunk_num,
            })
    return chunks


def process_file(file_content, file_name):
    if file_name.lower().endswith('.pdf'):
        return process_pdf(file_content)
    else:
        raise UnsupportedFileFormatError(f"Unsupported file format: {file_name}")