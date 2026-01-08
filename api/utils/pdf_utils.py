from pypdf import PdfReader, PdfWriter
import os
import uuid

def split_pdf_into_pages(pdf_path, output_dir):
    reader = PdfReader(pdf_path)
    page_paths = []

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        filename = f"{uuid.uuid4()}_page_{i+1}.pdf"
        out_path = os.path.join(output_dir, filename)

        with open(out_path, "wb") as f:
            writer.write(f)

        page_paths.append(out_path)

    return page_paths