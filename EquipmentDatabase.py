#! /usr/bin/env python2


import random, re

infinity = 1e5000

clearances = ['INFRARED', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET']

clearance_ranks = dict([(x, clearances.index(x)) for x in clearances])

def clearance_difference(c1, c2):
    v1 = clearance_ranks.get(c1, 1000)
    v2 = clearance_ranks.get(c2, 1000)
    return v1 - v2;


class EquipmentItem(object):
    __slots__ = ['name', 'price', 'clearance']

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', "Nothing")
        self.price = kwargs.get('price', 1)
        self.clearance = kwargs.get('clearance', "INFRARED")
        
    def __str__(self):
        return self.name + "; " + str(self.price) + "; " + self.clearance;

    def legal_at_clearance(self, clearance):
        if clearance_difference(clearance, self.clearance) >= 0:
            return True
        else:
            return False

EquipmentDatabase = []


def load_list(filename):
    equipment_line_re = re.compile("^(.*);([ \t0-9]*);(.*)$")
    
    f = open(filename)
    for line in f:
        m = equipment_line_re.match(line)
        if m != None:
            name = m.group(1).strip()
            price = int(m.group(2))
            EquipmentDatabase.append(EquipmentItem(name=name, price=price, clearance=m.group(3).strip()))


load_list("equipment.list")

def get_equip(creds, clearance, amount):
    my_list = []
    
    while creds > 200 and len(my_list) < amount:
        item = random.choice(EquipmentDatabase)    
        legality = clearance_difference(clearance, item.clearance)
        #print legality, item.name, item.clearance
        if creds - item.price > 0 and ((0 <= legality < 3) or random.choice([True, False, False])):
            # buy item
            my_list.append(item)
            creds -= item.price

    #compress list
    tmp_list = [(x.name, x) for x in my_list]
    tmp_list.sort()
    #    my_list = [x for (key, x) in tmp_list]
    # turn sorted list into (item, quant) list
 
    curr_name = None
    my_list = []
    for (name, i) in tmp_list:
        if name == curr_name:
            my_list[-1] = (my_list[-1][0], my_list[-1][1] + 1)
        else:
            my_list.append((i, 1))
            curr_name = name
      
        
    return my_list, creds
