from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from .controllers import *

router = routers.DefaultRouter()
router.register(r'users', UsersController)
router.register(r'classes', ClassesController)

classes_router = routers.NestedSimpleRouter(router, r'classes', lookup='class')
classes_router.register(r'members', ClassMembersController, basename='class-members')

urlpatterns = router.urls
urlpatterns += classes_router.urls

urlpatterns += [
    path('tokens/', include([
        path('acquire/', TokensController.as_view(), name='acquire_token_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),
        path('verify/', TokenVerifyView.as_view(), name='verify_token'),
    ])),
]