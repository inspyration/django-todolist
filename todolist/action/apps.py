"""## App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ActionConfig(AppConfig):
    """Basic configuration class"""

    name = "action"
    verbose_name = _("action")

    def ready(self):
        import_module("{}.signals".format(self.name))
