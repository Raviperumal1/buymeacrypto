from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cryptomus import Client

from .forms import CreatorForm
from .models import Creator, Support

# Create your views here.
MERCHANT_UUID = '621379c1-acca-4252-b066-2e86bfccff04'
PAYMENT_KEY = '1P0521ebLUozs8zAW2EOfNreI6DKi8qKeFuQaDWGzug8r3Wz7k32NCEdlzj5QjgaiagUfXisxmOqPND2HebpIfW1nB1aSrbuQg02PHvIxaj5opvEan9S52t92DV7C9bG'

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
        # Attempt to retrieve the Creator instance associated with the authenticated user
        creator = request.user.creator
    except Creator.DoesNotExist:
        # If the Creator instance doesn't exist, create a new one
        creator = Creator(user=request.user)

    if request.method == 'POST':
        # Process the form data if the request method is POST
        form = CreatorForm(request.POST, request.FILES, instance=creator)
        if form.is_valid():
            # Save the form data
            form.save()
            return redirect('Crypto_App:index')  # Redirect to the desired URL after saving
    else:
        # Initialize the form with the existing Creator instance (or a new one)
        form = CreatorForm(instance=creator)

    # Render the template with the form
    return render(request, 'Creator/edit.html', {'form': form})

def support_success(request, creator_id, support_id):
    support = Support.objects.get(pk=support_id)
    payment = Client.payment(PAYMENT_KEY, MERCHANT_UUID)

    result = payment.info({
        "uuid": f"{support.cryptomus_uuid}",
        "order_id": f"{support.id}"
    })

    if result['payment_status'] == 'paid':
        support.is_paid = True
        support.save()

    return render(request, 'Creator/success.html')

