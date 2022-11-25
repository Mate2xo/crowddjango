from tempfile import NamedTemporaryFile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
import pytest
from accounts.models import Natural, Profile
from accounts.tests.factories.profiles import NaturalFactory


@pytest.fixture
def valid_img():
    with NamedTemporaryFile(suffix='.png') as img:
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
