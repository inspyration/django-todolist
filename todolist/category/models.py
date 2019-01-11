"""# Models"""

from django.db.models import (
    Model,
    CharField,
    SlugField,
)
from django.utils.translation import ugettext_lazy as _


class Category(Model):
    """
    ## Source's categories

    This object is an bigger level of aggregation.
    """

    name = CharField(
        verbose_name=_("Name"),
        max_length=16,
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
        """Category Meta class"""

        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("name",)
