"""# App configuration details"""


from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProjectConfig(AppConfig):
    """Basic configuration class"""

    name = 'project'
    verbose_name = _("project")
