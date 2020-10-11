from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superUser(
            email='admin@user.com',
            password='pas123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@simple.com',
            password='pass123',
            name='userName'
        )

    def test_user_listed(self):
        """Test that user are listed on user page"""
        url = reverse('admin:main_app_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page works,
         we are testing just our code change
        """

        url = reverse('admin:main_app_user_change', args=[self.user.id])
        # /admin/core/user/(args)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page workds"""
        url = reverse('admin:main_app_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)