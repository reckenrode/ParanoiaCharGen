#!/usr/bin/env python2
# !/usr/bin/python2 -OO

import cgi
import cgitb

import EquipmentDatabase

cgitb.enable()

input_template = open("equipgen_tem.html")

output_html = input_template.read()

query = cgi.FieldStorage()
if 'clearance' in query:
    clearance = query['clearance'].value
    if clearance not in ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET']:
        clearance = 'RED'
else:
    clearance = 'RED'

if 'credits' in query:
    try:
        credits = int(query['credits'].value)
    except:
        credits = 1000
else:
    credits = 1000

if 'quantity' in query:
    try:
        quantity = int(query['quantity'].value)
    except:
        quantity = 20
else:
    quantity = 20

print("content-type: text/html")
print()
print()

(equipment, credsleft) = EquipmentDatabase.get_equip(credits, clearance, quantity)

equip_html = '<ul class="elist">'

for item, quant in equipment:
    equip_html += '<li>'
    equip_html += item.name + " "
    # equip_html += "%i"%item.price + "C "
    equip_html += '(' + item.clearance + ')'
    if quant > 1:
        equip_html += ' x' + '%i' % quant
    equip_html += '</li>\n'

equip_html += '</ul>'

balance_html = 'Credits left: %i' % credsleft

output_html = output_html.replace('<!--elist-->', equip_html, 1)
output_html = output_html.replace('<!--balance-->', balance_html, 1)

print(output_html)
