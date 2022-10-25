from django.contrib.auth.models import User
import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda user: f'{user.first_name}_{user.last_name}')
    password = factory.PostGenerationMethodCall('set_password', 'passpass')

    class Params:
        with_natural_profile = factory.Trait(
            profile=factory.RelatedFactory(
                'accounts.tests.factories.profiles.NaturalFactory',
                factory_related_name='user'
            )
        )
        with_legal_profile = factory.Trait(
            profile=factory.RelatedFactory(
                'accounts.tests.factories.profiles.LegalFactory',
                factory_related_name='user'
            )
        )
