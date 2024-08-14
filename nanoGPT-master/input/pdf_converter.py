import os
import fitz  # PyMuPDF

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def convert_pdfs(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            text = pdf_to_text(pdf_path)
            txt_filename = filename.replace(".pdf", ".txt")
            txt_path = os.path.join(output_dir, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
            print(f"Converted {pdf_path} to {txt_path}")

if __name__ == "__main__":
    input_dir = "pdfs"
    output_dir = "txts"
    convert_pdfs(input_dir, output_dir)
