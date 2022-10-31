from django.test import TestCase

from accounts.tests.factories.users import UserFactory
from accounts.tests.factories.profiles import LegalFactory, NaturalFactory

class FactoryTests(TestCase):
    def test_base_user_is_valid(self):
        user = UserFactory.build()

        self.assertEqual(user.full_clean(), None)

    def test_base_legal_profile_is_valid(self):
        profile = LegalFactory()

        self.assertEqual(profile.full_clean(), None)

    def test_base_natural_profile_is_valid(self):
        profile = NaturalFactory()

        self.assertEqual(profile.full_clean(), None)
