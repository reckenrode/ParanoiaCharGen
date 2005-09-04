#!/usr/bin/env python2

from __future__ import division

import cgi_buffer, paranoia, util, re, sys
sys.path.append('/home/demiurge/.site-packages/lib/python2.2/site-packages/')

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, PageBreak, Paragraph, Table, TableStyle

styles = getSampleStyleSheet()
normal = styles['Normal']
title = styles['title']
margins = (0.5 * inch, 0.5 * inch, 7 * inch, 10 * inch)

pagesize = {
	'letter': (8.5 * inch, 11 * inch)
}

version = 'chargen-pdf rev. %s' % re.match('[^\d]*(\d*).*', '$LastChangedRevision$').groups()[0]

def escape(str):
	return str.replace('&', '&amp;')

def build_table(char, sklist):
	return Table([
		[h for h in sklist],
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

	actionSkillTable = build_table(char, paranoia.action_skills)
	knowledgeSkillTable = build_table(char, paranoia.knowledge_skills)

	skillTableStyle = TableStyle([('BACKGROUND',(0,0),(-1, 0),colors.black), 
								  ('TEXTCOLOR',(0,0),(-1, 0),colors.white),
								  ('LINEBEFORE', (1, 1), (1, -1), 1, colors.black),
								  ('LINEBEFORE', (2, 1), (2, -1), 1, colors.black),
			  					  ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
								  ('VALIGN', (1, 0), (-1, -1), 'TOP')])

	actionSkillTable.setStyle(skillTableStyle)
	knowledgeSkillTable.setStyle(skillTableStyle)

	publicsheet = [
		Paragraph('<b>Name:</b> %s' % char.name, normal),
		Paragraph('<b>Gender:</b> %s' % char.gender, normal),
		Paragraph('<b>Service group:</b> ' + escape(util.format_service_group(char.group)), normal),
		Paragraph('Action Skills', title),
		actionSkillTable,
		Paragraph('Knowledge Skills', title),
		knowledgeSkillTable
	]
	privatesheet = [
		Paragraph('<b>Mutant power:</b> ' + util.format_power(char), normal),
		Paragraph('<b>Secret society:</b> ' + util.format_society(char.society), normal),
		build_table(char, ['Uncommon', 'Unlikely', 'Unhealthy']),
		Paragraph('<b>Notes</b>', normal)
	]
	
	if char.group.cover != None:
		privatesheet.append(Paragraph('You are a spy for Internal Security [%s].' % escape(`char.group.firm`), normal, '*'))
	elif char.group.spyon != None:
		privatesheet.append(Paragraph('You are an industrial spy or saboteur, and your target is %s.' % escape(`char.group.spyon`), normal, '*'))
	
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