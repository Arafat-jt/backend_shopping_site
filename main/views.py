from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import pymongo
from bson import ObjectId
from bson import json_util
import json

DB = settings.DB_FILE

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

sp_db = myclient["sp_db"]

userCollection = sp_db['users']

# Create your views here.


def readDB(filename=DB):
    with open(filename, mode='r') as jsonFile:
        data = json.load(jsonFile)

    return data

def writeDB(object, location, filename=DB):
    with open(filename, mode='r') as jsonFile:
        data = json.load(jsonFile)
        temp = data['database'][location]
        temp.append(object)

    with open(filename, mode="w") as f:
        json.dump(data,f)
      
       
def index(request):
    if(request.method == 'GET'):
        return HttpResponse("The url was wrong......so there's nothing we can do:(")

    elif(request.method =='POST'):
        return HttpResponse("You are updating in the wrong places!")


def func_men(request):
    if request.method == 'GET':
        data = readDB()
        
        mens_list = data['database']['men']
        
        #dictionary  #key    #value
        res_dict = {'men' : mens_list}

        return JsonResponse(res_dict)

    elif request.method == 'POST':

        obj = json.loads(request.body)
        if (obj['add'] == 'true'):
            insert_obj = obj['dress']
            writeDB(object = insert_obj, location = 'men')

        return HttpResponse(f"POSTED {insert_obj}") 


def func_women(request):
    if request.method == 'GET':
        data = readDB()
        womens_list = data['database']['women']
        
        #dictionary  #key    #value
        res_dict = {'women' : womens_list}

        return JsonResponse(res_dict)

    elif request.method == 'POST':

        obj = json.loads(request.body)
        if (obj['add'] == 'true'):
            insert_obj = obj['dress']
            writeDB(object = insert_obj, location = 'women')

        return HttpResponse(f"POSTED {insert_obj}") 

# user authentication function when no db is used
def user_authen(request):
    users_data = readDB()
    users = users_data['database']['users']
    users_dict ={'users' : users}

    if request.method == 'GET':
        return JsonResponse(users_dict)

    elif request.method == 'POST':
        obj = json.loads(request.body)
        if (obj['add'] == 'true'):

            for user in users_dict['users']:
                print(user['email'])
                print(user['pass'])
                if(user['email'] == obj['user']['email'] and user['pass'] == obj['user']['pass']):
                    return JsonResponse({'status': 'User already exists'})
            
            insert_obj = obj['user']
            writeDB(object = insert_obj, location = 'users')
            return JsonResponse(insert_obj)

        return JsonResponse({'status':"could not add/verify user"})

#  user login function when mongodb is used
def user_login(request):
    users_list = [json.dumps(usr, default=json_util.default) for usr in userCollection.find()]

    if request.method == "GET":
        return JsonResponse(users_list, safe=False)

    elif request.method == 'POST':
        obj = json.loads(request.body)
        
        if (obj['add'] == 'true'):
            search_key = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']})

            if search_key:
                return JsonResponse({'status': 'User already exists'})
            else:
                return JsonResponse({'status': 'No user found'})
            
        else:
            return JsonResponse({'status':"could not add/verify user"})

#  user sign up function when mongodb is used
def user_signup(request):
    users_list = [json.dumps(usr, default=json_util.default) for usr in userCollection.find()]

    if request.method == "GET":
        return JsonResponse(users_list, safe=False)

    elif request.method == 'POST':
        obj = json.loads(request.body)
        
        if (obj['add'] == 'true'):

            search_key = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']})
            
            if not search_key:
                userCollection.insert_one(
                    {
                    "email": obj['user']['email'], 
                    "pass": obj['user']['pass'],
                    "username": obj['user']['username'],
                    "name": obj['user']['name'],
                    "number": obj['user']['number']
                    }
                    )
                return JsonResponse({'status': "User Added"})
            else:
                return JsonResponse({'status': 'User already exists'})
            
        else:
            return JsonResponse({'status':"could not add/verify user"})
        
