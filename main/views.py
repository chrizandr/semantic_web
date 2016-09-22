from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Owl
from django.shortcuts import render
from ontospy import *
from .forms import OwlForm
import json
# Create your views here.


def index(request):
    context=dict()
    return render(request,'main/index.html',context)


def uploads(request):
    form = OwlForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get('OWLfile')
        instance.save()
        return HttpResponseRedirect(reverse('classes'))
    context = dict()
    context["form"] = form
    return render(request, 'main/upload.html', context)

def classes(request):
    context = dict()
    fileName = Owl.objects.order_by('-timestamp')[0]
    filePath = str(fileName.OWLfile.path)
    print filePath
    inputGraph= Graph(filePath)
    tree=generateTree(inputGraph)
    context = dict()
    context['tree_object'] = tree
    return render(request,'main/classes.html' , context )



def getAllChildren(node,class_id):
    child_list=list()
    parentid=class_id
    class_id+=1
    for child in node.children():
        class_dict= dict()
        class_dict["id"]=class_id
        class_dict["text"]=(str(child).split('#')[-1]).strip('*>')
        class_dict["parentid"]=parentid
        child_list.append(class_dict)
        sub_list=getAllChildren(child,class_id)
        class_id+=1
        for each_dict in sub_list:
            class_id+=1
            child_list.append(each_dict)
    return child_list

def generateTree(graph):
    classlist=list()
    class_id=1
    for each_class in graph.toplayer:
        class_dict= dict()
        class_dict["id"]=class_id
        class_dict["text"]=(str(each_class).split('#')[-1]).strip('*>')
        class_dict["parentid"]=-1
        child_list=getAllChildren(each_class,class_id)
        classlist.append(class_dict)
        for each_child in child_list:
            class_id+=1
            classlist.append(each_child)
        class_id+=1
    json.dumps(classlist)
    return classlist
