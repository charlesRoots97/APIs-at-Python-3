import os

class Configuration(object):
    #   APPLICATION_DIR = os_path.dirname(os.path.realpath(__file__))
      DEBUG = True
      SECRET_KEY = 'CHARLES'
    #   STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    #   IMAGES_DIR = os.path.join(APPLICATION_DIR, 'images')

    #   IMGS_USERS = os.path.join(APPLICATION_DIR, 'users')
      ALLOWED_IMGS = set(['jpg','jpeg','png'])