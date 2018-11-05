import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ge-heim-pje_D0t_nie-mand_00it_zal_ra-den'