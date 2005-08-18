#! /usr/bin/env python

import random


class Skill(object):
    def __init__(self, name, value, specs):
        self.name = name
        self.value = value
        self.__specs = dict((s, value) for s in specs)

    def __iter__(self):
        return iter(self.__specs)

    def __setitem__(self, idx, val):
        self.__specs[idx] = val

        
    def __getitem__(self, idx):
        return self.__specs[idx]

    def __repr__(self):
        return "%s: %i, %s" % (self.name, self.value, self.__specs)


class Character(object):
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
    
    action_skills = ["management", "stealth", "violence" ]
    knowledge_skills = ["hardware", "software", "wetware" ]

    def __init__(self):
        self.__skills = [Skill(sk, 0, (s for s in Character.__dict__[sk+'_specs']))
                       for sk in Character.action_skills+Character.knowledge_skills]

    def __getattribute__(self, attr):
        for sk in super(Character, self).__getattribute__('_Character__skills'):
            if attr == sk.name:
                return sk
        else:
            return super(Character, self).__getattribute__(attr)

    def __iter__(self):
        return iter(self.__skills)

    def __repr__(self):
        return '\n'.join(`x` for x in self)
    

def make_random_char():
    char = Character()

    for skill in char:
        # set skill base ratings
        rating = random.randint(1, 20) // 3
        if rating < 4:
            rating = 4
        for spec in skill:
            skill[spec] = rating

# Here we want a list of all the skills a character might have.
# The generator expression gives us an iterator over each list, and reduce
# adds each item to the final list
    tmp_spec_list = reduce(lambda x,y: x+y, (Character.__dict__[x] for x in Character.__dict__ if x.find('_spec') != -1))
    
    random.shuffle(tmp_spec_list)
    tmp_spec_list.remove("energy weapons")

    rec_skills = {}
    # boosts
    boosts = 0
    for spec in tmp_spec_list:
        if boosts >= 6:
            break
        for skill in char:
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
        for skill in char:
            if spec in skill:
                if rec_skills.get(skill.name, 0) > 0:
                    rec_skills[skill.name] = rec_skills.get(skill.name, 0) - 1
                    skill[spec] = 1
                    tmp_spec_list.remove(spec)
                    drops -= 1

    # vital speciality!
    char.violence['energy weapons'] += 4

    return char


