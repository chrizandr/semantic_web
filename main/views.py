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
    template_name = None
    inputGraph = None
    def post(self,request, *args, **kwargs):
        #try:
            self.template_name = 'main/classes.html'
            request.FILES["OWLfile"]
            form = self.form_class(request.POST or None, request.FILES or None)
            print request.FILES==None
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                filePath = instance.OWLfile.path
                self.inputGraph= Graph(filePath)
                tree=generateTree(self.inputGraph)
                context = dict()
                context['tree_object'] = tree
                return render(request,self.template_name , context )
        # except MultiValueDictKeyError:
        #     print "error"

    def get(self,request, *args , **kwargs):
        self.template_name = 'main/upload.html'
        form = self.form_class()
        context = dict()
        context["form"] = form
        return render(request, self.template_name , context)


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



def getClasses(request):
    fileName = Owl.objects.order_by('-timestamp')[0]
    filePath = str(fileName.OWLfile.path)
    print filePath
    g = Graph(filePath)
    s = 'Pizza'
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
        pdb.set_trace()


    return render(request,'main/form.html',context)
