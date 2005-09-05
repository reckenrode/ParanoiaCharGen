#!/usr/bin/env python2
#!/usr/bin/python2 -OO

from __future__ import division

import cgi, cgitb, cgi_buffer, paranoia, util, re, sys
sys.path.append('/home/demiurge/.site-packages/lib/python2.2/site-packages/')

cgitb.enable()

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, PageBreak, Paragraph, Table, TableStyle, Spacer

styles = getSampleStyleSheet()
normal = ParagraphStyle(name='normal', parent=styles['Normal'], fontName="Helvetica", bulletFontName='Symbol')
title = ParagraphStyle(name='title', parent=styles['title'], fontName="Helvetica", bulletFontName='Symbol', spaceBefore=6)

margins = (0.5 * inch, 0.5 * inch, 7 * inch, 9.5 * inch)

pagesize = {
	'letter': (8.5 * inch, 11 * inch)
}

version = 'chargen-pdf rev. %s' % re.match('[^\d]*(\d*).*', '$LastChangedRevision$').groups()[0]

def escape(str):
	return str.replace('&', '&amp;')

def build_table(char, sklist, s=TableStyle()):
	thirdsize = (7*inch - 0.5*inch)/3.0
	return Table([
		[h for h in sklist],
	  	[Table(util.build_skill_table(char.skills[skill]), style=s, colWidths=(thirdsize-inch/2, inch/2)) for skill in sklist]])

def get_spy_info(society):
	results = []
	if society.cover != None:
		results.append(Paragraph('You are a member of the Illuminati (degree: %s).' % society.degree, normal, 'a'))
		results += get_spy_info(society.cover)
	elif society.spyon != None:
		results.append(Paragraph('You are spying on %s for %s (degree: %s).' % (society.spyon.name, society.name, society.degree), normal, 'a'))
		results += get_spy_info(society.spyon)
	return results


query = cgi.FieldStorage()
if query.has_key('style'):
	style = query['style'].value
else:
	style = 'zap'
	
#if query.has_key('name'):
#	name = query['name']
	
char = paranoia.make_random_char(style)

mainTitle = ParagraphStyle(name='MainTitle',
                              parent=title,
                              fontName = 'Helvetica-Bold',
                              fontSize=18,
                              leading=22,
                              alignment=TA_CENTER,
                              spaceAfter=6)

individualSkillStyle = TableStyle([('FONT', (0,0), (-1, -1), "Helvetica", 10),
						      ('ALIGN', (1, 0), (1, -1), "RIGHT"),
							  ('RIGHTPADDING', (0,0), (-1, -1), 0),
							  ('LEFTPADDING', (0,0), (-1, -1), 0)])


actionSkillTable = build_table(char, paranoia.action_skills, individualSkillStyle)
knowledgeSkillTable = build_table(char, paranoia.knowledge_skills, individualSkillStyle)

skillTableStyle = TableStyle([('BACKGROUND',(0,0),(-1, 0),colors.black), 
							  ('TEXTCOLOR',(0,0),(-1, 0),colors.white),
							  ('LINEBEFORE', (1, 1), (1, -1), 1, colors.black),
							  ('LINEBEFORE', (2, 1), (2, -1), 1, colors.black),
		  					  ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
							  ('VALIGN', (0, 1), (-1, -1), 'TOP'),
							  ('FONT', (0,0), (-1, 0), "Helvetica-Bold", 16),
							  ('LEFTPADDING', (0,0), (-1, -1), 2),
							  ('RIGHTPADDING', (0,0), (-1, -1), 2),
							  ('BOTTOMPADDING', (0,0), (-1, 0), 0),
							  ('TOPPADDING', (0,0), (-1, 0), 0)])

actionSkillTable.setStyle(skillTableStyle)
knowledgeSkillTable.setStyle(skillTableStyle)

publicsheet = [
	Paragraph('PARANOIA<font size=7><super>TM</super></font> XP CHARACTER SHEET', style=mainTitle),
	Paragraph('<b>Name:</b> %s' % char.name, normal),
	Paragraph('<b>Gender:</b> %s' % char.gender, normal),
	Paragraph('<b>Service group:</b> ' + escape(util.format_service_group(char.group)), normal),
	Paragraph('Action Skills', title),
	actionSkillTable,
	Paragraph('Knowledge Skills', title),
	knowledgeSkillTable
]

secretSkillTable = build_table(char, ['Uncommon', 'Unlikely', 'Unhealthy'], individualSkillStyle)
secretSkillTable.setStyle(skillTableStyle)

footer = [
	Paragraph("<para fontsize=7>PARANOIA Copyright (c) 1983,1987,2005 Eric Goldberg and Greg Costikyan.\n PARANOIA is a trademark of Eric Goldberg and Greg Costikyan. All Rights Reserved.</para>", normal)
]


miscTableStyle = TableStyle([ ('LINEBEFORE', (1, 4), (2, 4), 1, colors.black),
							('LINEBELOW', (0, 4), (-1, 4), 1, colors.black),
							('FONT', (0,0), (-1, -1), "Helvetica", 12),
							('SPAN', (0,0), (-1, 0)),
							('SPAN', (0,1), (-1, 1)),
							('SPAN', (0,2), (-1, 2)),
						    ('VALIGN', (0, 1), (0, 1), 'TOP'),
						    ('BACKGROUND',(0,3),(-1, 3),colors.black),
							('TEXTCOLOR',(0,3),(-1, 3),colors.white),
							('FONT', (0,3), (-1, 3), "Helvetica-Bold", 16),
							('BOTTOMPADDING', (0,3), (-1, 3), 0),
							('TOPPADDING', (0,3), (-1, 3), 0)
							])


notesBlock = [Paragraph('', normal)]

if char.group.cover != None:
	notesBlock.append(Paragraph('You are a spy for %s [%s].' % (escape(char.group.name), escape(char.group.firm)), normal, 'a'))
elif char.group.spyon != None:
	notesBlock.append(Paragraph('You are an industrial spy or saboteur for %s [%s].' % (escape(char.group.name), escape(char.group.firm)), normal, 'a'))

notesBlock += get_spy_info(char.society)


miscTable = Table([[Paragraph('Notes', title), '', ''], 
				   [notesBlock, '', ''], 
				   [Paragraph('Equipment', title), '',''],
				   ['Personal', 'Assigned', 'Treasonous'],
				   ['', '', '']], style=miscTableStyle,
					rowHeights=[None, inch*3, None, None, inch*2.5])

privatesheet = [
	Paragraph('<b>Mutant power:</b> ' + util.format_power(char), normal),
	Paragraph('<b>Secret society:</b> ' + util.format_society(char.society), normal),
	Paragraph('Secret Skills', title),
	secretSkillTable,
	miscTable
]


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
Frame(0.5*inch, 0*inch, 7.5*inch, 0.5*inch ).addFromList(footer, output)
output.showPage()

output.save()