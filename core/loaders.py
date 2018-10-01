import importlib

from settings import settings


def autodiscover_app_module(module_name):
    for app in settings.INSTALLED_APPS:
        importlib.import_module(f'{app}.{module_name}')


def discover_urls():
    """
    Find and return all routes
    from apps
    :return: list
    """
    urlpatterns = []

    for app in settings.INSTALLED_APPS:
        try:
            _temp = __import__(f'{app}.urls', globals(), locals(), ['urlpatterns'], 0)
            urlpatterns += _temp.urlpatterns

        except ModuleNotFoundError:
            pass

    return urlpatterns
