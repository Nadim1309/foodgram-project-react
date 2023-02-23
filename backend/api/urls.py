from api.views import FollowViewSet, IngredientsViewSet, TagsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('ingredients/', IngredientsViewSet)
router.register('users', FollowViewSet)
router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
