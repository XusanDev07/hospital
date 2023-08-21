from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.

@login_required(login_url='login')
def index(req):
    return render(req, 'pages/index.html')
