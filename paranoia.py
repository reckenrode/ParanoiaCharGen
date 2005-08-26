#! /usr/bin/env python

import random

management_specs = [ "bootlicking", "chutzpah", "hygiene", "con games",
                         "interrogation", "intimidation", "moxie", "oratory" ]

stealth_specs = [ "concealment", "disguise", "high alert",
                  "security systems", "shadowing", "slight of hand",
                  "sneaking", "surveilance" ]

violence_specs = [ "agility", "energy weapons", "demolition",
                   "field weapons", "fine manipulation", "hand weapons",
                   "projectile weapons", "thrown weapons",
                   "unarmed combat", "vehicular combat" ]

hardware_specs = [ "bot ops & maintenance", "chemical engineering",
                   "electronic engineering", "habitat engineering",
                   "mechanical engineering", "nuclear engineering",
                   "vehicle ops & maintenance",
                   "weapons & armor maintenance"]

software_specs = [ "bot programming", "c-bay", "data analysis",
                   "data search", "financial systems", "hacking",
                   "operating systems", "vehicle programming" ]

wetware_specs = [ "biosciences", "bioweapons", "cloning", "medical",
                  "outdoor life", "pharmatherapy", "psychotherapy",
                  "suggestion" ]

action_skills = ["management", "stealth", "violence"]
knowledge_skills = ["hardware", "software", "wetware"]


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
        return "%s: %i, %s" % (self.name, self.value, self.__specs)


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

    def __repr__(self):
        return '\n'.join(`x` for x in self)


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
    tmp_spec_list = reduce(lambda x, y: x+y, (globals()[x] for x in globals() if x[-6:] == '_specs'))

    random.shuffle(tmp_spec_list)
    tmp_spec_list.remove("energy weapons")

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

    return char