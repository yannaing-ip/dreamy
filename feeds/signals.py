from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like, Comment

@receiver(post_save, sender=Like)
def increase_like_count(sender, instance, created, **kwargs):
    if created:
        feed = instance.feed
        feed.like_count += 1
        feed.save(update_fields=["like_count"])


@receiver(post_delete, sender=Like)
def decrease_like_count(sender, instance, **kwargs):
    feed = instance.feed
    feed.like_count -= 1
    feed.save(update_fields=["like_count"])

@receiver(post_save, sender=Comment)
def increase_comment_count(sender, instance, created, **kwargs):
    if created:
        feed = instance.feed
        feed.comment_count += 1
        feed.save(update_fields=["comment_count"])


@receiver(post_delete, sender=Comment)
def decrease_comment_count(sender, instance, **kwargs):
    feed = instance.feed
    feed.comment_count -= 1
    feed.save(update_fields=["comment_count"])
