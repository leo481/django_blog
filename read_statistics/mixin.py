from django.contrib.contenttypes.models import ContentType
from .models import ReadNum
from django.db.models.fields import exceptions

class ReadNumMixin():
    def get_read_num(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            read_num = ReadNum.objects.get(content_type=content_type, object_id=self.pk)
            return read_num.read_num
        except exceptions.ObjectDoesNotExist as err:
            return 0
        