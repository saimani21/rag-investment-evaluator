from fpdf import FPDF
from io import BytesIO



def generate_pdf_report(results: dict) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial")

    pdf.cell(0, 10, "Investment Memo Evaluation Report", ln=True)
    pdf.ln(5)

    for field, evaluation in results.items():
        pdf.cell(0, 10, f"{field}:", ln=True)
        pdf.multi_cell(0, 10, evaluation)
        pdf.ln(3)

    pdf_bytes = BytesIO()
    pdf_bytes.write(pdf.output(dest="S").encode("latin1"))
    pdf_bytes.seek(0)
    return pdf_bytes




