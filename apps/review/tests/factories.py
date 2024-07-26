import factory
from apps.review.models import Review
from apps.book.tests.factories import BookFactory,UserFactory

class ReviewFactory(factory.django.DjangoModelFactory):
    book = factory.SubFactory(BookFactory)
    user = factory.SubFactory(UserFactory)
    rating = factory.Faker('random_int', min=1, max=5)

    class Meta:
        model = Review
