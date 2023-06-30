# done by: Julius Bergmann and GPT-4


import os
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak, Spacer
import io
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader, PageObject
from reportlab.lib.colors import white, black, red, blue, green, yellow, brown, pink, purple, orange

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

            # open pdf that is in the songs folder to get the number of pages
            # open pdf that is in the songs folder
            filename = os.path.join(song_directory, f"{artist}-{title}.pdf")
            with open(filename, "rb") as song_file:
                # read pdf
                song_pdf = PyPDF2.PdfFileReader(song_file)

                # add page num of song to song_data
                song_num_pages = song_pdf.getNumPages()

            song_data.append({"artist" : artist, "title" : title, "page_length" : song_num_pages, "page_start" : None})

    return song_data

def get_song_with_pagenum(song_data, pagenum):
    """
    Get the song with the given pagenum.

    Args:
        song_data (list): A list of tuples containing artist and song title.
        pagenum (int): The pagenum of the song.

    Returns:
        dict: A dict containing artist, title, page_length, page_start.
    """
    for song in song_data:
        if song["page_start"] <= pagenum and pagenum < song["page_start"] + song["page_length"]:
            return song


def add_text_to_pdf(input_pdf_path, output_pdf_path, song_data):
    """
    Add text to every page of a PDF and add page numbers to all pages.

    Args:
        input_pdf_path (str): Path to the input PDF.
        output_pdf_path (str): Path to the output PDF.
    """
    # Read the existing PDF
    existing_pdf = PdfFileReader(open(input_pdf_path, "rb"))

    output = PdfFileWriter()

    # iterate over all pages
    for page_number in range(existing_pdf.getNumPages()):

        # get the song with pagenum
        current_song = get_song_with_pagenum(song_data, page_number+1)

        # make string for writing
        title = current_song["title"]
        artist = current_song["artist"]
        text = f"{title} - {artist}"

        # Create a new PDF with Reportlab
        packet = io.BytesIO()
        can = canvas.Canvas(packet)

        can.setFillColor(white)
        can.rect(50,780,420,45, fill=1, stroke=0)
        
        can.setFillColor(black)
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
            # read pdf
            song_pdf = PyPDF2.PdfFileReader(song_file)

            # Append the processed song PDF to the output PDF
            output_pdf.append(song_pdf)

    # Save the combined PDF
    with open(output_filename, "wb") as output_file:
        output_pdf.write(output_file)

def sort_songs(song_data):
    """
    Sort the songs by title.
    """
    song_data.sort(key=lambda song: song["title"])

def set_pages(song_data):
    """
    Set the page start for each song.
    """
    page_start = 1
    for song in song_data:
        song["page_start"] = page_start
        page_start += song["page_length"]

def create_toc(song_data, output_filename):
    """
    Create a Table of Contents from song data.

    Args:
        song_data (list of dicts): The song data.
        output_filename (str): Path to the output PDF.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    # Prepare the data for the Table
    data = [['Titel', 'Künstler:in', '', 'Seite']]  # Column labels
    for song in song_data:
        row = [song['title'], song['artist'], '', song['page_start']]
        data.append(row)

    # Create the Table
    table = Table(data, colWidths=[doc.width/2.5, doc.width/2.5, doc.width/5, doc.width/10])

    # Add a TableStyle
    style = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('GRID', (0,0), (-1,-1), 0, colors.transparent),  # Make the grid transparent
        ('LINEABOVE', (0,1), (-1,1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the Table to the elements to be added to the PDF
    elements = []
    elements.append(PageBreak()) # Add a page break before the Table, so it starts on a new page
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(PageBreak()) # Add a page break after the Table

    # Create the PDF
    doc.build(elements)

def build_songbook(cover_filename, songs_filename, output_filename, toc_filename="toc.pdf"):
    """
    Merge all PDFs in the song_directory and create a combined PDF.
    song_data: list of tuples containing artist and song title
    """
    # Initialize the output PDF merger
    output_pdf = PyPDF2.PdfFileMerger()


    with open(cover_filename, "rb") as file:
        # read pdf
        cover_pdf = PyPDF2.PdfFileReader(file)
        #TODO: scale to A4
        # Scale the cover to letter size
        #cover_pdf.getPage(0).scaleTo(612, 792)
        # Append the processed song PDF to the output PDF
        output_pdf.append(cover_pdf)

    with open(toc_filename, "rb") as file:
        # read pdf
        toc_pdf = PyPDF2.PdfFileReader(file)
        # Append the processed song PDF to the output PDF
        output_pdf.append(toc_pdf)

    with open(songs_filename, "rb") as file:
        # read pdf
        songs_pdf = PyPDF2.PdfFileReader(file)
        # Append the processed song PDF to the output PDF
        output_pdf.append(songs_pdf)

    # Save the combined PDF
    with open(output_filename, "wb") as output_file:
        output_pdf.write(output_file)

if __name__ == "__main__":
    
    song_data = get_song_data()
    #print(songs_data)

    # sort songs by title
    sort_songs(song_data)

    # set page start for each song
    set_pages(song_data)

    merge_songs(song_data)

    # create table of contents
    create_toc(song_data, "toc.pdf")

    # write song data and pagenum on each page
    add_text_to_pdf(output_filename, "real_output.pdf", song_data)

    build_songbook("cover.pdf", "real_output.pdf", "songbook.pdf")
    print("Done!")




