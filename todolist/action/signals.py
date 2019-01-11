"""App signals module"""
from django.db.models import Max
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from action.models import Action, Event, RecurrentAction, Note, Step, Log


#
# Receivers
#


@receiver(pre_save, sender=Action, dispatch_uid="action_pre_created")
@receiver(pre_save, sender=Event, dispatch_uid="event_pre_created")
@receiver(pre_save, sender=RecurrentAction, dispatch_uid="recurrent_action_pre_created")
def action_pre_created(sender, instance, raw, using, update_fields, **kwargs):  # pylint: disable=unused-argument
    """Create name and slug"""
    if instance.pk:  # Called only on creation
        return

    # from nose.tools import set_trace; set_trace()

    instance.name = "{} {} – {}".format(instance.priority[0], instance.project.name, instance.label)

    if not instance.slug:
        instance.slug = slugify(instance.project.name + "__" + instance.label)


@receiver(post_save, sender=Action, dispatch_uid="action_post_save")
@receiver(post_save, sender=Event, dispatch_uid="event_post_save")
@receiver(post_save, sender=RecurrentAction, dispatch_uid="recurrent_action_post_save")
def action_post_save(sender, instance, created, raw, using, update_fields,
                     **kwargs):  # pylint: disable=unused-argument,too-many-arguments
    """Create the first log when an action is created."""
    if not created:
        return

    Log.objects.create(action=instance, date=now(), content=_("Creation of the action"))


@receiver(pre_save, sender=Note, dispatch_uid="note_pre_created")
@receiver(pre_save, sender=Step, dispatch_uid="step_pre_created")
@receiver(pre_save, sender=Log, dispatch_uid="log_pre_created")
def inline_pre_created(sender, instance, raw, using, update_fields, **kwargs):  # pylint: disable=unused-argument
    """Create number"""
    if instance.pk:  # Called only on creation
        return

    # from nose.tools import set_trace; set_trace()

    instance.number = (instance.action.note_set.aggregate(Max('number'))["number__max"] or 0) + 1
