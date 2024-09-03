import streamlit as st
import nest_asyncio
from playwright.async_api import async_playwright
import asyncio
from main import get_response, save_response, get_pdf_page_count, create_overlay_pdf, overlay_headers_footers
from concurrent.futures import ThreadPoolExecutor
from reportlab.pdfgen import canvas
import os

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
                'top': '70px',
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

# Input fields in a single vertical layout
Chapter_text = st.text_input('Enter the Chapter text:')
author_name = st.text_input('Enter the Author Name:')
book_name = st.text_input('Enter the Book Name:')
font_size = st.text_input('Enter the Font Size')

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
    response = get_response(Chapter_text, font_size)
    html_pth = save_response(response)

    main_pdf = 'out.pdf'
    
    # Run the function to generate the main PDF
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(html_to_pdf_with_margins(html_pth, main_pdf))

    total_pages = get_pdf_page_count(main_pdf)
    overlay_pdf = "overlay.pdf"
    
    # Create the overlay PDF with selected font
    create_overlay_pdf(overlay_pdf, total_pages, First_page_no, book_name, author_name, font_style, first_page_position)
    
    final_pdf = 'final.pdf'
    
    # Overlay the headers and footers
    overlay_headers_footers(main_pdf, overlay_pdf, final_pdf)

    st.success("PDF Generated Successfully!")

    # Provide a download button for the final PDF
    with open(final_pdf, "rb") as pdf_file:
        st.download_button(
            label="Download Final PDF",
            data=pdf_file,
            file_name=final_pdf,
            mime="application/pdf"
        )
