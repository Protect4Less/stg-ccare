from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib import admin
from django.urls import include,path,re_path

urlpatterns = [
	re_path('', include('pages.urls')),
	re_path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
   	re_path('claim/', include('claim.urls')),
   	re_path('partners/', include('partners.urls')),

	re_path('login/', LoginView.as_view(), name='login'),
	
]
