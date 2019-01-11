"""# App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CategoryConfig(AppConfig):
    """Basic configuration class"""

    name = 'category'
    verbose_name = _("category")

    def ready(self):
        import_module("{}.signals".format(self.name))
