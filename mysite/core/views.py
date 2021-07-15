from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book
import os
import PyPDF2
from gtts import gTTS
from io import BytesIO

# Create your views here.
def home(request):
	count=User.objects.count()
	return render(request,'home.html',{
		'count': count
				})

def signup(request):
	if request.method == 'POST':
	   form = UserCreationForm(request.POST)
	   if form.is_valid():
	   	 form.save()
	   	 return redirect('home')
	else:
		form = UserCreationForm()
	return render(request,'registration/signup.html',{
		'form':form

		})


@login_required
def secret_page(request):
	return render(request,'secret_page.html')


class SecretPage(LoginRequiredMixin,TemplateView):
    template_name='secret_page.html'

def upload(request):
    language = 'en'
    music = ''

    context={
        'music':music,
    }
    return render(request,'upload.html',context)
    
    
@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })

@login_required
def upload_book(request):
    music = ''
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            pdfFileObj = request.FILES['document']
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            mytext = ""
            language = request.POST.get('lang')
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                mytext += pageObj.extractText()
            pdfFileObj.close()
            myobj=gTTS(text=mytext, lang=language)
            #myobj.save("static/speech.mp3")
            myobj.save("static/"+pdfFileObj.name+".mp3")
            music = 'ok'
            af = pdfFileObj.name+".mp3"
            context={
            'music':music,
            'audiofile':af,
            }
            return render(request,'upload.html',context)
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })

@login_required
def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')

    