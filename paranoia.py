#! /usr/bin/env python

from __future__ import division
import random, operator
from paranoia_data import *


class ServiceGroup(object):
    def __init__(self, group = None):
        if group != None:
            self.group, self.firm, self.spyfor, self.spyon = group
        else:
            self.group, self.firm, self.spyfor, self.spyon = (None, None, None, None)


class Skill(object):
    def __init__(self, name, defvalue, specs):
        self.name = name
        self.value = defvalue
        self.__specs = dict((s, defvalue) for s in specs)

    def __iter__(self):
        return iter(self.__specs)

    def __setitem__(self, idx, val):
        self.__specs[idx] = val


    def __getitem__(self, idx):
        return self.__specs[idx]

    def __repr__(self):
        return '%s: %i, %s' % (self.name, self.value, self.__specs)


class SkillProps(type):
    def __init__(cls, name, bases, dict):
        super(SkillProps, cls).__init__(name, bases, dict)
        for sk in knowledge_skills + action_skills:
            setattr(cls, sk, property(lambda self, key = sk: self._SkillCollection__skills[key]))


class SkillCollection(object):
    __metaclass__ = SkillProps

    def __init__(self):
        self.__skills = dict((sk, Skill(sk, 0, (s for s in globals()[sk+'_specs'])))
                                 for sk in action_skills + knowledge_skills)

    def __iter__(self):
        return self.__skills.itervalues()

    def __repr__(self):
        return repr(self.__skills)

    def __str__(self):
        return str(self.__skills)


class Character(object):
    def __init__(self):
        self.skills = SkillCollection()
        self.group = ServiceGroup()

    def __repr__(self):
        return '\n'.join(`x` for x in self.skills)


def pick_svc_group():
    group = weighted_groups[random.randint(0, 19)]
    
    # There are some special cases we need to handle
    if group[1] == 'Armed Forces' and random.randint(0, 2) == 0: # ~33% chance of not having a firm
        return (group[1], None, None, None)
    elif group[1] == 'Internal Security' and random.randint(0, 1) == 0: # 50% of spying
        cover = pick_svc_group()
        return (cover[1], get_svc_firm(group[2]), 'Internal Security', None)
    elif group[1] == 'Industrial spy or saboteur':
        spyfor = pick_svc_group()
        print spyfor
        spyon = pick_svc_group()
        print spyon
        return ('Industrial spy or saboteur', None, ServiceGroup(spyfor), ServiceGroup(spyon))
    else:
        return (group[1], get_svc_firm(group[2]), None, None)
        

def get_svc_firm(group):
    return random.choice(globals()[group+'_firms'])

def make_random_char():
    char = Character()

    for skill in char.skills:
        # set skill base ratings
        rating = random.randint(1, 20) // 3
        if rating < 4:
            rating = 4
        for spec in skill:
            skill[spec] = rating

# Here we want a list of all the skills a character might have.
# The generator expression gives us an iterator over each list, and reduce
# adds each item to the final list
    tmp_spec_list = reduce(operator.add, (globals()[x] for x in globals() if x[-6:] == '_specs'))

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
    char.group = ServiceGroup(pick_svc_group())
    
    return char