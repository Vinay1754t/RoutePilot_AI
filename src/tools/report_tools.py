from langchain_core.tools import tool
from fpdf import FPDF
import os
import tempfile

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'RoutePilot_AI Travel Itinerary', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@tool
def generate_itinerary_pdf(itinerary_text: str):
    """
    Generates a PDF file from the provided travel itinerary text. 
    Call this tool ONLY when the user asks to download, save, or get a PDF of the plan.
    Returns the file path of the generated PDF.
    """
    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Handle unicode roughly for hackathon speed (Latin-1)
        safe_text = itinerary_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_text)
        
        # Save to temp
        filename = "itinerary.pdf"
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        pdf.output(file_path)
        
        return f"PDF generated successfully at: {file_path}"
    except Exception as e:
        return f"Error generating PDF: {str(e)}"