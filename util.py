def format_service_group(char):
	rstr = 'Service group: %(group)s [%(firm)s]'
	if char.group.cover != None: # Spy for IntSec
		rstr += ' (NOTE: As a spy for IntSec, your cover group is %(cover)s [%(coverfirm)s]'
	elif char.group.spyon != None: # Spy
		rstr += ' (NOTE: You are a spy. Your target is %(spyon)s'
	return rstr % char.group.__dict__
	
def build_skill_table(skill):
	return [[spec, skill[spec]] for spec in skill]