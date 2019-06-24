from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core import serializers
from .models import ClothingItem, BadOutfit
from django.contrib.auth import authenticate,login
from .forms import SignUpForm, ClothingItemForm
from django.http import HttpResponse, HttpRequest,JsonResponse
import random

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView



# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'
    def get(self,request):
        return render(request,'index.html',{
            'hey':2
        })


def generate_outfit(user):
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
    return [outfit,len(clothes.values())]

def DashboardView(request):
    badoutfit = request.POST.get('Dislike')
    user = request.user
    outfit = generate_outfit(user)
    badoutfits = {}
    is_bad = True
    insufficient = outfit[1] < 2

    #Checks badoutfits
    for count,outfits in enumerate(BadOutfit.objects.filter()):
        badoutfits[count] = []
        for item in outfits.items.all():
            badoutfits[count].append(item)

    #Adds to bad outfit model
    if badoutfit == 'Dislike':
        badoutfits = BadOutfit()
        for clothing_item in outfit:
            badoutfits.save()
            badoutfits.items.add(clothing_item)
    
    count = len(badoutfits.values())
    for wear in badoutfits.values():
        while len(set(wear+outfit[0])) == len(outfit[0]):
            #print('badone')
            outfit = generate_outfit(user)

    return render(request,'dashboard.html',{'myclothes':outfit[0],'insufficient':insufficient})

class DashboardAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'result.html'
    #parser_classes = []
    def get(self,request):

        """
        Return a dictionary of an outfit, and if enough clothes
        """
        user = request.user
        
        clothes = {}
        outfit = []
        clothing_items = []
        for item in ClothingItem.objects.filter():
            clothing_items.append(item)
        for item in clothing_items:
            if item.category not in clothes:
                if item.user == user:
                    #print(model_to_dict(item))
                    clothes[item.category] = [item]
            else:
                if item.user == user:
                    clothes[item.category].append(item)
        #print(clothes)
        for cat in clothes:
            item = random.choice(clothes[cat])
            outfit.append(item)
        #pot_outfit = serializers.serialize("json", outfit)
        #print(outfit,pot_outfit)
        #print(type(outfit[0]))
        insufficient = len(clothes.values()) < 2
        #print(model_to_dict(outfit[0]))
        #Response class not working because outfit elements are not JSON serializable
        #return HttpResponse({'myclothes':outfit,'insufficient':insufficient})

        #Is it possible to render a template, and to have data in json?
        
        print('requested',outfit) 
        return Response({'myclothes':outfit,'insufficient':insufficient})

class NewItemView(CreateView):

    model = ClothingItem
    template_name = 'newitem.html'
    #fields = ['category','name','image']
    fields = '__all__'

#Changed from class view
def NewNotItemView(request):
    if request.method == 'POST':
        c_form = ClothingItemForm(request.POST,initial = {'user':request.user})
        if c_form.is_valid():
            c_form.save()
            return redirect('dashboard')
    else:
        c_form = ClothingItemForm(initial = {'user':request.user,'image': 'default.jpg'})
        print(c_form)
    return render(request,'newitem.html',{'form':c_form})

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
