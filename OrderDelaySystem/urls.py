
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendor/', include('vendor.urls')),
    path('api/order/', include('order.urls')),

]
