from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from .utils import publish_message
from .serializers import ProfileSerializerV1

@receiver(post_save, sender=Profile)
def send_upstream_signal(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    time = "{}".format(datetime.now()).encode()
    instanceType = instance.__class__.__name__
    id = instance.id
    data = ProfileSerializerV1(instance).data
    updated_fields = [] if created else kwargs["updated_fields"]
    data = {
        "action": action,
        "time": time,
        "instanceType": instanceType,
        "id": id,
        "updated_fields": updated_fields
    }
    publish_message(action, data)
