from django.shortcuts import render, redirect

# Create your views here.
def cats(request):
  return render(request, 'cats.html')