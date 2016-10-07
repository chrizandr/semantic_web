
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
