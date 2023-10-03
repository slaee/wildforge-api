from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Class, ClassMember, User
from api.serializers import ClassMemberSerializer

class ClassMembersTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword', first_name='John', last_name='Doe')
        self.client.login(username='testuser@example.com', password='testpassword')
        self.class1 = Class.objects.create(name='Math', sections='A', schedule='MWF 10:00 AM - 11:00 AM', class_code='12345678')
        self.class_member1 = ClassMember.objects.create(user_id=self.user, class_id=self.class1, is_teacher=True, status='accepted')

    def test_create_class_member(self):
        data = {
            'user_id': self.user.id,
            'class_id': self.class1.id,
            'is_teacher': False,
            'status': 'pending'
        }
        response = self.client.post('/api/classmembers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_class_members(self):
        response = self.client.get(f'/api/classes/{self.class1.id}/members/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ClassMemberSerializer(self.class_member1)
        self.assertEqual(response.data, [serializer.data])

    def test_delete_class_member(self):
        response = self.client.delete(f'/api/classmembers/{self.class_member1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ClassMember.objects.filter(id=self.class_member1.id).exists())

    def test_accept_class_member(self):
        self.class_member1.status = 'pending'
        self.class_member1.save()
        response = self.client.put(f'/api/classmembers/{self.class_member1.id}/accept/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.class_member1.refresh_from_db()
        self.assertEqual(self.class_member1.status, 'accepted')
