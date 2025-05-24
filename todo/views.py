from django.shortcuts import render, redirect
from .models import Task
from django.db.models import Count,Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Login View
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to dashboard or home
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# Sign-Up View
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('/log_in/')

    return render(request, 'signup.html')


# Logout View (Optional)
def log_out(request):
    logout(request)
    return redirect('/log_in/')

@login_required(login_url="/log_in/")
def home(request):
    # for conut padding
    padding = Task.objects.aggregate(
        padd = Count('task', filter=Q(task__isnull=False) & Q(complete=False) & Q(user=request.user))
    )
    p = padding['padd']

    # for count complete
    complate = Task.objects.aggregate(
        com = Count('task', filter=Q(task__isnull=False) & Q(complete=True)  & Q(user=request.user))
    )
    c = complate['com']



    # for retrieve all task
    obj1 = Task.objects.filter(user=request.user)

    return render(request, "home.html",{'page':'home','Tasks':obj1, 'padding':p, "complete": c})

@login_required(login_url="/log_in/")
def padding(request):

     # for conut padding
    padding = Task.objects.aggregate(
        padd = Count('task', filter=Q(task__isnull=False) & Q(complete=False)  & Q(user=request.user))
    )
    p = padding['padd']

    # for count complete
    complate = Task.objects.aggregate(
        com = Count('task', filter=Q(task__isnull=False) & Q(complete=True)  & Q(user=request.user))
    )
    c = complate['com']
    obj1 = Task.objects.filter(user=request.user)

    return render(request,"padding.html",{'Tasks': obj1,'padding':p, "complete": c})

@login_required(login_url="/log_in/")
def completed(request):
     # for conut padding
    padding = Task.objects.aggregate(
        padd = Count('task', filter=Q(task__isnull=False) & Q(complete=False)  & Q(user=request.user))
    )
    p = padding['padd']

    # for count complete
    complate = Task.objects.aggregate(
        com = Count('task', filter=Q(task__isnull=False) & Q(complete=True)  & Q(user=request.user))
    )
    c = complate['com']
    obj1 = Task.objects.filter(user=request.user)

    return render(request,"completed.html",{'Tasks':obj1,'padding':p, "complete": c})

@login_required(login_url="/log_in/")
def complate(request,id):
    id = id
    obj = Task.objects.get(id=id)
    obj.complete = True
    obj.save()
    return redirect("home")

@login_required(login_url="/log_in/")
def add_task(request):
     # for conut padding
    padding = Task.objects.aggregate(
        padd = Count('task', filter=Q(task__isnull=False) & Q(complete=False)  & Q(user=request.user))
    )
    p = padding['padd']

    # for count complete
    complate = Task.objects.aggregate(
        com = Count('task', filter=Q(task__isnull=False) & Q(complete=True)  & Q(user=request.user))
    )
    c = complate['com']
    if request.method == "POST":
        task = request.POST.get('task')
        due = request.POST.get('date')
        priority = request.POST.get('priority')

        Task.objects.create(
            user = request.user,
            task=task,
            due=due,
            priority=priority
            )
        return redirect("/add_task/")
    return render(request,"add_task.html",{'padding':p, "complete": c})

@login_required(login_url="/log_in/")
def clear_all(request):
    obj1= Task.objects.filter(user=request.user)
    obj1.delete()
    
    return redirect("/")
