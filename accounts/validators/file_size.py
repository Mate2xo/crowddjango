from django.core.validators import MaxValueValidator, ValidationError
from django.db.models.fields.files import FieldFile
from django.utils.translation import gettext as _


class FileSizeValidator:
    message = _("This file is {file_size} bytes, but cannot be larger than {max_size} bytes")

    def __init__(self, max_size=None) -> None:
        if max_size is None:
            max_size = 1024**2 * 10  # 10 MB
        self.max_size = max_size

    def __call__(self, file: FieldFile) -> None:
        if file.size > self.max_size:
            formatted_msg = self.message.format(max_size=self.max_size, file_size=file.size)
            raise ValidationError(formatted_msg,
                                  code='invalid_size',
                                  params={
                                      'max_size': self.max_size,
                                      'file_size': file.size
                                  }
                                  )
