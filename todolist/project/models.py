"""# Models"""

from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    SlugField,
    PROTECT,
)
from django.utils.translation import ugettext_lazy as _

from category.models import Category


class Project(Model):
    """
    ## Project

    This object represent an project of transactions (this is a revealing level of aggregation).
    """

    category = ForeignKey(
        verbose_name=_("category"),
        related_name="project_set",
        to=Category,
        blank=True,
        db_index=True,
        on_delete=PROTECT,
    )

    name = CharField(
        verbose_name=_("name"),
        max_length=32,
        blank=False,
        null=False,
        unique=True,
        db_index=True,
    )

    slug = SlugField(
        unique=True,
        max_length=32,
        editable=True,
        db_index=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.name

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.name)

    class Meta:  # pylint: disable=too-few-public-methods
        """Project Meta class"""

        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ("name",)
        index_together = (("category", "name"),)
