from re import A
from django.shortcuts import redirect, render

from .forms import NewUserForm, SocialPostForm, WeatherPostForm, DogPostForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, get_user_model
import requests
import json

# Create your views here.

APIGATEWAY = "https://2ocvn11xq1.execute-api.us-east-1.amazonaws.com/prod/DynamoDBManager"

def index(request):
   return render(request, "pawBook/index.html", {
    })

def welcome(request):
   return render(request, "pawBook/welcome.html", context={
    }) 
   
def login_page(request):
   if request.method == "POST":
      form = AuthenticationForm(data=request.POST)
      if form.is_valid():
         username = form.cleaned_data.get('username')
         password = form.cleaned_data.get('password')
         user = authenticate(username=username,password=password)
         if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect('homepage')
         else:
            messages.error(request, "Invalid username or password") 
      else:
         messages.error(request, "Invalid username or password")
   elif request.user.is_authenticated:
      return redirect('homepage')
   form = AuthenticationForm()
   return render(request, "pawBook/login.html", context={"login_form":form}
    ) 

def logout_view(request):
   if request.user.is_authenticated:
      logout(request)
      return render(request, "pawBook/logout.html", context={
   })
   else:
      return redirect('login')
 
def create(request):
   if request.method == 'POST':
      form = NewUserForm(request.POST)
      if form.is_valid():
         user = form.save()
         login(request, user)
         messages.add_message(request, messages.SUCCESS, "Registration successful.")
         return redirect('login')
      messages.add_message(request, messages.ERROR,"Unsuccessful Registration")
   form = NewUserForm()
   return render(request, template_name="pawBook/createaccount.html", context={"register_form":form})

def homepage(request):
   if request.user.is_authenticated:
      dataset = {
         "operation": "list",
         "tableName": "Posts",
         "payload" : {
            "username": "Testuser"
         }
      }
      json_dump = json.dumps(dataset)
      answer = requests.post(url=APIGATEWAY,data=json_dump)

      data = json.loads(answer.text)
      posts =[] 
      for a in data['Items']:
         username = a['username']
         if username != request.user.username:
            title = a['title']
            if a['type'] == 'dogPic':
               dogUrl = "https://pawbook-images.s3.amazonaws.com/" + a['dogImg']
               content = a['content']
               post = [username, title, 'dogPic', dogUrl, content]
               posts.append(post)
            elif a['type'] == 'weather':
               temp = a['temperature']
               conditions = a['conditions']
               location = a['location']
               post = [username, title, 'weather', temp,conditions,location] 
               posts.append(post)
            elif a['type'] == 'update':
               post = [username, title, 'update', a['content']]
               posts.append(post)

      return render(request, "pawBook/homepage.html", {
         "posts":posts
         })
   else:
      return render(request, "pawBook/login.html", {
    })


def createpost(request):
   if request.user.is_authenticated:
      form = SocialPostForm(request.POST)

      if request.method == 'POST':
         if form.is_valid():
            username = request.user.username
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            dataset = {
               "operation": "create",
               "tableName": "Posts",
               "payload": {
                  "Item": {
                     "title": title,
                     "username": username,
                     "type": "update",
                     "content": content
                  }      
               }
            }
            json_dump = json.dumps(dataset)
            answer = requests.post(url=APIGATEWAY,data=json_dump)

            return redirect('homepage')

      else:
         return render(request, "pawBook/createpost.html", context={'form': form
   })
   else:
      return redirect('login')

def weatherpost(request):
   if request.user.is_authenticated:
      form = WeatherPostForm(request.POST)

      if request.method == 'POST':
         if form.is_valid():
            key =  'aa8a6fcf6f86766163a9bc9f4715c208'
            username = request.user.username
            location = form.cleaned_data["location"]
            title = form.cleaned_data["title"]

            weather = requests.post(url="https://api.openweathermap.org/data/2.5/weather?q="+ location + '&appid=' + key)

            weather2 = json.loads(weather.text)

            temp = int(weather2['main']['temp'] - 273.15)
            cond = weather2['weather'][0]['main']

            
            dataset = {
               "operation": "create",
               "tableName": "Posts",
               "payload": {
                  "Item": {
                     "username": username,
                     "title": title,
                     "type": "weather",
                     "location": location,
                     "temperature": temp,
                     "conditions": cond
                  }      
               }
            }
            json_dump = json.dumps(dataset)
            answer = requests.post(url=APIGATEWAY,data=json_dump)

            task = form.save(commit=False)
            task.usern = request.user.username

            #task.save()
            return redirect('homepage')

      else:
         return render(request, "pawBook/shareWeather.html", context={'form': form
   })
   else:
      return redirect('login')


def dogPics(request):
   if request.user.is_authenticated:
      form = DogPostForm(request.POST)
      if request.method == 'POST':
         if form.is_valid():
            username = request.user.username
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            dog = requests.get(url='https://dog.ceo/api/breeds/image/random')

            dogdata = json.loads(dog.text)
            dogImg = dogdata['message']

            dataset = {
               "image": dogImg,
            }

            json_dump = json.dumps(dataset)
            answer = requests.post(url="https://fx94ye1lta.execute-api.us-east-1.amazonaws.com/prod/PythonDynamoDBManager",data=json_dump)
            json_ans = json.loads(answer.text)
            imgName = json_ans[1]

            dataset = {
               "operation": "create",
               "tableName": "Posts",
               "payload": {
                  "Item": {
                     "username": username,
                     "title": title,
                     "type": "dogPic",
                     "content": content,
                     "dogImg": imgName,
                  }      
               }
            }

            json_dump = json.dumps(dataset)
            answer = requests.post(url=APIGATEWAY,data=json_dump)

            return redirect('homepage')
      else:
         return render(request, "pawBook/shareDog.html", context={'form':form})

   else:
      return redirect('login')


def users(request):
   if request.user.is_authenticated:
      User = get_user_model()
      users = User.objects.all()

      return render(request, "pawBook/users.html", context={"users":users
   })
   else:
      return redirect('login')

def profile(request):
   if request.user.is_authenticated:
      dataset = {
         "operation": "list",
         "tableName": "Posts",
         "payload" : {
            "username": "Testuser"
         }
      }
      json_dump = json.dumps(dataset)
      answer = requests.post(url=APIGATEWAY,data=json_dump)

      data = json.loads(answer.text)
      posts =[]
      
      for a in data['Items']:
         username = a['username']
         if username == request.user.username:
            title = a['title']
            if a['type'] == 'dogPic':
               dogUrl = "https://pawbook-images.s3.amazonaws.com/" + a['dogImg']
               content = a['content']
               post = [username, title, 'dogPic', dogUrl, content]
               posts.append(post)
            elif a['type'] == 'weather':
               temp = a['temperature']
               conditions = a['conditions']
               location = a['location']
               post = [username, title, 'weather', temp,conditions,location] 
               posts.append(post)
            elif a['type'] == 'update':
               post = [username, title, 'update', a['content']]
               posts.append(post)

      return render(request, "pawBook/profile.html", 
      {
         "posts":posts
   })
   else:
      return render(request, "pawBook/login.html", {
    })