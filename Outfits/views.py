from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .models import ClothingItem
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
from django.http import HttpResponse, HttpRequest
import random
# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'

def DashboardView(request):
    user = request.user
    print(user)
    clothes = {}
    outfit = []
    for item in ClothingItem.objects.filter():
        if item.category not in clothes:
            if item.user == user:
                clothes[item.category] = [item]
        else:
            if item.user == user:
                clothes[item.category].append(item)
    for cat in clothes:
        outfit.append(random.choice(clothes[cat]))
    insufficient = len(clothes.values()) < 2
    return render(request,'dashboard.html',{'myclothes':outfit,'insufficient':insufficient})

class DashboakrdView(ListView):
    model = ClothingItem
    def get_user(request):
        user = request.GET.get('user')
        return user
    def get_context_data(self,**kwargs):
        clothes = {}
        outfit = []
        for item in ClothingItem.objects.filter():
            if item.category not in clothes:
                clothes[item.category] = [item]
            else:
                clothes[item.category].append(item)
        for cat in clothes:
            outfit.append(random.choice(clothes[cat]))
        ctx = super(DashboardView,self).get_context_data(**kwargs)
        ctx['myclothes'] = outfit
        return ctx
    #for cat in clothes:
    #   outfit.append(random.choice(clothes[cat]))
    #print(outfit)
    template_name = 'dashboard.html'


def generated_outfit_view():
    clothes = {}
    for item in ClothingItem.objects.filter():
        if item.category not in clothes:
            clothes[item.category] = [item]
        else:
            clothes[item.category].append(item)
    return clothes
    print(ClothingItem.objects.filter())

class NewItemView(CreateView):
    model = ClothingItem
    template_name = 'newitem.html'
    fields = '__all__'

class MyClothesView(ListView):
    model = ClothingItem
    #print(ClothingItem.objects.filter().first().user)
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
