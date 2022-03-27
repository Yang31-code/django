from django.http.response import JsonResponse
from .models import User, Course, Professor, Rate

from django.middleware.csrf import get_token


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    try:
        User.objects.get(username=username)

        data = {
            'message': 'username already registered.'
        }

        return JsonResponse(data, status=400, safe=False)
    except:
        User.objects.create(username=username, password=password, email=email, is_login=False)

        data = {
            'message': 'register done.',
        }

        return JsonResponse(data, status=200, safe=False)


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
        user = User.objects.get(username=username, password=password)
        user.token = get_token(request)
        user.is_login = True
        user.save()

        data = {
            'message': 'welcome, ' + user.username,
            'token': user.token
        }

        return JsonResponse(data, status=200, safe=False)
    except:
        data = {
            'message': 'wrong username or password'
        }
        return JsonResponse(data, status=400, safe=False)


def logout(request):
    token = request.POST.get("token")
    username = request.POST.get("username")

    try:
        user = User.objects.get(token=token, username=username)
        user.token = ""
        user.is_login = False
        user.save()

        data = {
            'message': 'logout'
        }

        return JsonResponse(data, status=200, safe=False)
    except:

        data = {
            'message': 'please login first.'
        }

        return JsonResponse(data, status=400, safe=False)


def list_all(request):
    course_list = list(
        Course.objects.all().values('id', 'code', 'name', 'year', 'semester', 'taught_by__code', 'taught_by__name'))

    return JsonResponse(data={'list':[course_list]}, status=200, safe=False)


def view_all(request):
    professors = Professor.objects.all()

    rates = []
    for professor in professors:
        total = 0
        ratings = Rate.objects.filter(professor=professor)
        for rating in ratings:
            total += rating.rate
        if len(ratings) > 0:
            rate = total / len(ratings)
        else:
            rate = 0
        rates.append({'code': professor.code, 'name': professor.name, 'rate': round(rate)})

    return JsonResponse(data={'list': rates}, status=200, safe=False)


def view_average(request):
    professor = request.POST.get("professor")
    course = request.POST.get("course")

    course = Course.objects.filter(code=course)
    professor = Professor.objects.get(code=professor)

    ratings = Rate.objects.filter(professor=professor, course=course[0])

    total = 0
    for rating in ratings:
        total += rating.rate
    if len(ratings) > 0:
        rate = total / len(ratings)
    else:
        rate = 0
    data = {'id': professor.code, 'professor': professor.name, 'rate': round(rate),
            'code': course[0].code, 'course': course[0].name}

    return JsonResponse(data=data, status=200, safe=False)


def rate(request):
    professor = request.POST.get("professor")
    course = request.POST.get("course")
    year = request.POST.get("year")
    semester = request.POST.get("semester")
    rate = request.POST.get("rate")
    token = request.POST.get("token")

    try:
        user = User.objects.get(token=token)
        try:
            professor = Professor.objects.get(code=professor)
            course = Course.objects.get(code=course, year=year, semester=semester)
            try:
                Rate.objects.get(user=user, professor=professor, course=course)

                data = {
                    'message': 'already rated.',
                }

                return JsonResponse(data, status=400, safe=False)

            except:
                Rate.objects.create(user=user, professor=professor, course=course, rate=rate)

                data = {
                    'message': 'done.',
                }

                return JsonResponse(data, status=200, safe=False)

        except:
            data = {
                'message': 'wrong information.',
            }

            return JsonResponse(data, status=400, safe=False)
    except:
        data = {
            'message': 'please login first.',
        }

        return JsonResponse(data, status=400, safe=False)
