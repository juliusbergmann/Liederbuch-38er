# done by: Julius Bergmann and GPT-4


import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader, PageObject

song_directory = "songs"
output_filename = "song_book.pdf"


# don't use this function now
def create_toc(song_data):
    """
    Create a table of contents PDF with song_data.
    
    Args:
        song_data (list): A list of tuples containing artist and song title.
    """
    # create a table of content and give back a pdf that can be merged

def merge_pdfs_with_toc():
    """
    Merge all PDFs in the song_directory and create a combined PDF with a table of contents.
    """
    song_data = []

    # Collect song data from PDF filenames
    for filename in os.listdir(song_directory):
        if filename.endswith(".pdf"):
            # Filenames are formatted as "Artist - Song Title.pdf"
            # Split the filename into artist and title
            artist, title = filename[:-4].split("-")
            song_data.append((artist, title))

    # Create a table of contents PDF
    #create_toc(song_data)

    # Initialize the output PDF merger
    output_pdf = PyPDF2.PdfFileMerger()

    # Append the table of contents to the output PDF
    #with open("temp_toc.pdf", "rb") as toc_file:
    #    output_pdf.append(PyPDF2.PdfFileReader(toc_file))

    # Process and append each song PDF
    for artist, title in song_data:
        # open pdf that is in the songs folder
        filename = os.path.join(song_directory, f"{artist}-{title}.pdf")

        with open(filename, "rb") as song_file:
            song_pdf = PyPDF2.PdfFileReader(song_file)

            # Add song title and artist name to the first page
            first_page = song_pdf.getPage(0)
            first_page.compressContentStreams()
            content = f"q /Helvetica 14 Tf 10 750 Td ({artist} - {title}) Tj Q"
            first_page._content = content.encode() + first_page["/Contents"]._data

            # Add page numbers
            for i in range(song_pdf.getNumPages()):
                page = song_pdf.getPage(i)
                page.compressContentStreams()
                content = f"q /Helvetica 14 Tf 10 10 Td ({i + 1}) Tj Q"
                page._content = page["/Contents"]._data + content.encode()

            # Append the processed song PDF to the output PDF
            output_pdf.append(song_pdf)

    # Save the combined PDF and remove the temporary table of contents PDF
    with open(output_filename, "wb") as output_file:
        output_pdf.write(output_file)
    #os.remove("temp_toc.pdf")


def get_song_data():
    """
    Collect song data from PDF filenames.
    
    Returns:
        list: A list of tuples containing artist and song title.
    """
    song_data = []

    # Collect song data from PDF filenames
    for filename in os.listdir(song_directory):
        if filename.endswith(".pdf"):
            # Filenames are formatted as "Artist - Song Title.pdf"
            # Split the filename into artist and title
            artist, title = filename[:-4].split("-")
            song_data.append({"artist" : artist, "title" : title, "page_length" : None, "page_start" : None})

    return song_data


def add_text_to_pdf(input_pdf_path, output_pdf_path, text):
    """
    Add text to every page of a PDF and add page numbers to all pages.

    Args:
        input_pdf_path (str): Path to the input PDF.
        output_pdf_path (str): Path to the output PDF.
        text (str): Text to add.
    """
    # Read the existing PDF
    existing_pdf = PdfFileReader(open(input_pdf_path, "rb"))

    output = PdfFileWriter()

    # iterate over all pages
    for page_number in range(existing_pdf.getNumPages()):

        # Create a new PDF with Reportlab
        packet = io.BytesIO()
        can = canvas.Canvas(packet)

        # Add the text to the PDF
        can.setFontSize(25)
        can.drawString(50, 790, text)

        # Add the page number
        can.setFontSize(20)
       
        if page_number % 2 == 0:  # even page numbers (since the first page is "0", it's considered even)
            x_coordinate = 500  # right side
        else:  # odd page numbers
            x_coordinate = 100  # left side

        can.drawString(x_coordinate, 50, str(page_number + 1))  # "+1" because page_number starts from 0

        # Save the PDF
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)

        # Add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(page_number)
        page.mergePage(new_pdf.getPage(0))

        # Write the output
        output.addPage(page)

    # Save the output PDF
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)


def merge_songs(song_data):
    """
    Merge all PDFs in the song_directory and create a combined PDF.
    song_data: list of tuples containing artist and song title
    """
    # Initialize the output PDF merger
    output_pdf = PyPDF2.PdfFileMerger()

    # Process and append each song PDF
    for song in song_data:
        
        artist = song["artist"]
        title = song["title"]

        # open pdf that is in the songs folder
        filename = os.path.join(song_directory, f"{artist}-{title}.pdf")

        with open(filename, "rb") as song_file:
            song_pdf = PyPDF2.PdfFileReader(song_file)

            # Append the processed song PDF to the output PDF
            output_pdf.append(song_pdf)

    # Save the combined PDF
    with open(output_filename, "wb") as output_file:
        output_pdf.write(output_file)

if __name__ == "__main__":
    
    song_data = get_song_data()
    #print(songs_data)

    merge_songs(song_data)

    # Process and append each song PDF
    for song in song_data:
        artist = song["artist"]
        title = song["title"]
        
        # get filename of pdf that is in the songs folder
        filename_read = os.path.join(song_directory, f"{artist}-{title}.pdf")
        filename_write = os.path.join("songs_modified", f"{artist}-{title}_modified.pdf")
        add_text_to_pdf(filename_read, filename_write, f"{title} - {artist}")




