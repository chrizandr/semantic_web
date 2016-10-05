from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Owl
from django.shortcuts import render
from ontospy import *
from .forms import OwlForm
import json


def index(request):
    context=dict()
    return render(request,'main/index.html',context)

def uploads(request):
    form = OwlForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        print "The ID is ........\n\n\n", instance.id
        return HttpResponseRedirect(reverse('classes'))
    context = dict()
    context["form"] = form
    return render(request, 'main/upload.html', context)

def instances(request):
    if request.method == "POST":
        data = request.POST.get('str')
        print data
        context['data'] = data
        context['flag'] = 1
    else:
        context['flag'] = 0
    return render(request, 'main/instances.html' , context)

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

def create_dict(node,node_id,parent_id):
    node_dict=dict()
    node_dict["id"]=node_id
    node_dict["text"]=(str(node).split('#')[-1]).strip('*>')
    node_dict["parentid"]=parent_id
    return node_dict

def getAllChildren(node,class_id):
    child_list=list()
    parentid=class_id
    class_id+=1
    for child in node.children():
        class_dict= create_dict(child,class_id,parentid)
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
        class_dict= create_dict(each_class,class_id,-1)
        child_list=getAllChildren(each_class,class_id)
        classlist.append(class_dict)
        for each_child in child_list:
            class_id+=1
            classlist.append(each_child)
        class_id+=1
    json.dumps(classlist)
    return classlist
