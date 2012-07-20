#from weakref import WeakValueDictionary
import random, operator, weakref

def format_service_group(group):
	"""pretty prints the group"""
	rstr = '%s [%s]'
	if group.cover != None: # Spy for IntSec
		return rstr % (group.cover, group.cover.firm)
	elif group.spyon != None:
		return rstr % (group.spyon, group.spyon.firm)
	else:
		return rstr % (group, group.firm)

def format_society(society):
	rstr = '%s (degree: %s)'
	if society.cover != None:
		return rstr % (society.cover, society.cover.degree)
	elif society.spyon != None:
		return rstr % (society.spyon.name, society.spyon.degree)
	else:
		return rstr % (society.name, society.degree)

def format_power(char):
	rstr = '%s'
	if char.registered:
		rstr += ' [registered]'
	return rstr % char.power

def build_skill_table(skill):
	"""makes an nx2 table of the skill's specs where n = len(skill.specs)"""
	table = [[spec, skill[spec]] for spec in skill]
	table.sort(lambda x, y: cmp(x[0], y[0]))
	if 'Energy Weapons' not in skill:
		table.append(['________________________', '__'])
		table.append(['________________________', '__'])
	table.append(['________________________', '__'])
	table.append(['________________________', '__'])
	return table

class tag(int): pass

class weightedchoice(object):
	__slots__ = ['cache']
	cache = {}
	
	def __new__(cls, lst):
		lid = id(lst)
		try:
			return random.choice(weightedchoice.cache[lid])
		except KeyError:
			weightedchoice.cache[lid] = reduce(operator.add, [[item for n in xrange(weight)] for weight, item in lst])
			return random.choice(weightedchoice.cache[lid])