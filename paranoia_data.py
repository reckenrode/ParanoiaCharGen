import operator

specs = {
    'Management': ['Bootlicking', 'Chutzpah', 'Hygiene', 'Con Games',
                   'Interrogation', 'Intimidation', 'Moxie', 'Oratory'],
    'Stealth': ['Concealment', 'Disguise', 'High Alert',
                'Security Systems', 'Shadowing', 'Slight of Hand',
                'Sneaking', 'Surveilance'],
    'Violence': ['Agility', 'Energy Weapons', 'Demolition',
                 'Field Weapons', 'Fine Manipulation', 'Hand Weapons',
                 'Projectile Weapons', 'Thrown Weapons',
                 'Unarmed Combat', 'Vehicular Combat'],
    'Hardware': ['Bot Ops & Maintenance', 'Chemical Engineering',
                 'Electronic Engineering', 'Habitat Engineering',
                 'Mechanical Engineering', 'Nuclear Engineering',
                 'Vehicle Ops & Maintenance',
                 'Weapons & Armor Maintenance'],
    'Software': ['Bot Programming', 'C-Bay', 'Data Analysis',
                 'Data Search', 'Financial Systems', 'Hacking',
                 'Operating Systems', 'Vehicle Programming'],
    'Wetware': ['Biosciences', 'Bioweapons', 'Cloning', 'Medical',
                'Outdoor Life', 'Pharmatherapy', 'Psychotherapy',
                'Suggestion']
}

action_skills = ['Management', 'Stealth', 'Violence']
knowledge_skills = ['Hardware', 'Software', 'Wetware']

