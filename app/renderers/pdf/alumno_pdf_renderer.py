from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.dto.alumno_ficha import AlumnoFicha

def render_alumno_ficha_pdf(ficha: AlumnoFicha) -> bytes:
    
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

  
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, height - 72, "Ficha del Alumno")

    
    c.setFont("Helvetica", 12)
    y = height - 72 - 30
    lineas = [
        f"Nro de Legajo: {ficha.legajo or 'N/D'}",
        f"Apellido y Nombre: {ficha.apellido}, {ficha.nombre}",
        f"DNI: {ficha.dni}",
        f"Email: {ficha.email}",
        f"Facultad: {ficha.facultad or 'N/D'}",
    ]
    for linea in lineas:
        c.drawString(72, y, linea)
        y -= 20

    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    return pdf
