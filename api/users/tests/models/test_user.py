from django.core.exceptions import ValidationError
from django.test import TestCase

from api.users.models import User


class UserTests(TestCase):
    def test_username_is_phone_number(self):
        user = User(
            username="cool_username",
            name="Osama Yasser",
            firebase_token="token",
        )
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_default_id_expiration_date(self):
        user = User(
            username="1005469972",
            name="Osama Yasser",
            firebase_token="token",
        )
        user.save()
        self.assertIsNone(user.id_exp_date)
