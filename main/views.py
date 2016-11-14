from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
#from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from ontospy import *
from .forms import OwlForm, UserForm, Data_type_form
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from treebuilder import *
import json
import pdb

##Tweaked login_required function so that it redirects to index.html on checking if user active fails
def mylogin_required(function):
        def wrap(request, *args, **kwargs):
                #this check the session if userid key exist, if not it will redirect to login page
                print "user id",request.user.id
                if not (request.user.id):
                        return HttpResponseRedirect("/login")
                return function(request, *args, **kwargs)
        wrap.__doc__=function.__doc__
        wrap.__name__=function.__name__
        return wrap


def index(request):
    context=dict()
    return render(request,'main/index.html',context)

@mylogin_required
def home(request):
    context = dict()
    return render(request, 'main/home.html', context)

class OwlProcessor(View):
    form_class = OwlForm
    inputGraph = None
    filePath = "temp.owl"

    def post(self,request, *args, **kwargs):
        if request.POST["classes"]:
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
                return render(request,"main/classes.html" , context)

        elif request.POST["form"]:
             s = request.POST['class_names']
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
             return render(request,'main/form.html',context)
        elif request.POST["instances"]:
             print "Shit"

    def get(self,request, *args , **kwargs):
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

def register(request):
    template_name = "main/register.html"
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,"main/home.html",[])
    else:
        form = UserForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render(request,template_name,token)

class DataPropView(View):
    def get(self,request):
        filePath = "temp.owl"
        print filePath
        graph = Graph(filePath)
        data_prop = list()
        for each in graph.properties:
            lis = list()
            if str(each.rdftype).split('#')[1] == 'DatatypeProperty':
                lis.append(str(each.locale))
                r_list = list()
                for property_range in each.ranges:
                    r_list.append(str(property_range).split('#')[1])
                d_list = list()
                for domain in each.domains:
                    d_list.append(str(domain).split('#')[1].split('*')[0])
                lis.append(r_list)
                lis.append(d_list)
            if len(lis) > 0:
                data_prop.append(lis)
        form = Data_type_form(request.POST or None, prop_object=data_prop)
        return render(request, "main/register.html", {'form': form})

    def post(self,request):
        print "enter"
        form = Data_type_form(request.POST)
        if form.is_valid():
            output_file = open("output.owl", 'w')
            i = 0
            st = "<p>"
            for (label, value) in form.data_values():
                st += "&lt;" + str(data_prop[i][2][0]) + "&gt;<br>"
                st += "&lt;" + label + " rdf:datatype= \"" + data_prop[i][1][0] + "\" &gt; " + str(
                    value) + " &lt;/" + label + "&gt;<br>"
                st += "&lt;/" + data_prop[i][2][0] + "&gt;<br><br>"
                i += 1
            st += "</p>"
            print data_prop
            # output_file.close()
            return HttpResponse(st)
        else:
            return render(request, "main/register.html", {'form': form})


def get_data_properties(request):
    filePath = "temp.owl"
    print filePath
    graph = Graph(filePath)
    data_prop=list()
    for each in graph.properties:
        lis=list()
        if str(each.rdftype).split('#')[1]=='DatatypeProperty':
                lis.append(str(each.locale))
                r_list=list()
                for property_range in each.ranges:
                        r_list.append(str(property_range).split('#')[1])
                d_list=list()
                for domain in each.domains:
                        d_list.append(str(domain).split('#')[1].split('*')[0])
                lis.append(r_list)
                lis.append(d_list)
        if len(lis)>0:
            data_prop.append(lis)
    form = Data_type_form(request.POST or None,prop_object=data_prop)
    if form.is_valid():
        output_file=open("output.owl",'w')
        st="<p>"
        for (label,value) in form.data_values():
            for i in range(0,len(data_prop)):
                if data_prop[i][0]==label:
                    break
            st+="&lt;rdf:Description rdf:about=\"#"+str(data_prop[i][2][0])+"\"&gt;<br>"
            st+="&lt;"+label+" rdf:datatype= \""+data_prop[i][1][0]+"\" &gt; "+str(value)+" &lt;/"+label+"&gt;<br>"
            st+="&lt;/rdf:Description&gt;<br><br>"
        st+="</p>"
        print data_prop
        #output_file.close()
        return HttpResponse(st)

    return render(request,"main/register.html", {'form': form})


# def getClasses(request):
#     if request.method == "POST":
#         s = request.POST['class_names']
#         print s
#         filePath = "temp.owl"
#         g = Graph(filePath)
#         class_names = s.split(',')
#         class_list = list()
#         name_list = list()
#         for ontoclass in g.classes:
#         	if str(ontoclass.uri).split('#')[1] in class_names:
#                     name = str(ontoclass.qname).split(':')[1]
#                     props = [str(prop.qname).split(':')[1] for prop in ontoclass.domain_of]
#                     name_list.append((name,props))
#         context = dict()
#         context['class_list'] = name_list
#         if request.method == "POST":
#             output = str()
#             classes = dict()
#             properties = dict()
#             for entry in request.POST:
#                 value = str(request.POST[entry])
#                 if entry[0]=='_':
#                     properties[entry[1:]] = value
#                 else:
#                     classes[entry] = value
#         return render(request,'main/form.html',context)
