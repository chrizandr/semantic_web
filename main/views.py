from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from ontospy import *
from .forms import OwlForm, UserForm, Data_type_form
import json
import pdb

def index(request):
    context=dict()
    return render(request,'main/index.html',context)

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

class RegisterView(View):
    template_name = "main/register.html"
    form_class = UserForm

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self,request):
        form = self.form_class(None)
        if form.is_valid():
            user = form.save(commit = False)
            username = user.cleaned_data["username"]
            password = user.cleaned_data["password"]
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("main:home")
        else:
            print "Invalid"
        return render(request, self.template_name, {"form": form})

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
            print st
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
        i=0
        st="<p>"
        for (label,value) in form.data_values():
            st+="&lt;"+str(data_prop[i][2][0])+"&gt;<br>"
            st+="&lt;"+label+" rdf:datatype= \""+data_prop[i][1][0]+"\" &gt; "+str(value)+" &lt;/"+label+"&gt;<br>"
            st+="&lt;/"+data_prop[i][2][0]+"&gt;<br><br>"
            i+=1
        st+="</p>"
        print st
        #output_file.close()
        return HttpResponse(st)

    return render(request,"main/register.html", {'form': form})

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
