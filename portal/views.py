from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.views import generic
from .forms import NotesForm,HomeworkForm
from .models import Notes,Homework
from youtubesearchpython import VideosSearch
import requests 
import wikipediaapi

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == 'POST':

        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save();
        messages.success(request,f"Notes added from {request.user.username} successfully")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user) # request.user means login user
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html',context)

def delete_note(request, pk=None):
    note = get_object_or_404(Notes, id=pk)
    note.delete()
    return redirect("notes")

# class notes_detail(generic.DetailView):
    # model = Notes

def NotesDetailView(request,pk=None):
    return render(request, 'dashboard/notes_detail.html')


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            hw = Homework(user=request.user, subject = request.POST['subject'], title = request.POST['title'], description = request.POST['description'],due = request.POST['due'],is_finished=finished)
            hw.save();
    else:
        form = HomeworkForm()
    hw = Homework.objects.filter(user=request.user)
    if len(hw) == 0:
        homework_done = True
    else:
        homework_done = False
    
    context2 = {'hw':hw, 'form':form,'homework_done':homework_done}
    return render(request, 'dashboard/homework.html',context2)


def update_hw(request,pk = None):
    hw = Homework.objects.get(id = pk)
    if hw.is_finished == True:
        hw.is_finished = False
    elif hw.is_finished == False:
        hw.is_finished = True
    hw.save();
    return redirect("homework")
    

def delete_hw(request, pk=None):
    hw = get_object_or_404(Homework, id=pk)
    hw.delete()
    return redirect("homework")


def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit = 10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
            }
        return render(request, 'dashboard/youtube.html',context)
    else:
        form = DashboardForm()
    form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/youtube.html',context)



def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todolist = Todo(user = request.user,title = request.POST['title'],is_finished=finished)
            todolist.save();
    else:
        form = TodoForm()
    to_do = Todo.objects.filter(user = request.user)
    context = {'form':form,'to_do':to_do}
    return render(request, 'dashboard/todo.html',context)


def delete_todo(request,pk= None):
    to_do = get_object_or_404(Todo, id = pk)
    to_do.delete()
    return redirect('todo')


def update_todo(request,pk = None):
    to_do = Todo.objects.get(id = pk)
    if to_do.is_finished == True:
        to_do.is_finished = False
    elif to_do.is_finished == False:
        to_do.is_finished = True
    to_do.save();
    return redirect("todo")


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form':form,
                'results':result_list,
            }
        return render(request, 'dashboard/books.html',context)
    else:
        form = DashboardForm()
    form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html',context)



def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except KeyError:
            context = {
                'form': form,
                'input': '',
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form,
        }
    return render(request, 'dashboard/dictionary.html', context)


def wikipedia(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        input = request.POST.get('text')
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(input)
        
        if page.exists():
            title = page.title
            summary = page.summary
            full_content = page.text
            link = "https://en.wikipedia.org/wiki/"+input
        else:
            title = 'Page not found'
            summary = ''
            link = ''
            full_content = ''

        context = {
            'form':form,
            'title': title,
            'summary': summary,
            'link':link,
            'full_content': full_content
        }

        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form':form
        }
    return render(request, 'dashboard/wiki.html',context)


