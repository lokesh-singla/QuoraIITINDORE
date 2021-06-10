from django.shortcuts import render,HttpResponse,redirect
from .models import Post
from django.contrib.auth.models import User
from django.urls import path

import mysql.connector as mcdb
conn = mcdb.connect(host="localhost", user="root", passwd="", database='contact')
print('Successfully connected to database')
cur = conn.cursor()

# Create your views here.
def blogHome(request):
    cur.execute("SELECT * FROM `query`")
    context = cur.fetchall()
    return render(request,'blog/blogHome.html',{'allPosts':context})

def blogPost(request,id):
    cur.execute("SELECT * FROM `query` WHERE `id`='{}'".format(id))
    context=cur.fetchall()
    return render(request,'blog/blogPost.html',{'post':context})
  
