from django.shortcuts import render
from app.models import Profession

# Create your views here.
def index_page(request):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(request, 'index.html', context=data)