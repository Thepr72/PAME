from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.handlers.modwsgi import check_password
from django.db.utils import IntegrityError
from django.http import JsonResponse

from cursos.models import Course


User = get_user_model()


class SignUp(MainClass):
    data_required = True
    content_type = 'application/json'
    fields_required = (
        'code',
        'email',
        'password',
        'first_name',
        'last_name'
    )

    def post(self, request, data, *args, **kwargs):
        try:
            user = User.objects.create_user(
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                profile_type=3,
                code=data['code']
            )

        except IntegrityError:
            return JsonResponse(USER_ALREADY_EXISTS)

        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)

        try:
            user = authenticate(
                request=request,
                username=data['email'],
                password=data['password']
            )

            if user is not None:
                login(request, user)

                if not request.session.exists(request.session.session_key):
                    request.session.create()

              

                
            return JsonResponse(INVALID_CREDENTIALS, status=403)
        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)


class Login(MainClass):
    data_required = True
    content_type = 'application/json'
    fields_required = (
        'username',
        'password'
    )

    def post(self, request, data, *args, **kwargs):
        try:
            user = authenticate(
                request=request,
                username=data['username'],
                password=data['password']
            )

            if user is not None:
                login(request, user)

                if not request.session.exists(request.session.session_key):
                    request.session.create()

               


            return JsonResponse(INVALID_CREDENTIALS, status=403)
        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)


class getProfile(MainClass):
    login_required = True

    def get(self, request, user, *args, **kwargs):
        try:
           

            courses = Course.objects.filter(students__email=user.email)
            response = {
                **ALL_OK,
                'user':
                    {
                        'username': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'code': user.code,
                        'date_joined': user.date_joined,
                        'profile_type': user.profile_type,
                        'learning_type': ltype,
                    }
            }

            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)


class UpdateProfile(MainClass):
    login_required = True
    data_required = True
    content_type = 'application/json'
    fields_required = (
        'username',
        'password',
    )

    def post(self, request, user, data, *args, **kwargs):
        try:
            valid_credentials = False
            try:
                valid_credentials = check_password(
                    user, data['username'], data['password'])
            except Exception as e:
                print(e)
                return JsonResponse(INVALID_CREDENTIALS)

            print(valid_credentials)

            if valid_credentials:
                get_user = User.objects.get(email=data['username'])

                if data['new_password'] is not None and data['confirm_new_password'] is not None:
                    if 'new_password' and 'confirm_new_password' in data:
                        if data['new_password'] == data['confirm_new_password']:
                            get_user.set_password(data['new_password'])
                        else:
                            return JsonResponse(PASSWORDS_DONT_MATCH, status=403)

                if 'new_username' in data:
                    get_user.username = data['new_username']
                if 'first_name' in data:
                    get_user.first_name = data['first_name']
                if 'last_name' in data:
                    get_user.last_name = data['last_name']
                if 'code' in data:
                    get_user.code = data['code']

                get_user.save()

                if 'new_password' in data:
                    user = authenticate(
                        request=request,
                        username=data['username'],
                        password=data['new_password']
                    )

                
                

                return JsonResponse(response)

            else:
                return JsonResponse(INVALID_CREDENTIALS, status=403)

        except Exception as e:
            return(e)
            return JsonResponse(INVALID_CREDENTIALS, status=403)





class Logout(MainClass):
    login_required = True

    def post(self, request, user, *args, **kwargs):
        try:
            logout(request)
        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)

        return JsonResponse(ALL_OK)