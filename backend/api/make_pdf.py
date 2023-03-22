import io

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('Noto', 'NotoSerif-Regular.ttf'))


def make_pdf(result):
    buffer = io.BytesIO()
    pdf_file = canvas.Canvas(buffer, pagesize=A4)
    text_object = pdf_file.beginText()
    text_object.setTextOrigin(25 * mm, 265 * mm)
    text_object.setFont('Noto', 20)
    text_object.setLeading(32)
    text_object.textLine('Список покупок')
    text_object.setFont('Noto', 14)
    text_object.setLeading(23)

    for key, value in result.items():
        text_object.textLine(f'\u2022 \u2006 {key.capitalize()}'
                             f' ({value[0]}) \u2014 {value[1]}')

    pdf_file.drawText(text_object)
    pdf_file.showPage()
    pdf_file.save()

    buffer.seek(0)
    return buffer
