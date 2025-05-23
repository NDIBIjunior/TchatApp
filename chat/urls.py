from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("<str:room_name>/<str:user_name>/", views.room, name="room"),
    path("upload/", views.upload_file, name='upload'),
    path('test_ui/', views.test_ui, name='test_ui'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
