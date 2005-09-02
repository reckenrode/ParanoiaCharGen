import operator

specs = {
    'management': [ 'bootlicking', 'chutzpah', 'hygiene', 'con games',
                  'interrogation', 'intimidation', 'moxie', 'oratory' ],
    'stealth': [ 'concealment', 'disguise', 'high alert',
                  'security systems', 'shadowing', 'slight of hand',
                  'sneaking', 'surveilance' ],
    'violence': ['agility', 'energy weapons', 'demolition',
                   'field weapons', 'fine manipulation', 'hand weapons',
                   'projectile weapons', 'thrown weapons',
                   'unarmed combat', 'vehicular combat' ],

    'hardware': ['bot ops & maintenance', 'chemical engineering',
                   'electronic engineering', 'habitat engineering',
                   'mechanical engineering', 'nuclear engineering',
                   'vehicle ops & maintenance',
                   'weapons & armor maintenance'],

    'software': ['bot programming', 'c-bay', 'data analysis',
                   'data search', 'financial systems', 'hacking',
                   'operating systems', 'vehicle programming'],

    'wetware': ['biosciences', 'bioweapons', 'cloning', 'medical',
                  'outdoor life', 'pharmatherapy', 'psychotherapy',
                  'suggestion']
}

action_skills = ['management', 'stealth', 'violence']
knowledge_skills = ['hardware', 'software', 'wetware']

groups = {
    'Armed Forces': {
        'weight': 3,
        'firms': ['Ammunition Fresheners', 'Armed Forces Friends Network',
            'Bodygaurd Communications Liaisons', 'Blast Shield Maintenance',
            'Crowd Control', 'Sensitivity Trainers', 'Threat Assessors',
            'Tool & Die Works', 'Vulture Squadron Recruiters'],
         'specs': ['demolition', 'energy weapons', 'hand weapons', 'projectile weapons',
                   'thrown weapons', 'unarmed combat', 'vehicle ops & maintenance']
    },
    'Central Processing Unit': {
        'weight': 2,
        'firms': ['Ammunition Fresheners', 'Armed Forces Friends Network',
            'Bodygaurd Communications Liaisons', 'Blast Shield Maintenance',
            'Crowd Control', 'Sensitivity Trainers', 'Threat Assessors',
            'Tool & Die Works', 'Vulture Squadron Recruiters'],
         'specs': ['security systems', 'electronic engineering', 'bot programming',
                   'data analysis', 'financial systems', 'data search', 'vehicle programming']
    },
    'HPD & Mind Control': {
        'weight': 3,
        'firms': ['Entertainment Scouting Agencies', 'History Purifiers',
             'News Services', 'Public Hating Coordination',
             'Psyche Ward Administration', 'Sector Expansion Surveyors',
             'Semantics Control', 'Singalong Agents', 'Subliminals Police'],
         'specs': ['bootlicking', 'chutzpah', 'con games', 'moxie', 'bot ops & maintenance',
                   'pharmatherapy', 'medical']
    },
    'Internal Security': {
        'weight': 2,
        'firms': ['Crowd Control', 'Forensic Analysis', 'Glee Quota Adjutants',
                    'Re-Education Client Procurement', 'Surveillance Operatives',
                    'Termination Center Janitorial', 'Thought Surveyors',
                    'Threat Assessors', 'Treason Scene Cleanup'],
         'specs': ['interrogation', 'intimidation', 'security systems',
                   'surveilance', 'energy weapons', 'hand weapons', 'unarmed combat']
        },
    'Production, Logistics & Commissary': {
        'weight': 3,
        'firms': ['Armored Autocar Escorts', 'BLUE Room Caterers', 'Equipment Assembly Control',
                 'Field Logistics Advisors', 'Food Vat Control', 'Inventory System Updaters',
                 'Printing Office Field Checkers', 'Storage Media Integrity Assessors',
                 'Warehouse System Inspectors'],
         'specs': ['chutzpah', 'con games', 'bot ops & maintenance', 'habitat engineering',
                   'vehicle ops & maintenance', 'data search', 'biosciences']
    },
    'Power Services': {
        'weight': 2,
        'firms': ['Battery Backup', 'Bum Radius Assessors', 'Circuit Maintenance',
                 'Fuel Cell Replenishment', 'Fuel Rod Disposal Consultants',
                 'Odor Fresheners', 'Power Oscillation Professionals', 'Safe Atoms Initiative',
                 'Wire Supply Checkers'],
         'specs': ['data analysis', 'data search', 'chemical engineering',
                   'electronic engineering', 'habitat engineering', 'mechanical engineering',
                   'nuclear engineering']
    },
    'Research & Design': {
        'weight': 2,
        'firms': ['Biological Niceness Indexers', 'Bot Processing', 'Drug Interaction Testers',
                 'Field Data Collectors', 'Goo Cleanup', 'RoboPsych Auditing',
                 'Scienctist Sanity Checkers', 'Vehicle Therapists',
                 'Weapon Effectiveness Assessors'],
         'specs': ['chemical engineering', 'mechanical engineering', 'nuclear engineering',
                   'bot programming', 'vehicle programming', 'bioweapons', 'cloning']
    },
    'Technical Services': {
        'weight': 2,
        'firms': ['Bedding Inspectors', 'Clone Tank Support Services',
                  'Consolidated Motorized Transport (CMT)', 'Fuel Cell Replenishment',
                  'MemoMax Quality Assurance', 'Medical Services', 'Paint Control',
                  'Slime Identification', 'Tech Support'],
         'specs': ['chemical engineering', 'electronic engineering', 'habitat engineering',
                   'vehicle ops & maintenance', 'bot programming', 'vehicle programming',
                   'pharmatherapy']
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