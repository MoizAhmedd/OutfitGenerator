from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .models import ClothingItem
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class NewItemView(CreateView):
    model = ClothingItem
    template_name = 'newitem.html'
    fields = '__all__'

class MyClothesView(ListView):
    model = ClothingItem
    print(ClothingItem.objects.filter().first().user)
    template_name = 'myclothes.html'
    context_object_name = 'clothes'


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username,password=raw_password)
            login(request,user)
            return redirect('/')

    else:
        form = SignUpForm()

    return render(request,'registration/signup.html',{'form':form})
