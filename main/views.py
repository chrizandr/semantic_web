##########################################################################################
## Semantic Web Form                                                                    ##
## Authors : Chris Andrew, Santhoshini Reddy                                            ##
## Email: chris.g14@iiits.in ; santhoshini.g14@iiits.in                                 ##
## Github: https://github.com/chrizandr ; https://github.com/Sanny26                    ##
###################################################################                     ##
## Description: This project was developed as part of the SEFP course at IIIT Sri City  ##
## All code is available for free usage for educational purposes                        ##
## Authors do not authorize commercial use of the source code                           ##
##########################################################################################

# Script defines acts as a handler for a given url invocation

################### Imports ##################
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import View
from ontospy import *
from .forms import OwlForm, UserForm, Data_type_form
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from treebuilder import *
import mimetypes, tempfile
from models import Owl
from os import remove
import pdb
##################### Source ####################
#----------------------------------------------------------------------------------------
# index : function generates the basic index page of the application
def index(request):
    context=dict()
    return render(request,'main/index.html',context)
#----------------------------------------------------------------------------------------
# mylogin_required : Function used to check wether a given user is logged in or not.
# In case no user is logged in, redirects to the login page
def mylogin_required(function):
        def wrap(request, *args, **kwargs):
                if not (request.user.id):
                        return HttpResponseRedirect("/login")
                return function(request, *args, **kwargs)
        wrap.__doc__=function.__doc__
        wrap.__name__=function.__name__
        return wrap
#----------------------------------------------------------------------------------------
# home: function generates the homepage of a logged in user
@mylogin_required
def home(request):
    context = dict()
    return render(request, 'main/home.html', context)

#----------------------------------------------------------------------------------------
# register: function to register a new user, redirects to home
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
#----------------------------------------------------------------------------------------
# OwlProcessor: Class to handle various processes related to OWL files
#
# OwlProcessor.post: Handles all post requests sent to the class. Flags decide the operation
#
# flag "classes" : Indicates that the post request is sending a file that needs to be parsed
# and the class tree of the file needs to be returned.
# flag "form" : Indicates that the post request is sending a list of classes that need to be
# selected for form to be generated. Expects form in return.
class OwlProcessor(View):
    form_class = OwlForm
    inputGraph = None
    filePath = "temp.owl"
    def post(self,request, *args, **kwargs):
        #----------------------------------------------------
        if request.POST["classes"]:
            if not(request.FILES):
                return self.construct_form(request,True,False)
            f = request.FILES["OWLfile"]
            fname = str(f.name)
            temp = tempfile.NamedTemporaryFile(delete=False)
            name = temp.name
            for chunk in f.chunks():
                temp.write(chunk)
            temp.close()
            try:
                self.inputGraph= Graph(name)
            except:
                remove(name)
                return self.construct_form(request,False,True)
            remove(name)
            owl = Owl()
            tree=generateTree(self.inputGraph)
            context = dict()
            context['tree_object'] = tree
            return render(request,"main/classes.html" , context)
        #----------------------------------------------------
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
    #-----------------------------------------------------------------
    def get(self,request, *args , **kwargs):
        self.template_name = 'main/upload.html'
        return self.construct_form(request,False,False)
    #-----------------------------------------------------------------
    def construct_form(self,request,form_flag,file_flag):
        form = self.form_class()
        context = dict()
        context["form"] = form
        context['form_flag'] = form_flag
        context['file_flag'] = file_flag
        return render(request, "main/upload.html" , context)
    #-----------------------------------------------------------------
    def handle_uploaded_file(self,f):
        with open('temp.owl', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
#----------------------------------------------------------------------------------------
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
        flag=0
        if len(data_prop)==0:
            flag=-1
        return render(request, "main/dataprop.html", {'form': form,'flag': flag})

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
            return render(request, "main/dataprop.html", {'form': form})

#----------------------------------------------------------------------------------------
# get_data_properties: function generates a form from the selected
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
    flag=0
    if len(data_prop)==0:
        flag=-1
    if form.is_valid():
        flag=1
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
        response = HttpResponse('text/xml; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="success.txt"'
        response.write(st)
        #response['X-Sendfile'] =
        return response
    return render(request,"main/dataprop.html", {'form': form,'flag':flag})
