from django.urls import path
from . import views
app_name="report"
urlpatterns = [
    path("report/employee",views.emplyee_Report_View, name="employeeReport"),
    path("report/visit/",views.visit_Report_View, name="visitReport"),
    path("report/offender/",views.offender_Report_View, name="offenderReport"),
    path("report/wood/",views.wood_Report_View, name="woodReport"),
    path("report/tree-Altment/",views.TreeAltment_Report_View, name="treeAltmentwoodReport"),
    path("report/complaints/",views.Complaints_Report_View, name="complaintsReport"),
]
