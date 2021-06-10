from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from .models import Contact
from django.contrib import messages 
from django.contrib.auth.models import User 
from blog.models import Post
from django.contrib.auth import authenticate,login,logout
from flask import url_for
from django.urls import reverse
from .templatetags import get_dict

#from blog.views import blogPost

import mysql.connector as mcdb
conn = mcdb.connect(host="localhost", user="root", passwd="", database='contact')
print('Successfully connected to database')
cur = conn.cursor()

def home(request): 
    print(type(request.user.username))
    cur.execute("SELECT * FROM `query`")
    context = cur.fetchall()
    return render(request, "home/home.html",{'allPosts':context})

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')
        else:
            try:
                user=User.objects.get(username=username)
                messages.error(request, " Username is already taken")
                return redirect('home')
            except:
                # Create the user
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.last_name= lname
                myuser.save()
                messages.success(request, " Your Quora account has been successfully created")
                return redirect('home')

    else:
        return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out!")
    return redirect('home')

def handleLogin(request):
    if request.method=="POST":
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials! Please try again")
            return redirect('home')
    
    return HttpResponse('404-Not Found')

cnt=183


def query(request):
    if request.method=="POST":
        user=request.user
        name=request.POST['name']
        content =request.POST['content']
        if len(name)<2 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            cur.execute("INSERT INTO `query` (`user`,`ques`,`desc`) VALUES ('{}','{}','{}')".format(user,name,content))
            conn.commit()
            messages.success(request, "Your query has been published")
            global cnt
            cnt=cnt+1
            redirect(blogPost,id=cnt)
            redirect(blogHome)
            return redirect(home)
    return render(request, "home/query.html")

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            cur.execute("INSERT INTO `category` (`name`,`email`,`phone`,`content`) VALUES ('{}','{}','{}','{}')".format(name,email,phone,content))
            conn.commit()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def use(request,user):
    cur.execute("SELECT * FROM `query` WHERE `user`='{}'".format(user))
    context = cur.fetchall()
    profile=User.objects.get(username=user)
    print(type(profile))
    return render(request,"home/user.html",{'user':profile,'myPosts':context})

def delete(request,id):
    cur.execute("delete from `query` where `id` = {}".format(id))
    conn.commit() 
    messages.success(request, "Your message has been deleted")
    redirect(blogHome)
    return redirect(home)

def edit(request,id):
    cur.execute("select * from `query` where `id` = {}".format(id))
    data=cur.fetchone()
    redirect(blogHome)
    redirect(blogPost,id=id)
    return render(request, 'home/edit.html', {'data': data})

def update(request,id):
    if request.method == 'POST':
        ques= request.POST['name']
        desc = request.POST['content']
        cur.execute("update `query` set `ques` ='{}' where `id`='{}'".format(ques,id))
        conn.commit()
        cur.execute("update `query` set `desc` ='{}' where `id`='{}'".format(desc,id))
        conn.commit()
        return redirect(home)
    return redirect(home)

def blogPost(request,id):
    cur.execute("SELECT * FROM `query` WHERE `id`='{}'".format(id))
    context=cur.fetchall()
    cur.execute("SELECT * FROM `comments` WHERE `post`={} and `parent` is NULL".format(id))
    comments=cur.fetchall()
    cur.execute("SELECT * FROM `comments` WHERE `post`={} and `parent` is NOT NULL".format(id))
    replies=cur.fetchall()
    repDict={}
    for reply in replies:
        if reply[4] not in repDict.keys():
            repDict[reply[4]]=[reply]
        else:
            repDict[reply[4]].append(reply)

    print(repDict)        
    return render(request,'blog/blogPost.html',{'post':context,'comments':comments,'replyDict':repDict})

def blogHome(request):
    cur.execute("SELECT * FROM `query`")
    context = cur.fetchall()
    return render(request,'blog/blogHome.html',{'allPosts':context})

def postComment(request,id):
    if request.method=='POST':
        comment=request.POST["comment"]
        user1=request.user
        postsno=id
        #cur.execute("SELECT `sno` FROM `comments` where `id`={}".format(id))
        parentSno=request.POST["parentSno"]
        if parentSno == "":
            cur.execute("INSERT INTO `comments`(`comment`,`user`,`post`) VALUES ('{}','{}','{}')".format(comment,user1,postsno))
            conn.commit()
            messages.success(request,"Your comment has been posted successfully")
        else:
            cur.execute("INSERT INTO `comments`(`comment`,`user`,`post`,`parent`) VALUES ('{}','{}','{}','{}')".format(comment,user1,postsno,parentSno))
            conn.commit()
            messages.success(request,"Your reply has been posted successfully")
    return redirect("/blog/{}".format(id))


if __name__ == "__main__":
        home()