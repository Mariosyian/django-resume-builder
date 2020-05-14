"""resumebuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

# Import local files from local directory
from ..resume import views as resume_views  # ../resume/views.py
from ..user import views as user_views      # ../user/views.py

# Maps '<string>' endpoint to a views.py method that returns
# the page to be loaded in the website.
urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Empty string = home page
    path(r'', RedirectView.as_view(pattern_name='resume')),

    # ../resume/* imported as resume_views
    # Read as: In ../resume/views.py call method resume_view()
    path(r'resume/', resume_views.resume_view, name='resume'),
    path(
        r'resume/item/edit/<int:resume_item_id>/',
        resume_views.resume_item_edit_view,
        name='resume-item-edit'
    ),
    path(
        r'resume/item/create/',
        resume_views.resume_item_create_view,
        name='resume-item-create'
    ),

    # ../user/* imported as user_views
    path(r'user/', user_views.account_edit_view, name='account-edit'),
    path(
        r'create-account/',
        user_views.account_create_view,
        name='account-create'
    ),
]
