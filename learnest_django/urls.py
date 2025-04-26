from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace="base")),
    path('user/', include('user.urls', namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
]
