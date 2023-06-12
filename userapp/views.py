from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.

class Home(TemplateView):
    template_name = "home.html"

# サインアップはDjangoが提供してくれる機能を最大限使う
def signup_func(request):
    form = SignUpForm
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save()
            #バリデート後にusernameをlast_name + first_nameで作成
            lastName = form.cleaned_data.get("last_name")
            firstName = form.cleaned_data.get("first_name")
            username = lastName + firstName

            eMail = form.cleaned_data.get("email")
            new_user = User(username=username, last_name=lastName, first_name=firstName, email=eMail,password="default_password")

            #パスワードは後から設定するっぽい。
            new_user.set_password(form.cleaned_data.get("password1"))

            new_user.save()

            return redirect("signin")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin_func(request):
    # form = SignInForm
    if request.method == "POST":
        # form = SignInForm(request.POST)
        # if form.is_valid():
            # eMail = form.cleaned_data.get("email")
            # passWord = form.cleaned_data.get("password")

        eMail = request.POST["email"]
        passWord = request.POST["password"]

        print("ここまで来たよん")
        print(eMail)
        print(passWord)

        #本来はuser = authenticate()とするのが良いが、email認証はダメっぽい。
        try:
            user = User.objects.get(email=eMail)
            print("メールアドレスが一致するユーザーを確認しました。")
        except:
            print("メールアドレスが一致するユーザーを確認できませんでした")
            return render (request, "signin.html", {"message":"メールアドレス、またはパズワードが間違っています"})
        
        # メールアドレスが一致するUserを取得した時のみここを通過する

        if check_password(passWord, user.password):
            login(request, user)
            print("ログイン完了！！！")
            return redirect("home")
        else:
            print("パスワードが一致しない")
            return render (request, "signin.html", {"message":"メールアドレス、またはパズワードが間違っています"})
                
    else:
        return render(request, 'signin.html')