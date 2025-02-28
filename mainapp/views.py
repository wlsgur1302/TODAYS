from django.shortcuts import render, redirect
from mainapp import functions as func  # 기능 함수들 모두 functions.py 로 분리

# 로그인에 필요한 내장 함수 사용
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from mainapp.models import Members
from datetime import datetime

#  기본값: 서울
lat = "37.579871128849334"
long = "126.98935225645432"

nx_ny = {'x': "60", 'y': "127"}
current_weather = {}
current_location = {'dist1': "서울특별시", 'dist2': "중구"}

sel_lat_long = {'x': "60", 'y': "127"}
selected_weather = {}
selected_location = {'dist1': "서울특별시", 'dist2': "중구"}
# 온도 TMP / 강수량 PCP / 풍속 WSD / 습도 REH / 적설량 SNO / 전운량1 - 10(범주)


def main(request):
    return render(request, 'main.html')

def result(request):
    if request.method == 'POST':
        background = "/static/videos/rainy.mp4"
        gu = request.POST.get('sido')
        dong = request.POST.get('gugun')
        feeling = request.POST.get('feeling')
        food = request.POST.get('food')

        # 임시
        gu = "종로구"
        dong = "청운효자동"
        feeling = "슬픔"
        food = "빵"
        print('넘어온 값 확인 :', gu, dong, feeling, food)

        # 현 위치 기반
        global current_location
        current_location = func.coord_to_loc(lat, long)
        global nx_ny
        nx_ny = func.grid(lat, long)
        global current_weather
        current_weather = func.dangi_api(nx_ny['x'], nx_ny['y']).get('weather')
        
        # 선택된 날짜 기반
        global sel_lat_long
        sel_lat_long = func.location_to_coord(gu, dong)
        print('함수 잘 먹나?:', sel_lat_long)
        sel_nx_ny = func.grid(sel_lat_long['x'], sel_lat_long['y'])
        global selected_weather
        selected_weather = func.dangi_api(sel_nx_ny['x'], sel_nx_ny['y']).get('weather')

        context = {
            'background': background,
            'latitude': nx_ny['x'],
            'longitude': nx_ny['y'],

            'current_tmp': current_weather['tmp'],
            'current_location1': current_location['dist1'],
            'current_location2': current_location['dist2'],

            'selected_tmp': selected_weather['tmp'],
            'selected_latitude': sel_nx_ny['x'],
            'selected_longitude': sel_nx_ny['y'],
            'gu': gu,
            'dong': dong,
        }
        return render(request, 'result.html', context)
    else:
        # 날씨 정보 차단시 default값 출력
        background = "/static/videos/rainy.mp4"
        context = {
            'background': background
        }
    return render(request, 'result.html', context)


def login(request):
    return render(request, 'users/loginform.html')

def loginok(request):
    return render(request, '/')

# 회원가입 페이지로 이동
def signup(request):
    return render(request, 'users/signup.html')

# POST 방식으로 각 항목들을 받아서 Err가 없으면 데이터베이스에 값을 삽입하고 회원가입 완료
def signupok(request):
    if request.method == "POST":
        name = request.POST.get('members_name')
        id = request.POST.get('members_id')
        pw1 = request.POST.get('members_pw1')
        pw2 = request.POST.get('members_pw2')
        email = request.POST.get('members_email')
        
        err_data = {}
        if not(id and name and pw1 and pw2):
            err_data['error'] = "모든 값을 입력해야 합니다."
        elif pw1 != pw2:
            err_data['error'] = "비밀번호가 틀립니다."
        else:
            Members(
                name=name,
                id=id,
                pw1=make_password(pw1),
                pw2=make_password(pw2),
                email=email
                ).save()
            return redirect('/')
    return render(request, 'main.html')

def logout(request):
    request.session.flush()
    return redirect('/')

def mypage(request):
    return render(request, 'users/mypage.html')



