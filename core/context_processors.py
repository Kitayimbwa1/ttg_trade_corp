"""
T&TG Trade Corp — Context Processors
Injects site-wide variables into every template context.
"""


def site_context(request):
    """Global context available in all templates."""
    return {
        'SITE_NAME': 'T&TG Trade Corp',
        'SITE_FULL_NAME': 'Tom & The Group Trade Corp',
        'SITE_PHONE': '+1 (416) 832 3512',
        'SITE_EMAIL': 'tom.grouptradecorp.ca',
        'SITE_ADDRESS': 'M1G 1L8, Toronto, ON, Canada',
        'SITE_FOUNDER': 'Tom Ssembiito',
        'OPERATING_COUNTRIES': [
            ('CA', 'Canada', '🇨🇦'),
            ('UG', 'Uganda', '🇺🇬'),
            ('NL', 'Netherlands', '🇳🇱'),
            ('JP', 'Japan', '🇯🇵'),
            ('KE', 'Kenya', '🇰🇪'),
        ],
    }
