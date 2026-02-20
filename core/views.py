from django.shortcuts import HttpResponse

def home(request):
        return HttpResponse("<h1>HelloM</h1>")

# Create your views here.
