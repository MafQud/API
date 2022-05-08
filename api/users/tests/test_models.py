from django.test import TestCase

from api.locations.services import populate_govs
from api.users.models import User
from api.users.services import create_user


class UserTests(TestCase):
    @classmethod
    def setUpTestData(cls):  # Called once at the beginning of the test run
        populate_govs()
        create_user(
            name="Osama Yasser",
            username="1005499972",
            password="hardpassword",
            email="osamayasserr@gmail.com",
            firebase_token="token",
            fcm_token="fcm_token",
            gov_id="1",
            city_id="4",
        )

    def test_name_max_lenght(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("name").max_length
        self.assertEqual(max_length, 256)

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_absolute_url(), "/api/users/1/")

    def test_object_name_is_username(self):
        user = User.objects.get(id=1)
        expected_name = user.username
        self.assertEqual(str(user), expected_name)

    def test_user_is_not_verified(self):
        user = User.objects.get(id=1)
        self.assertFalse(user.is_verified)

    def test_user_renew_id_one_year(self):
        user = User.objects.get(id=1)
        user.renew_id(days=365)
        self.assertTrue(user.is_verified)

    def test_user_renew_id_zero_days(self):
        user = User.objects.get(id=1)
        user.renew_id(days=0)
        self.assertFalse(user.is_verified)
