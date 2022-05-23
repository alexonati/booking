from django.shortcuts import render, HttpResponse


# Create your views here.

def return_blank(request):
    return render(request, 'landingpage.html')
