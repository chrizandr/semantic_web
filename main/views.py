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

# Script is used as a handler for a given url invocation

################### Imports ##################
import cPickle as pickle
import pdb,time
import tempfile
from os import remove

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.generic import View
from ontospy import *
from django.core.files import File
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from models import Owl
from treebuilder import *
from .forms import OwlForm, UserForm, Data_type_form
from generate import *
##################### Global ####################

RDF_DECLARATION="<?xml version=\"1.0\"?><rdf:RDF\nxmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\nxmlns:si=\"http://www.w3schools.com/rdf/\">"
RDF_ENDING="</rdf:RDF>"

##################### Source ####################

# ----------------------------------------------------------------------------------------
# mylogin_required : It is an authentication function used to check whether a user is logged in or not
# Uses the request object to check the user attribute. If the attribute is null (no user logged in) then redirects to log in page
# Any function can be made into an authenticated function by using the "@mylogin_required" override.
def mylogin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.id:
            return HttpResponseRedirect("/login")
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# ----------------------------------------------------------------------------------------
# index : Function generates the basic index page of the application.
# The index page displays ad introduction about the website/project
# Users are given the option to LogIn or SignUp. The page does not perform any functions other than linking the login and registration pages
# There is no need to be logged in to access the index page.
def index(request):
    context = dict()
    return render(request, 'main/index.html', context)

# ----------------------------------------------------------------------------------------
# register: Generates the page for a new user to register.
# Required fields for registration are: <username> <email> <password> [<confirm password>]
# Password field has certain restrictions that are displayed on the registration page
# If the user registration is correct it redirects the user to a confirmation page.
# Does not log in the user after registration process is complete. User must log in after registration.
def register(request):
    template_name = "main/register.html"
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "main/register_after.html", {})
    else:
        form = UserForm()
    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render(request, template_name, token)

