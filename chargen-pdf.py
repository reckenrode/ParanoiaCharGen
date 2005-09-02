#!/usr/bin/env python2

from __future__ import division

import cgi_buffer, paranoia, util, re, sys
sys.path.append('/home/demiurge/.site-packages/lib/python2.2/site-packages/')

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Paragraph, Table

styles = getSampleStyleSheet()
normal = styles['Normal']

def escape(str):
	return str.replace('&', '&amp;')

def build_table(char, sklist):
	return Table([
		[h.title() for h in sklist],
	  	[Table(util.build_skill_table(char.skills[skill])) for skill in sklist]])

char = paranoia.make_random_char()
sheet = [
	Paragraph('Name: %s' % char.name, normal),
	Paragraph('Gender: %s' % char.gender, normal),
	Paragraph(escape(util.format_service_group(char.group)), normal),
	Paragraph('Action Skills', normal),
	build_table(char, paranoia.action_skills),
	Paragraph('Knowledge Skills', normal),
	build_table(char, paranoia.knowledge_skills),
	Paragraph('Mutant power:', normal),
	Paragraph('Secret society:', normal)
]

print 'Content-Type: application/pdf'
print

output = Canvas(sys.stdout)
output.setTitle(char.name)
output.setAuthor('chargen-pdf rev. %s' % re.match('[^\d]*(\d*).*', '$LastChangedRevision$').groups()[0])
output.setSubject('Troubleshooter')
Frame(1/2 * inch, 1/2 * inch, 7.5 * inch, 10.5 * inch).addFromList(sheet, output)
output.save()