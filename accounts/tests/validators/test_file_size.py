from tempfile import NamedTemporaryFile
from django.core.validators import ValidationError
from django.db.models.fields.files import File
from django.utils.translation import gettext_lazy as _

import pytest

from accounts.validators.file_size import FileSizeValidator


@pytest.fixture
def tmp_file():
    with NamedTemporaryFile(mode='w+') as file:
        file.write('00')  # size of 2 bytes
        file.seek(0)
        yield File(file)


@pytest.mark.debug
def test_message_feedback(tmp_file):
    with pytest.raises(ValidationError) as excinfo:
        max_size = 1
        FileSizeValidator(max_size).__call__(tmp_file)

    expected_msg = _(
        "This file is {file_size} bytes, but cannot be larger than {max_size} bytes"
    ).format(max_size=max_size, file_size=tmp_file.size)
    assert excinfo.value.message == expected_msg
