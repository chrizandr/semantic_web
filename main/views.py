from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Owl
from django.shortcuts import render
from django.views.generic import View
from ontospy import *
from .forms import OwlForm
import json
import pdb


def index(request):
    context=dict()
    return render(request,'main/index.html',context)

class FormProcess(View):
    form_class = OwlForm
    inputGraph = None
    filePath = "temp.owl"
    def post(self,request, *args, **kwargs):
        if request.FILES:
            try:
                self.handle_uploaded_file(request.FILES["OWLfile"])
            except KeyError:
                return self.construct_form(request,True,False)

            form = self.form_class(request.POST or None, request.FILES or None)
            if form.is_valid():
                try:
                    self.inputGraph= Graph(self.filePath)
                except:
                    return self.construct_form(request,False,True)

                tree=generateTree(self.inputGraph)
                context = dict()
                context['tree_object'] = tree
                return render(request,"main/classes.html" , context )
        else:
             s = request.POST['class_names']
             print s
             filePath = "temp.owl"
             g = self.inputGraph
             class_names = s.split(',')
             class_list = list()
             name_list = list()
             for ontoclass in g.classes:
             	if str(ontoclass.uri).split('#')[1] in class_names:
                         name = str(ontoclass.qname).split(':')[1]
                         props = [str(prop.qname).split(':')[1] for prop in ontoclass.domain_of]
                         name_list.append((name,props))
             context = dict()
             context['class_list'] = name_list
             if request.method == "POST":
                 output = str()
                 classes = dict()
                 properties = dict()
                 for entry in request.POST:
                     value = str(request.POST[entry])
                     if entry[0]=='_':
                         properties[entry[1:]] = value
                     else:
                         classes[entry] = value
             return render(request,'main/form.html',context)

    def get(self,request, *args , **kwargs):
        if request.FILES:
            print "Sending file"
        else:
            print "Doing shit"
        self.template_name = 'main/upload.html'
        return self.construct_form(request,False,False)

    def construct_form(self,request,form_flag,file_flag):
        form = self.form_class()
        context = dict()
        context["form"] = form
        context['form_flag'] = form_flag
        context['file_flag'] = file_flag
        return render(request, "main/upload.html" , context)

    def handle_uploaded_file(self,f):
        with open('temp.owl', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

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

def getClasses(request):
    if request.method == "POST":
        s = request.POST['class_names']
        print s
        filePath = "temp.owl"
        g = Graph(filePath)
        class_names = s.split(',')
        class_list = list()
        name_list = list()
        for ontoclass in g.classes:
        	if str(ontoclass.uri).split('#')[1] in class_names:
                    name = str(ontoclass.qname).split(':')[1]
                    props = [str(prop.qname).split(':')[1] for prop in ontoclass.domain_of]
                    name_list.append((name,props))
        context = dict()
        context['class_list'] = name_list
        if request.method == "POST":
            output = str()
            classes = dict()
            properties = dict()
            for entry in request.POST:
                value = str(request.POST[entry])
                if entry[0]=='_':
                    properties[entry[1:]] = value
                else:
                    classes[entry] = value
        return render(request,'main/form.html',context)
