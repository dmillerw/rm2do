from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas


# def create_calibration_pdf():
canvas = Canvas("calibration.pdf", pagesize=LETTER)
canvas.setFillColor("black")
canvas.circle(inch,             LETTER[1] - inch, inch / 2, stroke=1, fill=1)
canvas.circle(LETTER[0] - inch, LETTER[1] - inch, inch / 2, stroke=1, fill=1)
canvas.circle(LETTER[0] / 2,    LETTER[1] / 2,    inch / 2, stroke=1, fill=1)
canvas.circle(inch,             inch,             inch / 2, stroke=1, fill=1)
canvas.circle(LETTER[0] - inch, inch,             inch / 2, stroke=1, fill=1)

canvas.circle(LETTER[0] / 2 - inch,    LETTER[1] / 2,    inch / 2, stroke=1, fill=1)
canvas.circle(LETTER[0] / 2 + inch,    LETTER[1] / 2,    inch / 2, stroke=1, fill=1)

canvas.setFillColor("white")
canvas.circle(inch,             LETTER[1] - inch, inch / 16, stroke=1, fill=1)
canvas.circle(LETTER[0] - inch, LETTER[1] - inch, inch / 16, stroke=1, fill=1)
canvas.circle(LETTER[0] / 2,    LETTER[1] / 2,    inch / 16, stroke=1, fill=1)
canvas.circle(inch,             inch,             inch / 16, stroke=1, fill=1)
canvas.circle(LETTER[0] - inch, inch,             inch / 16, stroke=1, fill=1)

canvas.circle(LETTER[0] / 2 - inch,    LETTER[1] / 2,    inch / 16, stroke=1, fill=1)
canvas.circle(LETTER[0] / 2 + inch,    LETTER[1] / 2,    inch / 16, stroke=1, fill=1)

canvas.save()