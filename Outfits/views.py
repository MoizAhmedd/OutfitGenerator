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

"""
#Possible get similar products
outfits = {}
styleOne = request.POST.get('StyleOne')
styleTwo = request.POST.get('StyleTwo')
styleThree = request.POST.get('StyleThree')
if styleOne:
    for count, outfit in styleOne.objects.filter():
        outfits[count] = []
        for item in outfit.items.all(): #Get all clothing items in this outfit
            outfits[count].append()
            #This should be a clothing item
                #Get the product name
                #Find the id
                #Go through the objects in users outfits
                #If user object id matches product id
                #Add to outfits[count]
return [outfits[random.choice(len(outfits))],len(clothes.values())]
"""
def generate_gcp_outfit(user,style):
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
        return [outfits[key],len(outfits)]
    except IndexError:
        return [] 

def insufficient_check(user):
    num_items = 0
    for item in ClothingItem.objects.filter():
        if item.user == user:
            num_items += 1
    return num_items < 2


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
    StyleOne = request.POST.get('Alex Costa Outfits')
    StyleTwo = request.POST.get('Alpha M Outfits')
    StyleThree = request.POST.get('TMF Outfits')
    #print(StyleTwo)
    user = request.user
    #generate_gcp_outfit(user)
    #if StyleOne == 'StyleOne':
    outfit = generate_gcp_outfit(user,1)
    if StyleOne == "StyleOne":
        outfit = generate_gcp_outfit(user,1)
    if StyleTwo == "StyleTwo":
        print('Alpha')
        outfit = generate_gcp_outfit(user,2)
    if StyleThree == "StyleThree":
        print('TMF')
        outfit = generate_gcp_outfit(user,3)
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
        if len(set(wear+outfit[0])) == len(outfit[0]) and len(badoutfitslist) != outfit:
            #all items same, outfit is a bad one
            #If length of badoutfits = length of total outfits, then insufficient
            #if len(badoutfitslist) == outfit[1]:
                #insufficient = True
            #else:
            if StyleOne == "StyleOne":
                outfit = generate_gcp_outfit(user,1)
            if StyleTwo == "StyleTwo":
                outfit = generate_gcp_outfit(user,2)

    if len(badoutfitslist) == outfit[1]:
        return render(request,'dashboard.html',{'myclothes':outfit[0],'insufficient':True})
    else:
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
