from django.shortcuts import render
from django.http import HttpResponse
import pymongo
from django.core.files.storage import FileSystemStorage

# Create your views here.
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['facebookdatabase']
mycol = mydb['registeredusers']

def index(request):
	return render(request,'postuploadapp/homepage.html')
	
def register(request):
	if request.method == 'POST' and request.FILES['img']:
		u = request.POST.get('username')
		p = request.POST.get('password')
		x = mycol.find({'username':u,'password':p})
		for i in x:
			return HttpResponse("Username already exist")
		else:
			img = request.FILES['img']
			fs = FileSystemStorage()
			filename = fs.save(img.name, img)
			uploaded_file_url = fs.url(filename)
			f = {'username':u,'password':p,'pimg':uploaded_file_url}
			# image.save("C:/Mscit/yudiz/postupload/media/")
			#x = mycol.find({},{"username": "","_id":0})
			mycol.insert_one(f)
		return render(request,'postuploadapp/homepage.html')


def signup(request):
	return render(request,'postuploadapp/signup.html')


def loginvalid(request):
	if request.method == 'POST':	
		u = request.POST.get('username')
		p = request.POST.get('password')
		image = request.POST.get('img')
		z = {'username':u,'password':p }
		users = mycol.find(z)
		for i in users:
			users = mycol.find({"username":u})
			request.session['name'] = u
			return render(request,'postuploadapp/facebookhome.html',{'u':users})

def searchfriend(request):
	s = request.GET.get('search')
	friends =mycol.find({'username':s},{'username':s,'_id':0,'pimg':''})
	return render(request,'postuploadapp/facebookhome.html',{'f':friends})


def friendsprofile(request):
	name = request.GET.get('usernames')
	x = mycol.find({'username':name},{'username':'','_id':0,'pimg':''})
	return render(request,'postuploadapp/facebookhome.html',{'frienddetails':x})


def logout(request):
	return render(request,'postuploadapp/logout.html')


def flist(request):
	u = request.session['name']
	friendscol = mydb[u]
	x = friendscol.find({'status':'pending'})
	return render(request,'postuploadapp/facebookhome.html',{'myfriendlist':x})
	

def friendrequest(request):
	u = request.session['name']
	freq = request.GET.get('username')
	friendscol = mydb[freq]
	# x = friendscol.delete_many({})
	# print(x)
	# blocklist = mydb['blocked']
	x = friendscol.find({'friend':u,'status':"blocked"})
	for b in x:
		return HttpResponse("Sorry you are temporarily blocked")
	u = request.session['name']
	freq = request.GET.get('username')
	friendscol = mydb[freq]
	f = friendscol.insert_one({'friend':u,'status':'pending'})
	return HttpResponse("Request Sent")	
	
	# return HttpResponse("done")
	# f = friendscol.insert_one({'friend':'u','status':'no'})

def requeststatustrue(request):
	a = request.GET.get('username')
	u = request.session['name']
	myfriendlist = mydb[u]
	myquery = {'friend':a,'status':"pending"}
	newvalues = { "$set": { 'status': "accepted" }}
	myfriendlist.update_one(myquery, newvalues)
	x = myfriendlist.find({})
	return render(request,'postuploadapp/facebookhome.html',{'myfriendlist':x})

def requeststatusfalse(request):
	a = request.GET.get('username')
	u = request.session['name']
	myfriendlist = mydb['blocked']
	mylist = mydb[u]

	myquery = {'friend':a,'status':'pending'}
	newvalues = { "$set": { 'status': "blocked" }}

	mylist.update_one(myquery, newvalues)
	x = mylist.find({})
	# for x in mylist.find():
	# 	print(x)
	return HttpResponse(x)
