"""# App configuration details"""


from importlib import import_module

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectConfig(AppConfig):
    """Basic configuration class"""

    name = 'project'
    verbose_name = _("project")

    def ready(self):
        import_module("{}.signals".format(self.name))
