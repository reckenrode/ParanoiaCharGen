def format_service_group(group):
	"""pretty prints the group"""
	rstr = 'Service group: %(group)s [%(firm)s]'
	if group.cover != None: # Spy for IntSec
		rstr += ' (NOTE: As a spy for IntSec, your cover group is %(cover)s [%(coverfirm)s])'
	elif group.spyon != None: # Spy
		rstr += ' (NOTE: You are a spy. Your target is %(spyon)s'
	return rstr % group.__dict__


def format_power(char):
	rstr = 'Mutant power: %s'
	if char.registered:
		rstr += ' [registered]'
	return rstr % char.power

def build_skill_table(skill):
	"""makes an nx2 table of the skill's specs where n = len(skill.specs)"""
	table = [[spec.title(), skill[spec]] for spec in skill]
	table.sort(lambda x, y: cmp(x[0], y[0]))
	return table