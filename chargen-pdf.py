from __future__ import division

import paranoia, util

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Table

styles = getSampleStyleSheet()
normal = styles['Normal']

def escape(str):
	return str.replace('&', '&amp;')

char = paranoia.make_random_char()
sheet = [
	Paragraph('Name: %s' % char.name, normal),
	Paragraph('Gender: %s' % char.gender, normal),
	Paragraph(escape(util.format_service_group(char)), normal),
	Paragraph('Action Skills', normal),
	Table([[Table(util.build_skill_table(char.skills[skill])) for skill in paranoia.action_skills]]),
	Paragraph('Knowledge Skills', normal),
	Table([[Table(util.build_skill_table(char.skills[skill])) for skill in paranoia.knowledge_skills]]),
	Paragraph('Mutant power:', normal),
	Paragraph('Secret society:', normal)
]
	
output = Canvas('char.pdf')
frame = Frame(1/2 * inch, 1/2 * inch, 7.5 * inch, 10.5 * inch)
frame.addFromList(sheet, output)
output.save()