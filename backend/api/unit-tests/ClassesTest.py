from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from api.models import Class, User, ClassMember
from rest_framework_simplejwt.tokens import RefreshToken

class ClassesTest(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create(
            email='superuser@example.com',
            password='superuserpassword',
            first_name='Super',
            last_name='User',
            is_superuser=True
        )
        
        # Create a regular user
        self.user = User.objects.create(
            email='user@example.com',
            password='userpassword',
            first_name='Regular',
            last_name='User',
            is_superuser=False
        )

        # Create JWT tokens for authentication
        self.superuser_refresh_token = RefreshToken.for_user(self.superuser)
        self.superuser_access_token = str(self.superuser_refresh_token.access_token)

        self.user_refresh_token = RefreshToken.for_user(self.user)
        self.user_access_token = str(self.user_refresh_token.access_token)

        # Initialize the API client with authentication headers
        self.client_superuser = APIClient()
        self.client_superuser.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_access_token}')

        self.client_user = APIClient()
        self.client_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_access_token}')

    def test_create_class_as_teacher(self):
        url = reverse('classes')
        data = {
            'name': 'Math 101',
            'sections': 'A',
            'schedule': 'MWF 9:00 AM - 10:00 AM',
            'class_code': '12345678'
        }

        response = self.client_superuser.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_retrieve_class(self):
    #     # Create a class instance first (you may need to adjust this according to your model)
    #     new_class = Class.objects.create(
    #         name='Math 101',
    #         sections='A',
    #         schedule='MWF 9:00 AM - 10:00 AM'
    #     )

    #     url = reverse('class-detail', args=[new_class.id])

    #     response = self.client_superuser.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_list_classes_as_superuser(self):
    #     self.user.is_superuser = True
    #     self.user.save()
    #     response = self.client.get(reverse('classes'))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    # def test_retrieve_class(self):
    #     class_obj = Class.objects.create(
    #         name='Math',
    #         sections='A',
    #         schedule='MWF 10:00 AM - 11:00 AM',
    #         class_code='12345678'
    #     )
    #     response = self.client.get(reverse('classes', args=[class_obj.id]))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_class(self):
    #     class_obj = Class.objects.create(
    #         name='Math',
    #         sections='A',
    #         schedule='MWF 10:00 AM - 11:00 AM',
    #         class_code='12345678'
    #     )
    #     data = {
    #         'name': 'Physics',
    #         'sections': 'B',
    #         'schedule': 'TTH 2:00 PM - 3:30 PM',
    #         'class_code': '87654321'
    #     }
    #     response = self.client.put(reverse('classes', args=[class_obj.id]), data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     class_obj.refresh_from_db()
    #     self.assertEqual(class_obj.name, 'Physics')
    #     self.assertEqual(class_obj.sections, 'B')
    #     self.assertEqual(class_obj.schedule, 'TTH 2:00 PM - 3:30 PM')
    #     self.assertEqual(class_obj.class_code, '12345678')  # class_code should be read-only

    # def test_partial_update_class(self):
    #     class_obj = Class.objects.create(
    #         name='Math',
    #         sections='A',
    #         schedule='MWF 10:00 AM - 11:00 AM',
    #         class_code='12345678'
    #     )
    #     data = {
    #         'sections': 'B'
    #     }
    #     response = self.client.patch(reverse('classes', args=[class_obj.id]), data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     class_obj.refresh_from_db()
    #     self.assertEqual(class_obj.sections, 'B')

    # def test_delete_class(self):
    #     class_obj = Class.objects.create(
    #         name='Math',
    #         sections='A',
    #         schedule='MWF 10:00 AM - 11:00 AM',
    #         class_code='12345678'
    #     )
    #     response = self.client.delete(reverse('classes', args=[class_obj.id]))
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Class.objects.filter(id=class_obj.id).exists())

    
