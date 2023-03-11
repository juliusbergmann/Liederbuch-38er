import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# Liste der PDF-Dateien, die zusammengefügt werden sollen
pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf']

# Erstelle ein neues PDF-Dokument
output_pdf = PdfFileWriter()

# Erstelle eine Liste mit den Titeln der PDF-Dateien
titles = []

# Durchlaufe alle PDF-Dateien und füge sie dem neuen Dokument hinzu
for pdf_file in pdf_files:
    # Öffne die PDF-Datei
    with open(pdf_file, 'rb') as file:
        # Lese die PDF-Datei
        input_pdf = PdfFileReader(file)
        # Füge die Seiten der PDF-Datei dem neuen Dokument hinzu
        for page in range(input_pdf.getNumPages()):
            output_pdf.addPage(input_pdf.getPage(page))
        # Füge den Titel der PDF-Datei der Titel-Liste hinzu
        # own
         # titles.append(input_pdf.getDocumentInfo().title)



titles = pdf_files
# Erstelle ein Inhaltsverzeichnis
output_pdf.addBookmark('Inhaltsverzeichnis', 0, parent=None)
# Durchlaufe die Titel-Liste und füge jeden Titel dem Inhaltsverzeichnis hinzu
for i, title in enumerate(titles):
    output_pdf.addBookmark(title, i+1, parent=None)

# Speichere das neue PDF-Dokument
with open('combined_pdf.pdf', 'wb') as file:
    output_pdf.write(file)