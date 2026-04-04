from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Follow

@receiver(post_save, sender=Follow)
def increase_follow_counts(sender, instance, created, **kwargs):
    if created:
        instance.follower.following_count = F("following_count") + 1
        instance.follower.save(update_fields=["following_count"])

        instance.following.followers_count = F("followers_count") + 1
        instance.following.save(update_fields=["followers_count"])


@receiver(post_delete, sender=Follow)
def decrease_follow_counts(sender, instance, **kwargs):
    instance.follower.following_count = F("following_count") - 1
    instance.follower.save(update_fields=["following_count"])

    instance.following.followers_count = F("followers_count") - 1
    instance.following.save(update_fields=["followers_count"])
