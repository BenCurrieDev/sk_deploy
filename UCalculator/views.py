from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Material, Composite, Component
from django.contrib.auth.models import User
from .forms import NewComponentForm, ClearForm, SaveForm, LoadForm, InsulatorForm, DeleteForm

from django.contrib.auth.decorators import login_required

@login_required
def database(request):
    materials = Material.objects.all()
    composites = Composite.objects.filter(user=request.user).all()
    delete = DeleteForm()
    context = { 
        'materials': materials,
        'composites': composites,
        'delete': delete
         }
    
    if request.method == "POST":
          if 'delete_composite' in request.POST: 
            form = DeleteForm(request.POST)
            if form.is_valid():
                to_del = request.POST['to_delete']
                composites.get(pk=to_del).delete()
                redirect('database')
                

    return render(request, 'database.html', context)

@login_required
def home(request):

    def deactivate():
        for component in components:
            if component.composite:
                component.active = False
                component.save()
            else:
                component.delete()
        if composites:
            active_composite.active = False
            active_composite.save()

    materials = Material.objects.all()
    composites = Composite.objects.filter(user=request.user).filter(active=True).all()
    if composites:
        active_composite = composites[0]
    else:
        active_composite = ''
    components = Component.objects.filter(user=request.user).filter(active=True).all()
    user = request.user
    clear_form = ClearForm()
    uVal = 'N/A'
    if components:
        rList = [component.calcR() for component in components]
        rSum = sum(rList)
        uVal = round(1 / (0.13 + rSum + 0.04), 2)
    insulation = ''

    if request.method == 'POST':
        
        if 'add_material' in request.POST: 
            form = NewComponentForm(request.POST)
            if form.is_valid():
                component = form.save(commit=False)
                component.user = user
                component.save()
                return redirect('home')
        
        if 'clear_material_view' in request.POST:
            deactivate()
            return redirect('home')
        
        if 'save_composite' in request.POST:
            if components:
                form = SaveForm(request.POST)
                if form.is_valid():
                    if composites:
                        active_composite.active = False
                        active_composite.save()
                    composite = form.save(commit=False)
                    composite.user = user
                    composite.save()
                    for component in components:
                        component.composite = composite
                        component.save()
                    return redirect('home')
        
        if 'calculate_insulation' in request.POST:
            form = InsulatorForm(request.POST)
            if form.is_valid():
                target_u = request.POST['target_u']
                insulation = round(0.022 * (1/float(target_u) - rSum)* 1000)


    if request.method == 'GET':
        if 'load_composite' in request.GET:
            form = LoadForm(request.GET)
            if form.is_valid():
                composite_id = request.GET['composite']
                if composite_id.isdigit():
                    deactivate()
                    to_load = Composite.objects.get(pk=composite_id)
                    to_load.active = True
                    to_load.save()
                    for component in to_load.component_set.all():
                        component.active = True
                        component.save()
                    return redirect('home')
            

    component_form = NewComponentForm()
    save_form = SaveForm()
    load_form = LoadForm()
    insulator_form = InsulatorForm()

    context = {
        'materials': materials,
        'composites': composites,
        'active_composite': active_composite,
        'components': components,
        'component_form': component_form,
        'clear_form': clear_form,
        'save_form': save_form,
        'load_form': load_form,
        'insulator_form': insulator_form,
        'uVal': uVal,
        'insulation': insulation
    }
        
    return render(request, 'home.html', context)
