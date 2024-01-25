from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import homeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='account')),
    path('account/', include('allauth.urls')),
    path('employee/', include('Apps.employees.urls', namespace="employees")),
    path('core/', include('Apps.core.urls', namespace="core")),
    path('income-expense/', include('Apps.incomeExpence.urls', namespace="incomeExpense")),
    path('offender/', include('Apps.offender.urls')),
    path('complaint/', include('Apps.complaints.urls')),
    path('wood/', include('Apps.wood.urls', namespace="wood")),
    path('employee/', include('Apps.report.urls', namespace="report")),
    path('', homeView.as_view(), name="home")
    
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
