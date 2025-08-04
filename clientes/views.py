from django.shortcuts import render, redirect

from .models import Cliente
from .forms import ClienteForm

# Create your views here.
def lista_clientes(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    context = {'clientes': clientes, 'form': form}
    return render(request, 'lista_clientes.html', context)