# ----------------------------------------------------------------------------------------
# OwlProcessor: Class to handle various processes related to OWL files uploading and storing
# GET request is handled by the get function, returns a form to allow a user to upload a file.
# Once form is submitted a PSOT request is issued and the post function is invoked to handle it.
# The POST function creates a temporary file where the contents of the uploaded file are copied.
# The file is parsed and a Graph object is created for the Ontology.
# The object is stored in the RAM, a screenshot of the state where the object is stored is taken.
# The screenshot of the objec is stored in another file. This file is linked to the database entry for the upload.
# Parsing the file takes a large amount of time, therefore this method was used to minimise the latency
# Stored images can be retrieved and loaded back into python objects almost instantaneously.
class OwlProcessor(View):
    form_class = OwlForm
    inputGraph = None
    filePath = "temp.owl"

    def post(self, request, *args, **kwargs):
        # ----------------------------------------------------
        if request.POST:
            if not (request.FILES):
                return self.construct_form(request, True, False)
            f = request.FILES["OWLfile"]
            fname = str(f.name)
            temp = tempfile.NamedTemporaryFile(delete=False)
            name = temp.name
            for chunk in f.chunks():
                temp.write(chunk)
            temp.close()
            try:
                self.inputGraph = Ontospy(name)
            except:
                remove(name)
                return self.construct_form(request, False, True)
            remove(name)
            temp = tempfile.NamedTemporaryFile(delete=False, dir="file_uploads/")
            name = temp.name
            pickle.dump(self.inputGraph, temp, -1)
            temp.close()
            f = open(name, 'rb')
            owl = Owl()
            owl.OWLfile = File(f)
            owl.userid = request.user.id
            owl.fname = fname
            owl.save()
            os.remove(name)
            return HttpResponseRedirect( reverse('classes',kwargs={'fileid':owl.id}))

    # -----------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        self.template_name = 'main/upload.html'
        return self.construct_form(request, False, False)

    # -----------------------------------------------------------------
    def construct_form(self, request, form_flag, file_flag):
        form = self.form_class()
        context = dict()
        context["form"] = form
        context['form_flag'] = form_flag
        context['file_flag'] = file_flag
        return render(request, "main/upload.html", context)

    # -----------------------------------------------------------------
    def handle_uploaded_file(self, f):
        with open('temp.owl', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

# ----------------------------------------------------------------------------------------
# get_graph: Function handles the main homepage of a logged in user.
# The current files that the user has uploaded to the server are displayed in a list.
# The files can be reused to generate new instances using classes from the old OWL file.
# The list of files is pagenated to prevent cluttering and overcrowding.
# Entries are limited to 10 per page.
# Buttons are provided to reuse and delete a previous Graph.
@mylogin_required
def get_graph(request):
    template_name="main/display_files.html"
    graph_models=Owl.objects.filter(userid=request.user.id)
    if request.method == 'POST':
        print "enter"
        name = request.POST.get('fileid',None)
        owl = Owl.objects.filter(id=name)[0]
        remove(str(owl.OWLfile))
        owl.delete()
    paginator = Paginator(graph_models, 10)
    page = request.GET.get('page', 1)
    try:
        graphs = paginator.page(page)
    except PageNotAnInteger:
        graphs = paginator.page(1)
    except EmptyPage:
        graphs = paginator.page(paginator.num_pages)
    return render(request,template_name,{'graphs':graphs,'count': graph_models.count()})

# ----------------------------------------------------------------------------------------
# get_property_set: Function used for getting the object properties and the data properties for a given class.
# Both the properties are in lists that are appended to a parent list and returned.
def get_property_set(ontoproperty):
    propset=list()
    propname=str(ontoproperty.locale)
    if str(ontoproperty.rdftype).split('#')[1] == 'DatatypeProperty':
        datatype=""
        if len(ontoproperty.ranges)>0:
            datatype =  str(ontoproperty.ranges[0]).split('#')[1]
        propset.append(1)
        propset.append((propname,datatype))
    elif str(ontoproperty.rdftype).split('#')[1] == 'ObjectProperty':
        propset.append(2)
        propset.append((propname))
    return propset

# ----------------------------------------------------------------------------------------
# FormProcess: Class based view used to generate a tree for the classes present in an OWL file.
# The generated tree object is hierchically arranged as parents and children classes.
# Selecting a parent would select it consecutive children as well.
# The tree was generated using the jqxTree widget for javascript.
# The tree generation is called via a GET request which is handled by the get functions
# Class trees are selected and communicated using a POST request. These are handled by the post function.
# The screenshoted RAM images of the Graph object are loaded directly so that they may be used without re-parsing the OWL file.
class FormProcess(View):
# ---------------------------attributes-------------------------------------------
    template_name = "main/form.html"
# ---------------------------functions--------------------------------------------
    def post(self,request,*args,**kwargs):
        if request.POST.get('class_names',False):
            fileid=kwargs['fileid']
            owlfile=Owl.objects.filter(id=fileid,userid=request.user.id)[0]
            g=pickle.load(open(str(owlfile.OWLfile.name),"rb"))
            s = request.POST['class_names']
            class_names = s.split(',')
            name_list = list()
            obj_prop_list= dict()
            data_prop_list= dict()
            context = dict()
            for ontoclass in g.classes:
                if str(ontoclass.uri).split('#')[1] in class_names:
                    name = str(ontoclass.qname).split(':')[1]
                    tdlist=set()
                    tolist=set()
                    for prop in ontoclass.domain_of:
                        pset=get_property_set(prop)
                        dproperty=pset[1]
                        if pset[0]==1:
                            tdlist.add(dproperty)
                        elif pset[0]==2:
                            tolist.add(dproperty)
                    for prop in ontoclass.range_of:
                        pset=get_property_set(prop)
                        dproperty=pset[1]
                        if pset[0]==1:
                            tdlist.add(dproperty)
                        elif pset[0]==2:
                            tolist.add(dproperty)
                    name_list.append(name)
                    obj_prop_list[name]=tolist
                    data_prop_list[name]=tdlist
                    print data_prop_list
            form = Data_type_form(request.POST or None, class_names=name_list, oprop_object=obj_prop_list, dprop_object=data_prop_list)
            context['form'] = form
            return render(request, self.template_name, context)
        else:
            return Http404("Invalid POST request")
    # -----------------------------------------------------------------
    def get(self, request, *args, **kwargs):
        fileid=kwargs['fileid']
        owlfile=Owl.objects.filter(id=fileid,userid=request.user.id)[0]
        g=pickle.load(open(str(owlfile.OWLfile.name),"rb"))
        tree = generateTree(g)
        context = dict()
        context['tree_object'] = tree
        context['fileid']=fileid
        return render(request,"main/classes.html", context)
# ----------------------------------------------------------------------------------------
# generate_file: Function used for viewing and downloading the generated OWL instance file.
# The file is displayed in a textbox for the user to be able to edit the contents.
# The newly updated content is downloaded when the download button is clicked. The name of the file is in the format "<user.id>u<timestamp>"
# Function cannot be accessed using a get method. An HTTP 404 error is raised in case of a get request
def generate_file(request):
    if request.method == "POST":
        if request.POST.get('code', False):
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename="%s.owl"' %(str(request.user.id)+"u_"+time.strftime('%H%M%S'))
            response.write(str(request.POST["code"]))
            return response
        else:
            st=get_file(request.POST)
            context = dict()
            context["code"] = str(st)
            return render(request,"main/instances.html",context)
    else:
        raise Http404("Cannot access this page like this")
