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
        self.teacher = User.objects.create(
            email='teacher@example.com',
            password='userpassword',
            first_name='Teacher',
            last_name='User',
            is_staff=True
        )

        self.student = User.objects.create(
            email='student@example.com',
            password='userpassword',
            first_name='Student',
            last_name='User'
        )


        # Create JWT tokens for authentication

        superuser_refresh = RefreshToken.for_user(self.superuser)
        self.superuser_auth = {
            'refresh': superuser_refresh,
            'access': str(superuser_refresh.access_token)
        }

        teacher_refresh = RefreshToken.for_user(self.teacher)
        self.teacher_auth = {
            'refresh': teacher_refresh,
            'access': str(teacher_refresh.access_token)
        }

        student_refresh = RefreshToken.for_user(self.student)
        self.student_auth = {
            'refresh': student_refresh,
            'access': str(student_refresh.access_token)
        }

        # Initialize the API client with authentication headers
        self.client_superuser = APIClient()
        self.client_superuser.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_auth.get("access")}')

        self.client_teacher_user = APIClient()
        self.client_teacher_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_auth.get("access")}')

        self.client_student_user = APIClient()
        self.client_student_user.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_auth.get("access")}')

    def test_create_class_as_teacher(self):
        url = reverse('classes')
        data = {
            'name': 'Math 101',
            'sections': 'A',
            'schedule': 'MWF 9:00 AM - 10:00 AM',
            'class_code': '12345678'
        }

        response = self.client_teacher_user.post(url, data, format='json')
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

    
