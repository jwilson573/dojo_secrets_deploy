from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Count
from .models import User, Secret

def errorMessage(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    user_id = request.session['user_id']
    return User.objects.get(id=user_id)

def index(request):
    
    return render(request, "dojo_secrets/index.html")

def secret(request):
    print "Inside the secret method"
    if 'user_id' in request.session:
        
        user_id = request.session['user_id']
        current_user = User.objects.get(id=user_id)
        secrets = Secret.objects.all()
        liked_secrets = []

        # for secret in user.likes.all():
        #     liked_secrets.append(secret.id)

        content = {
            'user': current_user,
            'secrets': secrets,
            'liked_secrets': liked_secrets
        }

        return render(request, "dojo_secrets/secrets.html", content)

    return redirect(reverse('home'))

def create(request):
    
    if request.method == 'POST':
        
        form_valid = User.objects.validate(request.POST)

        if form_valid == []:

            user = User.objects.register(request.POST)

            request.session['user_id'] = user.id
            
            return redirect('/secret')
        
        errorMessage(request, form_valid)
        
    return redirect(reverse('home'))

def logout(request):
    request.session.pop('user_id')
    return redirect(reverse('home'))

def login(request):
    if request.method == 'POST':
        
        data_check = User.objects.validate_login(request.POST)
        print data_check
        if type(data_check) == type(User()):

            request.session['user_id'] = data_check.id

            return redirect('/secret')

        errorMessage(request, data_check)
    return redirect(reverse('home'))

def create_secret(request):
    
    if request.method == 'POST':
        errors = Secret.objects.secret_validation(request.POST)

        if not errors:
            user = currentUser(request)
            secret = Secret.objects.create_secret(user, request.POST)
        
    return redirect('/secret')

def popular(request):
    print "Inside the popular method"

    popular = Secret.objects.annotate(num_likes=Count('liked_by')).order_by('-num_likes')    

    content = {
        'secrets': popular
    }

    return render(request, 'dojo_secrets/popular.html', content)

def create_like(request, id):
    print "Inside the create_like method"

    if request.method == 'POST':
        user = currentUser(request)
        secret = Secret.objects.get(id=id)
        
        user.likes.add(secret)

    return redirect(reverse('secret'))





