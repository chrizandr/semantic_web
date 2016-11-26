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


##################### Source ####################
RDF_DECLARATION="<?xml version=\"1.0\"?><rdf:RDF\nxmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\nxmlns:si=\"http://www.w3schools.com/rdf/\">"
RDF_ENDING="</rdf:RDF>"
# ----------------------------------------------------------------------------------------
# index : function generates the basic index page of the application
def index(request):
    context = dict()
    return render(request, 'main/index.html', context)

# ----------------------------------------------------------------------------------------
# mylogin_required : Function used to check wether a given user is logged in or not.
# In case no user is logged in, redirects to the login page
def mylogin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.id:
            return HttpResponseRedirect("/login")
        return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# ----------------------------------------------------------------------------------------
# home: function generates the homepage of a logged in user
@mylogin_required
def home(request):
    context = dict()
    return render(request, 'main/home.html', context)

# ----------------------------------------------------------------------------------------
# register: function to register a new user, redirects to home
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

@mylogin_required
def get_graph(request):
    template_name="main/display_files.html"
    graph_models=Owl.objects.filter(userid=request.user.id)
    if request.method == 'POST':
        print "enter"
        name = request.POST.get('fileid',None)
        Owl.objects.filter(id=name).delete()
    paginator = Paginator(graph_models, 10)
    page = request.GET.get('page', 1)
    try:
        graphs = paginator.page(page)
    except PageNotAnInteger:
        graphs = paginator.page(1)
    except EmptyPage:
        graphs = paginator.page(paginator.num_pages)
    return render(request,template_name,{'graphs':graphs,'count': graph_models.count()})

@mylogin_required
def submitted_classes():
    return HttpResponse("sbdbhjds")

def get_property_set(ontoproperty):
    propset=list()
    propname=str(ontoproperty.locale)
    if str(ontoproperty.rdftype).split('#')[1] == 'DatatypeProperty':
        #r_list = list()
        #for property_range in ontoproperty.ranges:
        #    r_list.append(str(property_range).split('#')[1])
        datatype=""
        if len(ontoproperty.ranges)>0:
            datatype =  str(ontoproperty.ranges[0]).split('#')[1]
        propset.append(1)
        propset.append((propname,datatype))
    elif str(ontoproperty.rdftype).split('#')[1] == 'ObjectProperty':
        propset.append(2)
        propset.append((propname))
    return propset

    '''else:
         owl_content = generate_file(request.POST)
         response = HttpResponse()
         response['Content-Disposition'] = 'attachment; filename="%s.owl"' %(str(request.user.id)+"u_"+time.strftime('%H%M%S'))
         response.write(st)
         return response'''

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
        raise Http404("Cannot acces this page like this")


@mylogin_required
def create_class(request,**kwargs):
    fileid=kwargs['fileid']
    owlfile=Owl.objects.filter(id=fileid,userid=request.user.id)[0]
    g=pickle.load(open(str(owlfile.OWLfile.name),"rb"))
    tree = generateTree(g)
    context = dict()
    context['tree_object'] = tree
    context['fileid']=fileid
    if request.method=='POST':
        s = request.POST['class_names']
        class_names = s.split(',')
        name_list = list()
        obj_prop_list= dict()
        data_prop_list= dict()
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
        form = Data_type_form(request.POST or None, class_names=name_list, oprop_object=obj_prop_list, dprop_object=data_prop_list)
        context['form'] = form
        return render(request, 'main/form.html', context)
    return render(request,"main/classes.html", context)

# ----------------------------------------------------------------------------------------
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
                self.inputGraph = Graph(name)
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
