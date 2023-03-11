import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PageObject

# Öffne das PDF-Dokument, das bearbeitet werden soll
with open('merged_files.pdf', 'rb') as fin:
    reader = PdfFileReader(fin)
    writer = PdfFileWriter()

    # Iteriere über jede Seite im Dokument
    for i in range(reader.getNumPages()):
        page = reader.getPage(i)

        # Füge Seitenzahl hinzu
        page.mergePage(PageObject.createBlankPage(page.mediaBox.getWidth(), page.mediaBox.getHeight()))
        page_text = page.extractText()
        page_text = 'Seite {}\n{}'.format(i + 1, page_text)
        page.updatePageFormTextField(page_text)

        # Füge Seite zum neuen Dokument hinzu
        writer.addPage(page)

    # Speichere das bearbeitete Dokument
    with open('edited_document.pdf', 'wb') as fout:
        writer.write(fout)