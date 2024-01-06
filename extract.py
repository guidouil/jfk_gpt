import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance
import os

def extract_text_with_fitz(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
        print(f"Page {page.number} extracted by PyMuPDF")
    doc.close()
    return text

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

def extract_text_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = preprocess_image(pix)
        custom_config = r'--oem 3 --psm 6'
        text += pytesseract.image_to_string(img, config=custom_config, lang='eng')
        print(f"Page {page_num} extracted by OCR")
    doc.close()
    return text

def is_text_complete(text, threshold=100):
    # Vous pouvez ajuster la logique ici pour déterminer si le texte semble complet
    return len(text) > threshold

def main():
    pdf_directory = os.getcwd()
    output_file = 'combined_text.txt'

    with open(output_file, 'w') as outfile:
        for pdf in os.listdir(pdf_directory):
            if pdf.endswith('.pdf'):
                pdf_path = os.path.join(pdf_directory, pdf)
                extracted_text = extract_text_with_fitz(pdf_path)

                if not is_text_complete(extracted_text):
                    extracted_text = extract_text_with_ocr(pdf_path)

                outfile.write(f"--- Texte de {pdf} ---\n")
                outfile.write(extracted_text)
                outfile.write("\n\n")

if __name__ == "__main__":
    main()
