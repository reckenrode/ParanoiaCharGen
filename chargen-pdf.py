#!/usr/bin/env python2

from __future__ import division

import cgi_buffer, paranoia, util, re, sys
sys.path.append('/home/demiurge/.site-packages/lib/python2.2/site-packages/')

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, PageBreak, Paragraph, Table

styles = getSampleStyleSheet()
normal = styles['Normal']
margins = (0.5 * inch, 0.5 * inch, 7 * inch, 10 * inch)

pagesize = {
	'letter': (8.5 * inch, 11 * inch)
}

version = 'chargen-pdf rev. %s' % re.match('[^\d]*(\d*).*', '$LastChangedRevision$').groups()[0]

def escape(str):
	return str.replace('&', '&amp;')

def build_table(char, sklist):
	return Table([
		[h.title() for h in sklist],
	  	[Table(util.build_skill_table(char.skills[skill])) for skill in sklist]])

def get_spy_info(society):
	results = []
	if society.cover != None:
		results.append(Paragraph('You are a member of the Illuminati.', normal, '*'))
		results += get_spy_info(society.cover)
	elif society.spyon != None:
		results.append(Paragraph('You are spying on %s for %s.' % (society.spyon.name, society.name), normal, '*'))
		results += get_spy_info(society.spyon)
	return results

try:
	char = paranoia.make_random_char('zap')

	publicsheet = [
		Paragraph('Name: %s' % char.name, normal),
		Paragraph('Gender: %s' % char.gender, normal),
		Paragraph(escape(util.format_service_group(char.group)), normal),
		Paragraph('Action Skills', normal),
		build_table(char, paranoia.action_skills),
		Paragraph('Knowledge Skills', normal),
		build_table(char, paranoia.knowledge_skills)
	]
	privatesheet = [
		Paragraph(util.format_power(char), normal),
		Paragraph(util.format_society(char.society), normal),
		Paragraph('Uncommon skill: %s' % escape(char.skills.uncommon), normal),
		Paragraph('Unlikely skill: %s' % escape(char.skills.unlikely), normal),
		Paragraph('Unhealthy skill: %s' % escape(char.skills.unhealthy), normal),
		Paragraph('Notes', normal)
	]
	
	if char.group.cover != None:
		privatesheet.append(Paragraph('You are a spy for Internal Security [%s].' % escape(char.group.firm), normal, '*'))
	elif char.group.spyon != None:
		privatesheet.append(Paragraph('You are an industrial spy or saboteur, and your target is %s.' % escape(char.group.spyon), normal, '*'))
	
	privatesheet += get_spy_info(char.society)
	
	print 'Content-Type: application/pdf'
	print 'Content-Disposition: attachment; filename="%s.pdf"' % char.name
	print
	
	output = Canvas(sys.stdout, pagesize = pagesize['letter'])
	output.setTitle(char.name)
	output.setAuthor(version)
	output.setSubject('Troubleshooter')
	Frame(*margins).addFromList(publicsheet, output)
	output.showPage()
	Frame(*margins).addFromList(privatesheet, output)
	output.save()
	print char.group.cover
	print char.group.spyon
	print get_spy_info(char.society)
except:
	print 'Content-Type: text/html'
	print
	exc = sys.exc_info()
	print '<html><head><title>Jinkies!</title></head><body><pre>'
	print 'There was an error processing your request.'
	print 'To report this, please send everything after the two hyphens to kenada@polyatomic.org.'
	print '--'
	print version
	print
	sys.stderr = sys.stdout
	sys.excepthook(*sys.exc_info())
	print '</pre><body></html>'
	sys.stderr = sys.__stderr__