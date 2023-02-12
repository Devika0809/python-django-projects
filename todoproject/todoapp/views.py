from django.contrib import messages
from django.forms import SelectDateWidget
from django.shortcuts import render,redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import TodoForm
from . models import Task

class Tasklistview(ListView):
    model = Task
    template_name = 'index.html'
    context_object_name = 'task1'

class TaskDetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task1'

class TaskUpdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task1'
    fields = ("name","priority","date")
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})
    def get_form(self):
        form = super(TaskUpdateview, self).get_form()
        form.fields['date'].widget = SelectDateWidget()
        return form

class TaskDeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

def home(request):
    task1 = Task.objects.all().order_by('priority','date').values()
    if request.method=='POST':
        name = request.POST.get('task','')
        priority = request.POST.get('priority','')
        date= request.POST.get('date','')
        task = Task(name=name,priority=priority, date=date)
        task.save()
    return render(request,'home.html',{'task1':task1})
# def details(request):
#     task= Task.objects.all()
#     return render(request,'details.html',{'task':task})

def delete(request, taskid):
    task = Task.objects.get(id=taskid)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task = Task.objects.get(id=id)
    f = TodoForm(request.POST or None, instance = task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,'edit.html',{'f':f,'task':task})
