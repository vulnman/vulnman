
PROJECT_MEMBER_CHOICES = [
    ('pentester', 'Pentester'),
]

INFORMATION_BASIS_CHOICES = [
    ('whitebox', 'White-Box'),
    ('blackbox', 'Black-Box')
]

AGGRESSION_CHOICES = [
    ('passive', 'Passiv scannend'),
    ('careful', 'Vorsichtig'),
    ('balancing', 'Abwägend'),
    ('aggressive', 'Aggressiv')
]

EXTENT_CHOICES = [
    ('complete', 'Vollständig'),
    ('limited', 'Begrenzt'),
    ('focused', 'Fokussiert')
]

APPROACH_CHOICES = [
    ('hidden', 'Verdeckt'),
    ('obvious', 'Offensichtlich')
]

TECHNIQUE_CHOICES = [
    ('network', 'Netzwerkzugang'),
    ('misc_comm', 'Sonstige Kommunikation'),
    ('physical', 'Physischer Zugang'),
    ('se', 'Social Engineering')
]

STARTING_POINT_CHOICES = [
    ('outside', 'Von außen'),
    ('inside', 'Von innen')
]