groups = {
    'Armed Forces': {
        'weight': 3,
        'firms': ['Ammunition Fresheners', 'Armed Forces Friends Network',
                  'Bodygaurd Communications Liaisons', 'Blast Shield Maintenance',
                  'Crowd Control', 'Sensitivity Trainers', 'Threat Assessors',
                  'Tool & Die Works', 'Vulture Squadron Recruiters'],
        'specs': ['Demolition', 'Energy Weapons', 'Hand Weapons', 'Projectile Weapons',
                   'Thrown Weapons', 'Unarmed Combat', 'Vehicle Ops & Maintenance'],
        'societies': [(3, 'Anti-Mutant'), (3, 'Death Leopard'), (3, 'Frankenstein Destroyers'),
                      (3, 'PURGE'), (1, 'Communists'), (1, 'FCCC-P'), (1, 'Free Enterprise'),
                      (1, 'Pro Tech'), (1, 'Psion'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Central Processing Unit': {
        'weight': 2,
        'firms': ['Ammunition Fresheners', 'Armed Forces Friends Network',
                  'Bodygaurd Communications Liaisons', 'Blast Shield Maintenance',
                  'Crowd Control', 'Sensitivity Trainers', 'Threat Assessors',
                  'Tool & Die Works', 'Vulture Squadron Recruiters'],
        'specs': ['Security Systems', 'Electronic Engineering', 'Bot Programming',
                   'Data Analysis', 'Financial Systems', 'Data Search', 'Vehicle Programming'],
        'societies': [(4, 'Computer Phreaks'), (4, 'Corpore Metal'), (2, 'FCCC-P'),
                      (2, 'Sierra Club'), (1, 'Anti-Mutant'), (1, 'Communists'), (1, 'Pro Tech'),
                      (1, 'Psion'), (1, 'PURGE'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'HPD & Mind Control': {
        'weight': 3,
        'firms': ['Entertainment Scouting Agencies', 'History Purifiers',
                  'News Services', 'Public Hating Coordination',
                  'Psyche Ward Administration', 'Sector Expansion Surveyors',
                  'Semantics Control', 'Singalong Agents', 'Subliminals Police'],
        'specs': ['Bootlicking', 'Chutzpah', 'Con Games', 'Moxie', 'Bot Ops & Maintenance',
                  'Pharmatherapy', 'Medical'],
        'societies': [(2, 'Anti-Mutant'), (2, 'FCCC-P'), (3, 'Humanists'),
                      (4, 'Romantics'), (2, 'Sierra Club'), (1, 'Communists'), (1, 'Mystics'),
                      (1, 'Psion'), (1, 'PURGE'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Internal Security': {
        'weight': 2,
        'firms': ['Crowd Control', 'Forensic Analysis', 'Glee Quota Adjutants',
                  'Re-Education Client Procurement', 'Surveillance Operatives',
                  'Termination Center Janitorial', 'Thought Surveyors',
                  'Threat Assessors', 'Treason Scene Cleanup'],
        'specs': ['Interrogation', 'Intimidation', 'Security Systems',
                  'Surveilance', 'Energy Weapons', 'Hand Weapons', 'Unarmed Combat'],
        'societies': [(3, 'Anti-Mutant'), (3, 'Death Leopard'), (3, 'FCCC-P'),
                      (3, 'Frankenstein Destroyers'), (1, 'Communists'), (1, 'Free Enterprise'), (1, 'Pro Tech'),
                      (1, 'Psion'), (1, 'PURGE'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Production, Logistics & Commissary': {
        'weight': 3,
        'firms': ['Armored Autocar Escorts', 'BLUE Room Caterers', 'Equipment Assembly Control',
                  'Field Logistics Advisors', 'Food Vat Control', 'Inventory System Updaters',
                  'Printing Office Field Checkers', 'Storage Media Integrity Assessors',
                  'Warehouse System Inspectors'],
        'specs': ['Chutzpah', 'Con Games', 'Bot Ops & Maintenance', 'Habitat Engineering',
                  'Vehicle Ops & Maintenance', 'Data Search', 'Biosciences'],
        'societies': [(5, 'Free Enterprise'), (3, 'Humanists'), (2, 'Mystics'),
                      (2, 'Romantics'), (1, 'Communists'), (1, 'Pro Tech'), (1, 'Psion'),
                      (1, 'Sierra Club'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Power Services': {
        'weight': 2,
        'firms': ['Battery Backup', 'Bum Radius Assessors', 'Circuit Maintenance',
                  'Fuel Cell Replenishment', 'Fuel Rod Disposal Consultants',
                  'Odor Fresheners', 'Power Oscillation Professionals', 'Safe Atoms Initiative',
                  'Wire Supply Checkers'],
        'specs': ['Data Analysis', 'Data Search', 'Chemical Engineering',
                  'Electronic Engineering', 'Habitat Engineering', 'Mechanical Engineering',
                  'Nuclear Engineering'],
        'societies': [(2, 'Computer Phreaks'), (2, 'Death Leopard'), (2, 'FCCC-P'),
                      (2, 'Frankenstein Destroyers'), (2, 'Free Enterprise'), (2, 'Mystics'), (2, 'Pro Tech'),
                      (2, 'PURGE'), (1, 'Communists'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Research & Design': {
        'weight': 2,
        'firms': ['Biological Niceness Indexers', 'Bot Processing', 'Drug Interaction Testers',
                  'Field Data Collectors', 'Goo Cleanup', 'RoboPsych Auditing',
                  'Scienctist Sanity Checkers', 'Vehicle Therapists',
                  'Weapon Effectiveness Assessors'],
        'specs': ['Chemical Engineering', 'Mechanical Engineering', 'Nuclear Engineering',
                  'Bot Programming', 'Vehicle Programming', 'Bioweapons', 'Cloning'],
        'societies': [(3, 'Computer Phreaks'), (3, 'Corpore Metal'), (3, 'Pro Tech'),
                      (3, 'Psion'), (3, 'PURGE'), (1, 'FCCC-P'), (1, 'Communists'),
                      (1, 'Illuminati'), (1, 'Spy')]
    },
    'Technical Services': {
        'weight': 2,
        'firms': ['Bedding Inspectors', 'Clone Tank Support Services',
                  'Consolidated Motorized Transport (CMT)', 'Fuel Cell Replenishment',
                  'MemoMax Quality Assurance', 'Medical Services', 'Paint Control',
                  'Slime Identification', 'Tech Support'],
        'specs': ['Chemical Engineering', 'Electronic Engineering', 'Habitat Engineering',
                  'Vehicle Ops & Maintenance', 'Bot Programming', 'Vehicle Programming',
                  'Pharmatherapy'],
        'societies': [(2, 'Computer Phreaks'), (2, 'Corpore Metal'), (2, 'Death Leopard'),
                      (2, 'Frankenstein Destroyers'), (2, 'Mystics'), (2, 'Pro Tech'), (2, 'Psion'),
                      (2, 'Sierra Club'), (1, 'Communists'), (1, 'Illuminati'), (1, 'Spy')]
    },
    'Industrial spy or saboteur': {
        'weight': 1,
        'firms': [],
        'specs': []
    }
}

weighted_groups = reduce(operator.add, [[g for w in xrange(v['weight'])] for g, v in groups.iteritems()])

powers = {
    'classic': ['Charm', 'Corrosion', 'Detect Mutant Power', 'Electroshock', 'Empathy',
                'Energy Field', 'Hypersenses', 'Levitation', 'Machine Empathy',
                'Matter Eater', 'Mental Blast', 'Polymorphism', 'Puppeteer',
                'Pyrokinesis', 'Regeneration', 'Slippery Skin', 'Telekinesis',
                'Teleportation', 'Uncanny Luck', 'X-Ray Vision'],                  
    'straight': ['Adhesive Skin', 'Adrenalin Control', 'Bureaucratic Intuition',
                 'Charm', 'Death Simulation', 'Deep Thought', 'Electroshock',
                 'Empathy', 'Energy Field', 'Hypersenses', 'Machine Empathy',
                 'Matter Eater', 'Mechanical Intuition', 'Mental Blast',
                 'Pyrokinesis', 'Regeneration', 'Rubbery Bones', 'Toxic Metabolism',
                 'Uncanny Luck', 'Ventriloquist'],
    'zap': ['Absorption', 'Chameleon', 'Charm', 'Desolidity', 'Electroshock',
            'Energy Field', 'Growth', 'Levitation', 'Machine Empathy',
            'Matter Eater', 'Mental Blast', 'Polymorphism', 'Puppeteer',
            'Pyrokinesis', 'Regeneration', 'Shrinking', 'Telekinesis',
            'Teleportation', 'Transmutaiton', 'X-Ray Vision']
}

# A skill of 'M' indicates the next is mandatory for that society                
societyskills = [#              Uncommon                                     Unlikely                                        Unhealthy
    ['Anti-Mutant',            'Power Studies',                             'Comic Book Trivia',                            'Twitchtalk'],
    ['Computer Phreaks',       'Cash Hacking',                              'Jargon',                                      ('Hacking', 'programming skills')],
    ['Communists',             'Demolition',                                'Tractor Maintenance',                    ('M', 'Propaganda')],
    ['Corpore Metal',          'Cyborging',                                 'Botspotting',                                  'Bioweapons'],
    ['Death Leopard',    ('M', 'Demolition'),                              ('Action Movies', 'Partying'),                   'Gambling'],
    ['FCCC-P',                 'Alpha Complex History',                     'priestly skills',                              'Meeting Machine Empaths'],
    ['Frankenstein Destroyers', 'Demolition',                               'toolmaking skills',                            'programming skills'],
    ['Free Enterprise',        'Haggling',                                  'Advertising & Marketing',                     ('Bribery', 'Forgery')],
    ['Humanists',              'Marital Arts',                             ('hobbies', 'languages'),                        'Old Reckoning Cultures'],
    ['Mystics',          ('M', 'Drug Procurement'),                        ('Meditation', 'Partying'),                      'Old Reckoning Drugs'],
    ['Pro Tech',               'Experimental Equipment Repair',             'Video Games',                                  'WMD'],
    ['Psion',                  'Power Studies',                             'Comic Book Trivia',                            'Twitchtalk'],
    ['PURGE',            ('M', 'Demolition'),                               'Gloating',                                    ('Bioweapons', 'Twitchtalk')],
    ['Romantics',              'Archival Studies',                         ('Cooking', 'Knitting', 'Music'),          ('M', 'Old Reckoning Cultures')],
    ['Sierra Club',            ('Survial', 'Wild Lore', 'Travel'),         ('Birdwatching', 'Botany', 'Spoor Recognition'), 'Bioweapons']
]