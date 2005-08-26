import operator

management_specs = [ 'bootlicking', 'chutzpah', 'hygiene', 'con games',
                     'interrogation', 'intimidation', 'moxie', 'oratory' ]

stealth_specs = [ 'concealment', 'disguise', 'high alert',
                  'security systems', 'shadowing', 'slight of hand',
                  'sneaking', 'surveilance' ]

violence_specs = [ 'agility', 'energy weapons', 'demolition',
                   'field weapons', 'fine manipulation', 'hand weapons',
                   'projectile weapons', 'thrown weapons',
                   'unarmed combat', 'vehicular combat' ]

hardware_specs = [ 'bot ops & maintenance', 'chemical engineering',
                   'electronic engineering', 'habitat engineering',
                   'mechanical engineering', 'nuclear engineering',
                   'vehicle ops & maintenance',
                   'weapons & armor maintenance']

software_specs = [ 'bot programming', 'c-bay', 'data analysis',
                   'data search', 'financial systems', 'hacking',
                   'operating systems', 'vehicle programming' ]

wetware_specs = [ 'biosciences', 'bioweapons', 'cloning', 'medical',
                  'outdoor life', 'pharmatherapy', 'psychotherapy',
                  'suggestion' ]

action_skills = ['management', 'stealth', 'violence']
knowledge_skills = ['hardware', 'software', 'wetware']

# groups is a list of 3-tuples (probability, name, short name)
groups = [(3, 'Armed Forces', 'af'),
          (2, 'Central Processing Unit', 'cpu'),
          (3, 'HPD & Mind Control', 'hpd'),
          (2, 'Internal Security', 'intsec'),
          (3, 'Production, Logistics & Commissary', 'plc'),
          (2, 'Power Services', 'pow'),
          (2, 'Research & Design', 'rnd'),
          (2, 'Technical Services', 'tech'),
          (1, 'Industrial spy or saboteur', 'spy')]

weighted_groups = reduce(operator.add, ([g for w in xrange(g[0])] for g in groups))


af_firms = ['Ammunition Fresheners', 'Armed Forces Friends Network',
             'Bodygaurd Communications Liaisons', 'Blast Shield Maintenance',
             'Crowd Control (Armed Forces)', 'Sensitivity Trainers', 'Threat Assessors (Armed Forces)'
             'Tool & Die Works', 'Vulture Squadron Recruiters', 'DM\u2019s Choice']

cpu_firms = ['116 Emergency Systems', 'Credit License Checkers',
              'Facility Surveillance Control', 'Form Facilitators',
              'Form Inventory Officers', 'Form Disposal Advisors',
              'Pocket Protector Refurbishers', 'Security System Installers',
              'Volunteer Collection Agencies', 'DM\u2019s Choice']
              
hpd_firms = ['Entertainment Scouting Agencies', 'History Purifiers',
              'News Services', 'Public Hating Coordination',
              'Psyche Ward Administration', 'Sector Expansion Surveyors',
              'Semantics Control', 'Singalong Agents', 'Subliminals Police', 'DM\u2019s Choice']
              
intsec_firms = ['Crowd Control (IntSec)', 'Forensic Analysis', 'Glee Quota Adjutants',
                 'Re-Education Client Procurement', 'Surveillance Operatives',
                 'Termination Center Janitorial', 'Thought Surveyors',
                 'Threat Assessors (IntSec)', 'Treason Scene Cleanup', 'DM\u2019s Choice']
                 
plc_firms = ['Armored Autocar Escorts', 'BLUE Room Caterers', 'Equipment Assembly Control',
              'Field Logistics Advisors', 'Food Vat Control', 'Inventory System Updaters',
              'Printing Office Field Checkers', 'Storage Media Integrity Assessors',
              'Warehouse System Inspectors', 'DM\u2019s Choice']
              
pow_firms = ['Battery Backup', 'Bum Radius Assessors', 'Circuit Maintenance',
              'Fuel Cell Replenishment (Power)', 'Fuel Rod Disposal Consultants',
             'Odor Fresheners', 'Power Oscillation Professionals', 'Safe Atoms Initiative',
             'Wire Supply Checkers', 'DM\u2019s Choice']
             
rnd_firms = ['Biological Niceness Indexers', 'Bot Processing', 'Drug Interaction Testers',
              'Field Data Collectors', 'Goo Cleanup', 'RoboPsych Auditing',
              'Scienctist Sanity Checkers', 'Vehicle Therapists',
              'Weapon Effectiveness Assessors', 'DM\u2019s Choice']
              
tech_firms = ['Bedding Inspectors', 'Clone Tank Support Services',
               'Consolidated Motorized Transport (CMT)', 'Fuel Cell Replenishment (Tech Svcs)',
              'MemoMax Quality Assurance', 'Medical Services', 'Paint Control',
              'Slime Identification', 'Tech Support']