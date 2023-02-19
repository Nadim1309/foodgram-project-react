from django.urls import include, path

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
]
