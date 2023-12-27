import random


chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
size = 80
secret_key = "".join(random.sample(chars,size))


CONFIG_STRING="""
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS= *
DATABASE_URL=sqlite:///db.sqlite3
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
STATIC_ROOT = 'static'
MEDIA_ROOT ='media'

""".strip() % (secret_key)

with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)

print('Success!')
print('Type: cat .env')
