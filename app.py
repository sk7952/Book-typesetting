import streamlit as st
import nest_asyncio
from playwright.async_api import async_playwright
import asyncio
from main import get_response, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers
from concurrent.futures import ThreadPoolExecutor
from reportlab.pdfgen import canvas
import os
from PyPDF2 import PdfMerger

# Install Playwright if needed
os.system('playwright install')

# Create a ThreadPoolExecutor to run the async function
executor = ThreadPoolExecutor()

# Function to convert HTML to PDF with Playwright
nest_asyncio.apply()

async def html_to_pdf_with_margins(html_file, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        await page.set_content(html_content, wait_until='networkidle')

        pdf_options = {
            'path': output_pdf,
            'format': 'A4',
            'margin': {
                'top': '85px',
                'bottom': '60px',
                'left': '70px',
                'right': '40px'
            },
            'print_background': True
        }

        await page.pdf(**pdf_options)
        await browser.close()

# Streamlit UI
st.title("Chapter PDF Generator")

# Dynamic list to store chapter inputs
chapter_texts = []
num_chapters = st.number_input('How many chapters do you want to add?', min_value=1, max_value=10, step=1)

for i in range(num_chapters):
    chapter_text = st.text_area(f'Enter the Chapter {i+1} text:')
    chapter_texts.append(chapter_text)

author_name = st.text_input('Enter the Author Name:')
book_name = st.text_input('Enter the Book Name:')
font_size = st.text_input('Enter the Font Size')
line_height = st.text_input('Enter the Line Spacing')

# Dropdown menu for font selection
fonts = [
    'Courier', 'Courier-Bold', 'Courier-BoldOblique', 'Courier-Oblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-BoldOblique', 'Helvetica-Oblique',
    'Times-Roman', 'Times-Bold', 'Times-BoldItalic', 'Times-Italic',
    'Symbol', 'ZapfDingbats'
]
font_style = st.selectbox('Select Font Style:', fonts)

First_page_no = st.number_input('Enter the First Page Number:', min_value=0, max_value=1000, step=1)
options = ['Left', 'Right']
first_page_position = st.selectbox('Select First Page Position:', options)

# Button to generate PDF
if st.button("Generate PDF"):
    final_pdfs = []
    current_page_number = First_page_no  # Start from the user-defined first page number

    # Set the initial page position for the first chapter
    current_position = first_page_position  # "Right" or "Left" based on input

    for idx, chapter_text in enumerate(chapter_texts):
        response = get_response(chapter_text, font_size, line_height)
        html_pth = save_response(response)

        main_pdf = f'out_{idx+1}.pdf'
        
        # Run the function to generate the main PDF
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf))

        total_pages = get_pdf_page_count(main_pdf)
        overlay_pdf = f"overlay_{idx+1}.pdf"
        
        # Create the overlay PDF with continuous page numbers
        current_position = create_overlay_pdf(overlay_pdf, total_pages, current_page_number, book_name, author_name, font_style, current_position)
        
        final_pdf = f'final_{idx+1}.pdf'
        final_pdfs.append(final_pdf)
        
        # Overlay the headers and footers
        overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)
        
        # Update current_page_number for the next chapter
        current_page_number += total_pages
    
    # Merge all the final PDFs into one
    merger = PdfMerger()
    for pdf in final_pdfs:
        merger.append(pdf)

    merged_pdf_path = 'merged_final.pdf'
    merger.write(merged_pdf_path)
    merger.close()

    st.success("All PDFs merged successfully into one!")

    # Provide a download button for the merged final PDF
    with open(merged_pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download Final Merged PDF",
            data=pdf_file,
            file_name=merged_pdf_path,
            mime="application/pdf"
        )
