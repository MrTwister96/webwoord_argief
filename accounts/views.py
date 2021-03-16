from django.shortcuts import render
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect

from accounts.forms import UserLoginForm

User = get_user_model()

# Create your views here.
def user_login(request, *args, **kwargs):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        user_obj = User.objects.get(username__iexact=username)
        login(request, user_obj)

        try:
            next_url = request.GET['next']
        except:
            next_url = '/'
        return HttpResponseRedirect(next_url)
    
    return render(request, 'login.html', {'form': form})

def user_logout(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect('/')
