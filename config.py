class Config(object):
    DEBUG = False


class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
