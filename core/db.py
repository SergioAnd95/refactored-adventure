from gino import Gino

from .loaders import autodiscover_app_module

db = Gino()
autodiscover_app_module('models')
