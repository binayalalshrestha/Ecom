from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import RandomObject

# RandomObject list view
class RandomObjectListView(ListView):
    model = RandomObject
    template_name = 'randomObject/randomObject_list.html'
    # context_object_name = 'randomObject:randomObjects'

# RandomObject detail view
class RandomObjectDetailView(DetailView):
    model = RandomObject
    template_name = 'randomObject/randomObject_detail.html'
    context_object_name = 'randomObject:randomObject'

# RandomObject create view
class RandomObjectCreateView(CreateView):
    model = RandomObject
    fields = ['name', 'type']
    template_name = 'randomObject/randomObject_create.html'
    success_url = reverse_lazy('store:adminDashboard2')

# RandomObject update view
class RandomObjectUpdateView(UpdateView):
    model = RandomObject
    fields = ['name', 'type']
    template_name = 'randomObject/randomObject_update.html'
    success_url = reverse_lazy('store:adminDashboard2')

# RandomObject delete view
class RandomObjectDeleteView(DeleteView):
    model = RandomObject
    template_name = 'randomObject/randomObject_delete.html'
    success_url = reverse_lazy('store:adminDashboard2')
