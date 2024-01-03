import requests
import openpyxl

def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Le fichier {filename} a été téléchargé avec succès.")
    else:
        print(f"Échec du téléchargement du fichier {filename}.")

def main():
    # Remplacez ceci par le chemin de votre fichier Excel
    excel_path = 'jfk.xlsx'

    # Ouvrir le fichier Excel
    try:
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier Excel : {e}")
        return

    # Parcourir les cellules pour trouver les hyperliens
    for row in sheet.iter_rows(min_row=2):  # Ajustez min_row si nécessaire
        cell = row[0]  # Première colonne
        if cell.hyperlink:
            url = cell.hyperlink.target
            filename = url.split('/')[-1]
            download_pdf(url, filename)

if __name__ == "__main__":
    main()
