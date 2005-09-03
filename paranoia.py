#! /usr/bin/env python

from __future__ import division
import math, random, namegen, operator, util
from paranoia_data import *


class SecretSociety(object):
    __slots__ = ['cover', 'name', 'skills', 'spyon']
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.spyon = kwargs.get('spyon', None)
        self.cover = kwargs.get('cover', None)
        self.skills = kwargs.get('skills', [])
        
    def __str__(self):
        return self.name
        
        
class ServiceGroup(object):
    """Represents a service group in Alpha Complex. This includes any
    industrial espionage activies and the appropriate cover."""
    __slots__ = ['cover', 'firm', 'name', 'spyon']
    def __init__(self, **kwargs):
        self.cover = kwargs.get('cover', None)
        self.firm = kwargs.get('firm', None)
        self.name = kwargs.get('name', None)
        self.spyon = kwargs.get('spyon', None)
        
    def __str__(self):
        return self.name


class Skill(object):
    """Represents a character's skill and any of its associated specs."""
    __slots__ = ['__specs', 'name', 'value']
    def __init__(self, name, defvalue, specs):
        self.name = name
        self.value = defvalue
        self.__specs = dict([(s, defvalue) for s in specs])

    def __iter__(self):
        """Returns an iterator to the skill's specs"""
        return iter(self.__specs)

    def __setitem__(self, spec, value):
        """Sets the value of the spec to that specified by value. If the spec
        does not belong to the Skill, KeyError will be raised."""
        self.__specs[spec] = value

    def __getitem__(self, spec):
        """Returns the value of the specified spec. If the spec
        does not belong to the Skill, KeyError will be raised."""
        return self.__specs[spec]


class SkillCollection(object):
    """Represents a Character's set of skills"""
    __slots__ = ['__skills', 'uncommon', 'unlikely', 'unhealthy']

    def __init__(self):
        self.__skills = dict([(sk, Skill(sk, 0, [s for s in specs[sk]]))
                                 for sk in action_skills + knowledge_skills])

    def __getitem__(self, key):
        return self.__skills[key]

    def __iter__(self):
        """Returns an iterator over the skills in the collection"""
        return self.__skills.itervalues()


class Character(object):
    """Represents a troubleshooter in Alpha Complex. By default, the
    troubleshooter is not a commie mutant traitor."""
    __slots__ = ['gender', 'group', 'name', 'power', 'registered', 'skills', 'society']
    
    def __init__(self):
        self.skills = SkillCollection()
        self.group = ServiceGroup()
        self.name = ''
        self.gender = ''


def pick_svc_group(filter = []):
    """Returns a randomly chosen service group and firm for the character. If
    the character be a spy, pick_svc_group will also choose his target and
    cover."""
    group = random.choice(weighted_groups)
    while group in filter:
        group = random.choice(weighted_groups)
    # There are some special cases we need to handle
    if group == 'Armed Forces' and random.randint(0, 2) == 0: # ~33% chance of not having a firm
        return ServiceGroup(name = group, firm = 'Military')
    elif group == 'Internal Security' and random.randint(0, 1) == 0: # 50% of spying
        cover = pick_svc_group(['Internal Security'])
        return ServiceGroup(name = group, firm = get_svc_firm(group), cover = cover)
    elif group == 'Industrial spy or saboteur':
        spyfor = pick_svc_group(['Industrial spy or saboteur'])
        spyfor.spyon = pick_svc_group(['Industrial spy or saboteur', spyfor.name])
        return spyfor
    else:
        return ServiceGroup(name = group, firm = get_svc_firm(group))


def get_svc_firm(group):
    """Returns a random service firm associated with the specified group."""
    return random.choice(groups[group]['firms'])

        
def lookup_society(society):
    if type(society) != str:
        society = society.name
    for n in xrange(len(societyskills)):
        if societyskills[n][0] == society:
            return n
    else:
        raise SyntaxError('Someone goofed when keying the data (society = %s)' % society)


def getskills(n):
    return [pickskill(n, 1), pickskill(n, 2), pickskill(n, 3)]
    

def pickskill(n, skilltype):
    skill = societyskills[n][skilltype]
    if type(skill) == tuple:
        if skill[0] == 'M':
            return skill[1]
        elif random.randint(1, 5) == 1:
            num = random.randint(1, len(societyskills)) - 1
            while num == n:
                num = random.randint(1, len(societyskills)) - 1
            return pickskill(num, skilltype)
        else:
            return random.choice(skill)
    elif random.randint(1, 5) == 1:
        num = random.randint(1, len(societyskills)) - 1
        while num == n:
            num = random.randint(1, len(societyskills)) - 1
        return pickskill(num, skilltype)
    else:
        return skill


def pick_society(group):
    society = util.weightedchoice(groups[group.name]['societies'])
    if society == 'Illuminati':
        cover = pick_society(group)
        while cover.name == 'Illuminati': # Fold all Illuminatis into one big Illuminati
            cover = pick_society(group)
        return SecretSociety(name = society, cover = cover, skills = getskills(lookup_society(cover)))
    elif society == 'Spy':
        forwhom = pick_society(group)
        forwhom.spyon = pick_society(group)
        while forwhom.spyon.name == forwhom.name:
            forwhom.spyon = pick_society(group)
        return forwhom
    else:
        return SecretSociety(name = society, skills = getskills(lookup_society(society)))


def make_random_char(style):
    """Returns a new troubleshooter to serve Friend Computer. Termination of
    commie mutant traitors that may be generated is left up to the user."""
    char = Character()

    char.name = namegen.random_name()
    char.gender = random.choice(['Male', 'Female'])

    char.group = pick_svc_group()
    grpspec = random.choice(groups[char.group.name]['specs'])

    for skill in char.skills:
        # set skill base ratings
        rating = int(math.ceil(random.randint(1, 20) / 2))
        if rating < 4:
            rating = 4
        for spec in skill:
            skill[spec] = rating

    # put all of the spec lists into one big list
    tmp_spec_list = reduce(operator.add, specs.itervalues())

    random.shuffle(tmp_spec_list)
    tmp_spec_list.remove('energy weapons')

    rec_skills = {}
    # boosts
    boosts = 0
    for spec in tmp_spec_list:
        if boosts >= 6:
            break
        for skill in char.skills:
            if spec in skill:
                if rec_skills.get(skill.name, 0) < 3:
                    rec_skills[skill.name] = rec_skills.get(skill.name, 0) + 1
                    skill[spec] += 4
                    tmp_spec_list.remove(spec)
                    boosts += 1

    # drops
    drops = 6
    for spec in tmp_spec_list:
        if drops <= 0:
            break
        for skill in char.skills:
            if spec in skill:
                if rec_skills.get(skill.name, 0) > 0:
                    rec_skills[skill.name] = rec_skills.get(skill.name, 0) - 1
                    skill[spec] = 1
                    tmp_spec_list.remove(spec)
                    drops -= 1

    try:
        for skill in char.skills:
            for spec in skill:
                if spec == grpspec:
                    skill[spec] += 4
                    raise StopIteration()
        else:
            raise SyntaxError('Someone goofed when keying the data (grpspec = %s)' % grpspec)
    except StopIteration:
        pass

    # vital speciality!
    char.skills['violence']['energy weapons'] += 4

    char.power = random.choice(powers[style])
    char.registered = (random.randint(1, 20) == 1) and char.power != 'Machine Empathy'
    
    char.society = pick_society(char.group)
    char.skills.uncommon = char.society.skills[0]
    char.skills.unlikely = char.society.skills[1]
    char.skills.unhealthy = char.society.skills[2]

    return char