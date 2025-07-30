from decouple import config
DJANGO_ENV = config("DJANGO_ENV", default='development')

print(f"DJANGO_ENV: {DJANGO_ENV}")

if DJANGO_ENV == 'production':
    from .production import *
elif DJANGO_ENV == 'testing':
    from .testing import *
else:
    from .development import *
