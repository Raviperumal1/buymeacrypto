from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Creator
from .forms import CreatorForm

# Create your views here.
def signup(request):
    if request.method == 'POST':  # Checking if the request method is POST
        form = UserCreationForm(request.POST)  # Creating a form instance with POST data
        if form.is_valid():  # Checking if the form data is valid
            form.save()  # Saving the form data (creating a new user)
            return redirect('Creator:login')  # Redirecting to the login page after successful signup
    else:
        form = UserCreationForm()  # Creating a blank form for GET requests
    
    return render(request, 'Creator/signup.html', {'form': form})
@login_required
def mypage(request):
    creator = request.user.creator
    return render(request,'Creator/mypage.html',{'creator':creator})

def creators(request):
    creators = Creator.objects.all()
    return render(request, 'Creator/creators.html', {'creators': creators})

def creator(request,pk):
    creator = Creator.objects.get(pk=pk)
    return render(request, 'Creator/creator.html', {'creator': creator})

def edit(request):
    try:
        creator = request.user.creator
        if request.method == 'POST':
            form=CreatorForm(request.POST,request.FILES,instance=creator)
            if form.is_valid():
                form.save()
                return redirect('core:index')
        else:
            form = CreatorForm(instance=creator)
    except Exception:
        if request.method == 'POST':
            form=CreatorForm(request.POST,request.FILES)
            if form.is_valid():
                creator = form.save(commit=False)
                creator.user = request.user
                creator.save()
                return redirect('Crypto_App:index')
        else:    
            form = CreatorForm()
    return render(request,'creator/edit.html',{'form':form})