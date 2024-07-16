from os import environ
SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='firstpriceauction', num_demo_participants=None, app_sequence=['Firstpriceauction']), dict(name='secondpriceauction', num_demo_participants=None, app_sequence=['Secondpriceauction']), dict(name='nodisclosure', num_demo_participants=None, app_sequence=['nodisclosure'])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']


