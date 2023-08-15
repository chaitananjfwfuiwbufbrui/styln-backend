from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from authentications import views
from django.contrib import admin
from django.urls import path
admin.autodiscover()
admin.site.enable_nav_sidebar = False

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from authentications.views import *

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from authentications.views import *
admin.autodiscover()
admin.site.enable_nav_sidebar = False
admin.site.site_header = "phstosher"
admin.site.site_title = "phstosher"
admin.site.index_title = "phstosher"
schema_view = get_schema_view(
   openapi.Info(
      title="phothosher API",
      default_version='v1',
      description="devloped by chaitanya ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kc508275@gmail.com"),
      # license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # path('Auth/GoogleRedirect/', RedirectSocial.as_view()),
    path('swagger/s.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('superuser/', superuser.as_view(), name='superuser'),
    path('admin/', admin.site.urls),
    # path('main/', include('main.urls')),
    path('auth/', include('djoser.urls')),
    path('home/', include('home.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),
    path('api/token/otp/', OTPVerifyView.as_view(), name='otp-login'),
    path('api/otp-login/', OTPLoginAPIView.as_view(), name='otp-login'),
    path('api/token/', PhoneJWTAPIView.as_view(), name='phone-jwt'),
    # path('auth/login/', views.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('superuser/', views.SuperUserAPIView.as_view(), name='token_obtain_pair'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+ static(settings.IMAGES_URL,document_root=settings.IMAGES_ROOT)
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]