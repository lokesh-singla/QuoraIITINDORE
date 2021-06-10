from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('query', views.query, name="query"),
    path('signup', views.handleSignUp, name="handleSignUp"),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('<str:user>',views.use,name="use"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('edit/update/<int:id>', views.update, name="update"),
    path('blog/<int:id>', views.blogPost,name="blogPost"),
    path('blog/', views.blogHome,name="blogHome"),

    # API to post comment
    path('blog/postComment/<int:id>',views.postComment,name="postComment"),
]
