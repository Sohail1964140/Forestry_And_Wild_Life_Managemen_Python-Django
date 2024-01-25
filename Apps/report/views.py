from django.http import HttpResponse
from django.shortcuts import render
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template, render_to_string
from Apps.employees.models import EMPLOYEE, VISIT
from Apps.offender.models import Offender
from Apps.wood.models import WoodEntry, TreeAltment
from Apps.complaints.models import Complaints
from django.contrib.auth.decorators import login_required
# Create your views here.

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
def emplyee_Report_View(request):
    
    
    pdf = render_to_pdf('report/employee/employee.html',{'employees': EMPLOYEE.objects.all().order_by("designation")})
    

    resp =  HttpResponse(pdf, content_type='application/pdf')
    
    return resp

@login_required
def Complaints_Report_View(request):
    
    
    if request.method=="POST":

        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        area = request.POST.get("area")
        employee = request.POST.get("employee")
        status = request.POST.get("status")

        complaints = Complaints.objects.filter(date__gte=fromDate, date__lte=toDate)

        if area:
            complaints = complaints.filter(area__pk=area)
            
        if employee:
            complaints = complaints.filter(employee__pk=employee)

        if status:
            complaints = complaints.filter(status=status)

        data = {'complaints': complaints}
        pdf = render_to_pdf('report/complaints/complaints.html',data)
        resp =  HttpResponse(pdf, content_type='application/pdf')

        return resp

    return HttpResponse("Something went wrong.")



@login_required
def TreeAltment_Report_View(request):
    
    
    if request.method=="POST":

        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        area = request.POST.get("area")
        customer = request.POST.get("customer")

        trees = TreeAltment.objects.filter(date__gte=fromDate, date__lte=toDate)

        if customer:
            trees = trees.filter(customer__pk=customer)
        if area:
            trees = trees.filter(area__pk=area)

        data = {'trees': trees}
        pdf = render_to_pdf('report/wood/treeAltment.html',data)
        resp =  HttpResponse(pdf, content_type='application/pdf')

        return resp

    return HttpResponse("Something went wrong.")



@login_required
def wood_Report_View(request):
    
    
    if request.method=="POST":

        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')

        woods = WoodEntry.objects.filter(date__gte=fromDate, date__lte=toDate)
        data = {'woods': woods}
        pdf = render_to_pdf('report/wood/wood.html',data)
        resp =  HttpResponse(pdf, content_type='application/pdf')

        return resp

    return HttpResponse("Something went wrong.")

@login_required
def offender_Report_View(request):
    
    
    if request.method=="POST":

        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')

        offenders = Offender.objects.filter(date__gte=fromDate, date__lte=toDate)
        
        data = {'offenders': offenders}
        pdf = render_to_pdf('report/offender/offender.html',data)
        resp =  HttpResponse(pdf, content_type='application/pdf')

        return resp

    return HttpResponse("Something went wrong.")


@login_required
def visit_Report_View(request):
    
    
    if request.method=="POST":

        area = request.POST.get('area')
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')

        visits = VISIT.objects.filter(forestArea__pk=area).filter(date__gte=fromDate, date__lte=toDate)
        
        data = {'visits': visits}
        pdf = render_to_pdf('report/visit/visit.html',data)
        resp =  HttpResponse(pdf, content_type='application/pdf')

        return resp

    return HttpResponse("Something went wrong.")