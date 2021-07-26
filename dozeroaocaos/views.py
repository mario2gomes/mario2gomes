from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import  login_required
import requests
import sys

@login_required
def index(request):
    return render(request, 'investe/index.html')