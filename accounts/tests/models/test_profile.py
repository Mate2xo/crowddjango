from tempfile import NamedTemporaryFile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from accounts.tests.factories.profiles import NaturalFactory


@pytest.fixture
def valid_img():
    with NamedTemporaryFile(mode='w+', suffix='.png') as img:
        yield SimpleUploadedFile(img.name, None)


@pytest.fixture
def invalid_img():
    with NamedTemporaryFile(suffix='.pdf') as img:
        yield SimpleUploadedFile(img.name, None)


@pytest.mark.django_db
def test_validate_avatar_mime_type(valid_img, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    profile = NaturalFactory(avatar=valid_img)
    assert profile.full_clean() is None


@pytest.mark.django_db
def test_invalidate_avatar_mime_type(invalid_img, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    profile = NaturalFactory(avatar=invalid_img)
    with pytest.raises(ValidationError):
        profile.full_clean()


@pytest.mark.django_db
def test_validate_avatar_file_size(valid_img, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    valid_img.write(b'0' * (1024**2))  # simulate size of 1 MB

    profile = NaturalFactory(avatar=valid_img)
    assert profile.full_clean() is None


@pytest.mark.django_db
def test_invalidate_avatar_file_size(valid_img, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    valid_img.write(b'0' * (1024**2 + 1))  # simulate size of 1.000001 MB

    profile = NaturalFactory(avatar=valid_img)
    with pytest.raises(ValidationError):
        profile.full_clean()
