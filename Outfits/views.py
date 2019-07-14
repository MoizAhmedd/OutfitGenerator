from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.core import serializers
from .models import ClothingItem, BadOutfit, StyleOne, StyleTwo, StyleThree
from django.contrib.auth import authenticate,login
from .forms import SignUpForm, ClothingItemForm
from django.http import HttpResponse, HttpRequest,JsonResponse
import random
from . import generate
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import os



# Create your views here.
class HomePageView(TemplateView):
    template_name = 'index.html'
    def get(self,request):
        return render(request,'index.html',{
            'hey':2
        })

def generate_gcp_outfit(user,style):
    print(style)
    if style == 0:
        return [[]]
    outfits = {}
    objects = []
    if style == 1:
        objects = StyleOne.objects.filter()
        #print(objects)
    if style == 2:
        objects = StyleTwo.objects.filter()
    if style == 3:
        objects = StyleThree.objects.filter()
    for count, outfit in enumerate(objects):
        outfits[count] = []
        for item in outfit.items.all():
            project_id = "outfitgenerator"
            location = "us-east1"
            product_set_id = user.username + str("_PS")
            product_category = "apparel"
            file_path = item.image.path
            #print(product_set_id)
            filter = "category=" + str(item.category)
            #create clothing item from line below/find clothing item
            #print(item)
            product_id = generate.get_similar_products_file(project_id,location,product_set_id,product_category,file_path,filter)
            for my_item in ClothingItem.objects.filter():
                if my_item.user == user:
                    if my_item.id == int(product_id):
                        outfits[count].append(my_item)
                        #print(my_item.name,my_item.id,product_id)
                    #print(product_id,my_item.id)
                #print(product_id,my_item.user,my_item.id)
                #outfits[count].append(my_item)
    #print(outfits[key])
    try:
        key = random.choice(list(outfits.keys()))
        print(outfits[key])
        return [outfits[key],len(outfits),outfits]
    except IndexError:
        return [] 

def insufficient_check(user):
    num_items = 0
    for item in ClothingItem.objects.filter():
        if item.user == user:
            num_items += 1
    return num_items < 2


def DashboardView(request,style):
    badoutfit = request.POST.get('Dislike')
    StyleOne = request.POST.get('Alex Costa Outfits')
    StyleTwo = request.POST.get('Alpha M Outfits')
    StyleThree = request.POST.get('TMF Outfits')
    styleChosen = None
    #print(StyleTwo)
    user = request.user
    outfit = generate_gcp_outfit(user,style)
    #generate_gcp_outfit(user)
    #if StyleOne == 'StyleOne':
    #outfit = generate_gcp_outfit(user,0)
    #if StyleOne == "StyleOne":
     #   outfit = generate_gcp_outfit(user,1)
    #if StyleTwo == "StyleTwo":
    #    print('Alpha')
    #    outfit = generate_gcp_outfit(user,2)
    #if StyleThree == "StyleThree":
    #    print('TMF')
    #    outfit = generate_gcp_outfit(user,3)
    print(StyleOne,StyleTwo,StyleThree)
    badoutfitslist = {}
    is_bad = True
    insufficient = insufficient_check(user)

    #Checks badoutfits
    for count,outfits in enumerate(BadOutfit.objects.filter()):
        #badoutfitslist[count] = []
        if outfits.user == user:
            badoutfitslist[count] = []
            for item in outfits.items.all():
                badoutfitslist[count].append(item)

    #Adds to bad outfit model
    if badoutfit == 'Dislike':
        badoutfits = BadOutfit()
        for clothing_item in outfit[0]:
            badoutfits.user = request.user
            badoutfits.save()
            badoutfits.items.add(clothing_item)
                
    #print(badoutfitslist)
    count = len(badoutfitslist.values())
    for wear in badoutfitslist.values():
        if len(set(wear+outfit[0])) == len(outfit[0]):
            #all items same, outfit is a bad one
            #If length of badoutfits = length of total outfits, then insufficient
            #if len(badoutfitslist) == outfit[1]:
                #insufficient = True
            #else:
            if StyleOne == "StyleOne":
                outfit = generate_gcp_outfit(user,style)
            if StyleTwo == "StyleTwo":
                outfit = generate_gcp_outfit(user,style)
            if StyleThree == "StyleThree":
                outfit = generate_gcp_outfit(user,style)
    
    if not (style == 1 or style == 2 or style == 3):
        styleChosen = False
    else:
        styleChosen = True

    if len(outfit[0]) <= 2:
        return render(request,'dashboard.html',{'myclothes':outfit[0],'insufficient':True,'styleChosen':styleChosen,'style':style})
    
    
    #Fix this so bad outfits aren't generated
    return render(request,'dashboard.html',{'myclothes':outfit[0],'insufficient':insufficient,'styleChosen':styleChosen,'style':style})



class NewItemView(CreateView):

    model = ClothingItem
    template_name = 'newitem.html'
    #fields = ['category','name','image']
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
            project_id = "outfitgenerator"
            location = "us-east1"
            product_set_id = username + "_PS"
            product_set_display_name = username + "_OUTFITS"
            generate.create_product_set(project_id,location,product_set_id,product_set_display_name)
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username,password=raw_password)
            login(request,user)
            return redirect('/')

    else:
        form = SignUpForm()

    return render(request,'registration/signup.html',{'form':form})
