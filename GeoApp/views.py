from django.shortcuts import redirect

def redirection(request):
    return redirect('hello_page', permanent = True)
