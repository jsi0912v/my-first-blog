from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

# Create your views here.
def signup(request):
    '''
        계정생성
    '''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            ## 가입 후 자동 로그인 설정.
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main:index')
    else:
        form = UserForm()
        
    context = { 'form' : form }        
    
    return render(request, 'common/signup.html', context)