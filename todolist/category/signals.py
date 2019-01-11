"""App signals module"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from category.models import Category


#
# Receivers
#


@receiver(pre_save, sender=Category, dispatch_uid="category_pre_created")
def category_pre_created(sender, instance, raw, using, update_fields, **kwargs):  # pylint: disable=unused-argument
    """Create slug"""
    if instance.pk:  # Called only on creation
        return

    # from nose.tools import set_trace; set_trace()

    if not instance.slug:
        instance.slug = slugify(instance.name)
