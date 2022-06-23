import os
from docx import Document
from docx.shared import Inches
import win32print
document = Document()
section = document.sections[0]
section.page_height = Inches(1)
section.page_width = Inches(3)
section.left_margin = Inches(0.1)
section.right_margin = Inches(0.1)
section.top_margin = Inches(0.1)
section.bottom_margin = Inches(0.1)
document.add_paragraph("This is a test label to see how much text I can fit onto one label. It seems like this label should be able to hold a lot of text.")
document.save("test.docx")

os.startfile("test.docx", "print")