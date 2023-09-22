from django.urls import path, re_path, include
from rest_framework import routers
from .controllers import *

router = routers.DefaultRouter()
router.register(r'users', UsersController)
router.register(r'classes', ClassesController)
urlpatterns = router.urls