from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@everythingisata.com",
            password="password1"
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@everythingisata.com",
            password="test4321",
            name="Test users full name "
        )

    def test_users_listed(self):
        """Test that users are listed on users page"""
        urls = reverse("admin:core_user_changelist")
        res = self.client.get(urls)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that users edit page works. """
        url = reverse("admin:core_user_change", args=[self.user.id])

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create users page works"""
        url = reverse("admin:core_user_add")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
