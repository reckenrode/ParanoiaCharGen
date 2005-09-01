#! /usr/bin/env python

from __future__ import division
import random, operator, namegen
from paranoia_data import *


class ServiceGroup(object):
    """Represents a service group in Alpha Complex. This includes any
    industrial espionage activies and the appropriate cover."""
    def __init__(self, **kwargs):
        self.cover = kwargs.get('cover', None)
        self.coverfirm = kwargs.get('coverfirm', None)
        self.group = kwargs.get('group', None)
        self.firm = kwargs.get('firm', None)
        self.spyfor = kwargs.get('spyfor', None)
        self.spyon = kwargs.get('spyon', None)


class Skill(object):
    """Represents a character's skill and any of its associated specs."""
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


class SkillProps(type):
    """Metaclass used to add properties for the skills in a SkillCollection"""
    def __init__(cls, name, bases, dict):
        super(SkillProps, cls).__init__(name, bases, dict)
        for sk in knowledge_skills + action_skills:
            setattr(cls, sk, property(lambda self, key = sk: self._SkillCollection__skills[key]))


class SkillCollection(object):
    """Represents a Character's set of skills"""
    __metaclass__ = SkillProps

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
    def __init__(self):
        self.skills = SkillCollection()
        self.group = ServiceGroup()
        self.name = ''
        self.gender = ''


def pick_svc_group():
    """Returns a randomly chosen service group and firm for the character. If
    the character be a spy, pick_svc_group will also choose his target and
    cover."""
    group = weighted_groups[random.randint(0, 19)]
    # There are some special cases we need to handle
    if group == 'Armed Forces' and random.randint(0, 2) == 0: # ~33% chance of not having a firm
        return ServiceGroup(group = group, firm = 'the military')
    elif group == 'Internal Security' and random.randint(0, 1) == 0: # 50% of spying
        cover = pick_svc_group()
        while cover.group == None:
            cover = pick_svc_group()
        return ServiceGroup(group = group, firm = firm, cover = cover.group, coverfirm = cover.firm,
            spyfor = ServiceGroup(group = group, firm = get_svc_firm(group)),
            spyon = ServiceGroup(group = 'everyone'))
    elif group == 'Industrial spy or saboteur':
        spyfor = pick_svc_group()
        spyon = pick_svc_group()
        spyon.firm = None
        return ServiceGroup(spyfor = spyfor, spyon = spyon)
    else:
        return ServiceGroup(group = group, firm = get_svc_firm(group))


def get_svc_firm(group):
    """Returns a random service firm associated with the specified group."""
    return random.choice(groups[group]['firms'])

def make_random_char():
    """Returns a new troubleshooter to serve Friend Computer. Termination of
    commie mutant traitors that may be generated is left up to the user."""
    char = Character()
    
    char.name = namegen.random_name()
    char.gender = random.choice(['Male', 'Female', 'Other'])

    for skill in char.skills:
        # set skill base ratings
        rating = random.randint(1, 20) // 3
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

    # vital speciality!
    char.skills.violence['energy weapons'] += 4
    char.group = pick_svc_group()

    return char