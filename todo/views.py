from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.utils import timezone, dateformat
from django.core.serializers import serialize
from datetime import datetime

import json
from .models import UserInfo, Todo




# main part #
def index(request):
    # GET 요청
    if request.method == 'GET':
        print(request.session)
        if request.session.has_key('user'):
            return redirect('/cal')
        else:
            return render(request, 'todo/index.html', {})


    # POST 요청
    if request.method == "POST":
        id = request.POST['login-id'].strip()
        pwd = request.POST['login-pw'].strip()
        # print("input info ->>> id:{} / pwd: {}".format(id, pwd))

        try:
            db_user = UserInfo.objects.get(user_id=id)
            # print("db_user ->> ", db_user)
            # print(type(db_user))
        except:
            print("에러발쌩쓰 아이디없음")
            return render(request, 'todo/index.html', {'error_msg':'NoSuchID'})


        if db_user.password == pwd:
            request.session['user'] = id
            request.session['user_no'] = db_user.user_no

            return redirect('/cal')

        else:
            print("에러발쌩쓰 비밀번호틀림")
            return render(request, 'todo/index.html', {'error_msg':'IncorrectPW'})

    else:
        return render(request, 'todo/index.html', {'error_msg':'BadRequest'})


# user part #
def join(request):
    if request.method == 'POST':
        # 사용자가 입력한 정보 꺼내기
        id = request.POST['user_id'].strip()
        pwd = request.POST['password'].strip().strip()
        name = request.POST['name'].strip()
        birthday = request.POST['birthday']
        mail = request.POST['mail'].strip()

        # 객체
        user = UserInfo(user_id=id, password=pwd, name=name, birthday=birthday, mail=mail)
        # print(user)

        # 추가사항
        # 비밀번호 확인 만들어서 일치하는지 확인, 비밀번호 암호
        user.save()
        return redirect('/')

    else:
        return render(request, 'todo/join.html', {})


# login
def login(request):
    if request.method == "POST":
        id = request.POST['login-id'].strip()
        pwd = request.POST['login-pw'].strip()
        print("input info ->>> id:{} / pwd: {}".format(id, pwd))

        try:
            db_user = UserInfo.objects.get(user_id=id)
            print("db_user ->> ", db_user)
            # print(type(db_user))
        except:
            print("에러발쌩쓰 아이디없음")
            return render(request, 'todo/index.html', {'error_msg':'NoSuchID'})


        if db_user.password == pwd:
            request.session['user'] = id
            request.session['user_no'] = db_user.user_no

            return redirect('/cal')

        else:
            print("에러발쌩쓰 비밀번호틀림")
            return render(request, 'todo/index.html', {'error_msg':'IncorrectPW'})

    else:
        return render(request, 'todo/index.html', {'error_msg':'BadRequest'})


def logout(request):
    if request.session['user'] : #로그인 중이라면
        del(request.session['user'])
        del(request.session['user_no'])

    return redirect('/') #홈으로


# todo part #
def cal(request):

    data = {
        'user_no': request.session['user_no'],
        'date': datetime.now().strftime("%Y-%m-%d"),
    }
    print("달력실행시 날짜-> ", datetime.now().strftime("%Y-%m-%d"))
    todo_list = get_todo_list(data)

    return render(request, 'todo/todo_main.html', {'todos':todo_list})


def get_todo_list(data):
    print('list_request->>>', data)
    user_no = data['user_no']
    date = data['date']

    # print('list->>>', Todo.objects.filter(user_no=user_no, date=date))
    return Todo.objects.filter(user_no=user_no, date=date)



def addTodo(request):

    # <QueryDict: {'content': ['테스트'], 'date': ['2021-02-10'], 'user_no': ['1'], 'csrfmiddlewaretoken': ['ihGSmw29DxgNEt7r95hPy4ZkfoYm7uaR5qMNTMIiLkHk2auEwzzbM1r7WJUwPZht']}>
    print('addTodo_request->>>>', request.POST)
    # 입력한 todo db에 저장

    curr_user = UserInfo.objects.get(user_no=request.POST['user_no'])
    do_thing = Todo(content=request.POST['content'], date=request.POST['date'], user_no=curr_user)
    print('do_thing->>>>>', do_thing)
    do_thing.save()

    todo_list = get_todo_list(request.POST)
    data = json.loads(serialize('json', todo_list))

    return JsonResponse({'items': data})


def delTodo(request):
    print('delTodo_request->>>>', request.POST)

    do_thing = Todo.objects.get(pk=request.POST['todo_pk'])
    do_thing.delete()

    todo_list = get_todo_list(request.POST)
    data = json.loads(serialize('json', todo_list))

    return JsonResponse({'items': data})


def getTodo(request):
    print('getTodo_request->>>>', request.POST)

    todo_list = get_todo_list(request.POST)
    data = json.loads(serialize('json', todo_list))

    return JsonResponse({'items': data})
#
