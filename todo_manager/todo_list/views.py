from msilib.schema import ListView
from pipes import Template
from typing import Any
from django.contrib.messages import success
from django.db.models import Model
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import ToDoItemCreateForm, ToDoItemUpdateForm
from .models import ToDoItem



def index_view(request: HttpRequest) -> HttpResponse:
    todo_items = ToDoItem.objects.all()[:3]
    return render(
        request, 
        template_name="todo_list/index.html",
        context={"todo_items": todo_items},
    )

class ToDoListIndexView(ListView):
    template_name = "todo_list/index.html"
    # queryset = ToDoItem.objects.order_by('-id').all()[:2]
    queryset = ToDoItem.objects.all()[:2]

    
class ToDoListView(ListView):
    # model = ToDoItem
    queryset = ToDoItem.objects.filter(archived=False)
    

class ToDoListDoneView(ListView):
    queryset = ToDoItem.objects.filter(done=True).all()

class ToDoDetailView(DetailView):
    # model = ToDoItem 

    queryset = ToDoItem.objects.filter(archived=False)

class ToDoItemCreateView(CreateView):
    model = ToDoItem
    form_class = ToDoItemCreateForm
    # fields = ("title", "description")

    def get_success_url(self):
         return reverse(
             "todo_list:detail",
             kwargs={"pk": self.object.pk}, # type: ignore
         )
    
class ToDoItemUpdateView(UpdateView):
    model = ToDoItem
    template_name_suffix = "_update_form"
    form_class = ToDoItemUpdateForm
    

class ToDoItemDeleteView(DeleteView):
    model = ToDoItem

    success_url = reverse_lazy("todo_list:list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True # type: ignore
        self.object.save() # type: ignore
        return HttpResponseRedirect(success_url)
