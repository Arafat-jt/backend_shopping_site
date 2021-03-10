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

# Variables pointing to each collection
userCollection = sp_db['users']

mensCollection = sp_db['men_attire']

womensCollection = sp_db['women_attire']

watchCollection = sp_db['watches']

othersCollection = sp_db['others']

elecCollection = sp_db['electronics']

jacketsCollection = sp_db['jackets']

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
      
#empty fun points to nothing       
def index(request):
    if(request.method == 'GET'):
        return HttpResponse("The url was wrong......so there's nothing we can do:(")

    elif(request.method =='POST'):
        return HttpResponse("You are updating in the wrong places!")

# men function when no db is used
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

# women function when no db is used
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




# men function when sp_db db is used
def mens_wear(request):
    # mens_list = [json.dumps(men, default=json_util.default) for men in mensCollection.find()]
    cursor = mensCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)

# women function when sp_db db is used
def womens_wear(request):
    # womens_list = [json.dumps(women, default=json_util.default) for women in womensCollection.find()]
    cursor = womensCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)

#fun accessing 'other' Collection from sp_db
def fun_others(request):
    cursor = othersCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)

#fun accessing 'electronics' Collection from sp_db
def fun_elec(request):
    cursor = elecCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)

#fun accessing 'watches' Collection from sp_db
def fun_watches(request):
    cursor = watchCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)

#fun accessing 'watches' Collection from sp_db
def fun_jackets(request):
    cursor = jacketsCollection.find()
    x = []
    for i in cursor:
        x.append(i)

    if request.method == 'GET':
        return JsonResponse({'status': 'OK', 'catalog': x}, safe=False)



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

# updates user's credentials
def user_update(request):
    users_list = [json.dumps(usr, default=json_util.default) for usr in userCollection.find()]

    if request.method == "GET":
        return JsonResponse(users_list, safe=False)
        
    elif request.method == 'POST':
        obj = json.loads(request.body)

        if (obj['add'] == 'true'):
            
            userCollection.update(
                {"email": obj['user']['email'], "pass": obj['user']['pass']},
                 {"$set": {"username": obj['user']['username'], "name": obj['user']['name'], "number": obj['user']['number']}}
            )
            user_details = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']},{"_id": 0})    
            return JsonResponse({'status':"Credentials updated", "Details": user_details})

        else:
            return JsonResponse({'status':"could not add/verify user"})


# this part converts the collection to cursor to array
cart_cursor = userCollection.find({},{"products": 1, "_id": 0})
all_products = []
for i in cart_cursor:
    all_products.append(i)
# all_products contains all the users' product lists


# adds a product to user collection sp_db
def addtocart(request):

    if request.method == "GET":

        return JsonResponse(all_products, safe=False)

    elif request.method == "POST":
    
        obj = json.loads(request.body)
        
        if (obj['add'] == 'true'):

            search_key = userCollection.find_one(
                {
                    "email": obj['user']['email'], 
                    "pass": obj['user']['pass'], 
                    "products":{ 
                        "$elemMatch": {"product_id": obj['user']['product_id']}
                        }
                }
            )

            # print(search_key)
            # return JsonResponse({"status": "hi"})
            if search_key:
                userCollection.update(
                        {"email": obj['user']['email'], "pass": obj['user']['pass'], "products":{"$elemMatch": {"product_id": obj['user']['product_id']}}},
                        {"$inc": {"products.$.quantity": 1}}
                    )
                # returns only user specific products
                user_products = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']},{"products": 1, "_id": 0})
                return JsonResponse({"status": "Successfully incremented product quantity", "Products": user_products})

            else:   
                userCollection.update(
                    {"email": obj['user']['email'], "pass": obj['user']['pass']},
                    { "$push": 
                        {"products": 
                            {"product_id": obj['user']['product_id'], "quantity": 1}   
                        }
                    }
                )
                # returns only user specific products
                user_products = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']},{"products": 1, "_id": 0})
                return JsonResponse({"status": "Successfully assigned product to user", "Products": user_products})

        else:
            return JsonResponse({'status':"could not add/verify user"})
            
# returns all products for a user in sp_db
def mycart(request):

    if request.method == "GET":
        
        return JsonResponse({'status': 'OK', 'Products': all_products}, safe=False)

    elif request.method == "POST":
        obj = json.loads(request.body)
        
        if (obj['return'] == 'true'):

            cursor2 = userCollection.find_one({"email": obj['user']['email'], "pass": obj['user']['pass']},{"products": 1, "_id": 0})

            # final list sent to fontend
            users_products = []
            # converts list of obj to list of lists
            p_ids = []
            for i in cursor2["products"]:
                for j in i.items():
                    p_ids.append(j[1])

            # has products_id only
            p_ids2 = p_ids[::2]
            
            # has quantity of each product
            p_quantity = p_ids[1::2]

            # print(p_quantity)
            # print(p_ids2)

            # compare every product_id from given user, append its corresponding product to final list
            for index,i in enumerate(p_ids2):
                if mensCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(mensCollection.find_one({"_id": i}))

                if womensCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(womensCollection.find_one({"_id": i})) 

                if elecCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(elecCollection.find_one({"_id": i}))

                if watchCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(watchCollection.find_one({"_id": i}))

                if jacketsCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(jacketsCollection.find_one({"_id": i}))

                if othersCollection.find_one({"_id": i}):
                    # for j in range(p_quantity[index]):
                        users_products.append(othersCollection.find_one({"_id": i}))

            return JsonResponse({"quantity": p_quantity, "catalog": users_products})



