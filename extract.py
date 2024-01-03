import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import fitz  # PyMuPDF
import os
import datetime

def preprocess_image(pix):
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # Convertir en niveaux de gris
    img = img.convert('L')
    # Amélioration du contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    # Binarisation pour obtenir une image en noir et blanc
    img = img.point(lambda x: 0 if x < 128 else 255, '1')
    return img

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = preprocess_image(pix)
            custom_config = r'--oem 3 --psm 6'
            text += pytesseract.image_to_string(img, config=custom_config, lang='eng')
    return text

def write_text_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text)
    print(f"Written to file: {filename}")

def log_extraction(pdf, timestamp):
    print(f"Extraction terminée pour {pdf} à {timestamp}.")

def main():
    pdf_directory = os.getcwd()
    max_size = 1000000  # 1 Mo
    accumulated_text = ""
    file_index = 1
    output_filename = f"extracted_text_{file_index}.txt"

    for pdf in os.listdir(pdf_directory):
        if pdf.endswith('.pdf'):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf_path = os.path.join(pdf_directory, pdf)
            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_text_with_header = f"\n\n--- Start of {pdf} ---\n\n{extracted_text}\n\n--- End of {pdf} ---\n"

            if len(accumulated_text.encode('utf-8')) + len(extracted_text_with_header.encode('utf-8')) > max_size:
                write_text_to_file(output_filename, accumulated_text)
                accumulated_text = extracted_text_with_header
                file_index += 1
                output_filename = f"extracted_text_{file_index}.txt"
            else:
                accumulated_text += extracted_text_with_header

            log_extraction(pdf, timestamp)

    # Write any remaining text to a file
    if accumulated_text:
        write_text_to_file(output_filename, accumulated_text)

if __name__ == "__main__":
    main()
