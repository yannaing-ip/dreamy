from django.db.models import Q
from .models import Feed
from accounts.models import Follow

def get_visible_feeds(viewer):

    # Anonymous users -> only public
    if not viewer.is_authenticated:
        return Feed.objects.filter(visibility="PL")

    # Get users that viewer follows
    following_ids = Follow.objects.filter(
        follower=viewer
    ).values_list("following_id", flat=True)

    return Feed.objects.filter(
        Q(visibility="PL") |                          # public
        Q(visibility="PR", author__in=following_ids) | # private for followers
        Q(author=viewer)                               # author sees all
    )
