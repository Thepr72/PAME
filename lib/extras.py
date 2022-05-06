from django.contrib.sessions.models import Session
from authentication.models import User
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta, datetime
from jwt.exceptions import DecodeError
from ast import literal_eval
from random import shuffle
import json
import jwt

from lib.responses import *


JWT_KEY = "ftpetIyX4B0FklTtzFM44Ix5oTmbvcNKw7eWQiFYbZD3SNDtX6"
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TYPE = {
    0: "kinestesico",
    1: "auditivo",
    2: "visual"
}


class MainClass(View):
    body = None
    fields_required = None
    files_required = None
    content_type = None
    login_required = False
    data_required = False

    def parse_data(self, request):
        if not self.data_required:
            return None

        try:
            if self.body is None:
                data = json.loads(request.body.decode('utf8'))
            else:
                data = json.loads(request.POST.get(self.body))

            print(data)

            if data is None:
                return JsonResponse(MISSING_PARAMETERS, status=422)

        except json.decoder.JSONDecodeError:
            print("JSON DECODER ERROR")
            print(self.body)
            print(request.POST.get('request'))
            return JsonResponse(BAD_REQUEST, status=400)

        print(self.fields_required)

        if self.fields_required is not None and not all(field in data for field in self.fields_required):
            return JsonResponse(MISSING_PARAMETERS, status=422)

        return data

    def get_user(self, request):
        if not self.login_required:
            return None

        if 'HTTP_AUTHORIZATION' in request.META:
            header = request.META.get('HTTP_AUTHORIZATION')
        else:
            return JsonResponse(INVALID_CREDENTIALS, status=403)

        fields = header.split(' ')
        if len(fields) == 2 and fields[0] == 'Bearer':
            token = fields[1]

        try:
            credentials = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        except DecodeError as e:
            print(e)
            return JsonResponse(TOKEN_ERROR, status=400)
        except Exception as e:
            print(e)
            return JsonResponse(SERVER_ERROR, status=500)

        if credentials is None:
            print("credentials decoding\n", INVALID_CREDENTIALS)
            return JsonResponse(INVALID_CREDENTIALS, status=403)

        now = datetime.now()
        generated = datetime.strptime(
            credentials['generation'].split(".")[0], TIME_FORMAT)
        expires = datetime.strptime(
            credentials['expiration'].split(".")[0], TIME_FORMAT)

        if generated is None or expires is None:
            print("dates decoding\n", INVALID_CREDENTIALS)
            return JsonResponse(INVALID_CREDENTIALS, status=403)

        if not (generated < now < expires):
            print("expired token\n", INVALID_CREDENTIALS)
            return JsonResponse(INVALID_CREDENTIALS, status=403)

        if request.session.session_key is None:
            request.session._set_session_key(credentials['id'])

        valid_key = request.session._validate_session_key(
            request.session.session_key
        )
        session = request.session._get_session()

        try:
            user = User.objects.get(email=credentials['email'])
        except User.DoesNotExist as e:
            print(e)
            return JsonResponse(INVALID_CREDENTIALS, status=403)

        if valid_key and len(session.keys()) > 0:
            return user

        return JsonResponse(INVALID_CREDENTIALS, status=403)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if self.content_type is not None and request.content_type != self.content_type:
            return JsonResponse(WRONG_CONTENT_TYPE, status=415)

        data = self.parse_data(request)
        if isinstance(data, JsonResponse):
            return data

        if self.files_required is not None and not all(file in request.FILES for file in self.files_required):
            return JsonResponse(MISSING_FILE, status=422)

        # user = self.get_user(request)
        # if isinstance(user, JsonResponse):
        #     return user
        # print(user)
        return super().dispatch(request, data=data, *args, **kwargs)


def extract_data(request):
    try:
        try:
            dictionary = json.loads(request.body.decode('utf8'))
        except Exception as e:
            print(e.args)
            dictionary = literal_eval(request.body.decode('utf8'))
        return dictionary
    except Exception as e:
        print(e.args)
        return None


def date_convert(date, str_format="%Y-%m-%dT%H:%M:%S.%fZ"):
    try:
        date = datetime.strptime(date, str_format)
    except Exception as e:
        print(e)
        return None
    return date


  

def save_grades(kind, user_id):
    user = User.objects.get(id=user_id)

    Cuestionario.objects.create(
        profile=user,
        results=kind
    )


def get_user_session(session_id):
    session = None
    try:
        session = Session.objects.get(pk=session_id)
    except Session.DoesNotExist as e:
        return None

    return session


def check_user_permission(usr_id, course_id):
    try:
        course = Curso.objects.get(id=course_id)
        if course.profesor == User.objects.get(id=usr_id):
            return True
        return False
    except Curso.DoesNotExist as e:
        print(e.args)
        return None


def save_homework(usr_id, course_id, data):
    if check_user_permission(usr_id, course_id):
        Tarea.objects.create(
            FK_curso=Curso.objects.get(id=course_id),
            titulo=data['titulo'],
            descripcion=data['descripcion'],
            fecha_limite=dateConverter(data['limite']),
            tipo=data['tipo']
        )
        return True
    return False


def get_user_permissions(usr_id):
    try:
        profile = Profile.objects.get(user=usr_id)
    except Profile.DoesNotExist as e:
        return None
    return profile.profile_type


def get_homework(usr_id, course_id):
    home = Tarea.objects.filter(
        FK_curso=course_id, closed=False).order_by('-fecha_limite')

    return home


def is_professor(usr_id):
    prof = Profile.objects.get(user=usr_id).profile_type

    if prof > 2:
        return False
    return True


def get_usr(usr_id):
    return User.objects.get(id=usr_id)


def create_course(usr_id, data):
    Curso.objects.create(
        nombre=data['nombre'],
        curso_pass=data['pass'],
        profesor=User.objects.get(id=usr_id),
        fecha_inicio=dateConverter(data['inicio']),
        fecha_fin=dateConverter(data['fin']),
        activo=True
    )


def is_course_owner(usr_id, course_id):
    usr = get_usr(usr_id)

    curso = Curso.objects.filter(id=course_id, profesor=usr)

    if curso is not None:
        return True
    return False


def get_courses(usr_id):
    response = None

    if is_professor(usr_id):
        courses = Curso.objects.filter(profesor=usr_id)

        response = [
            {
                'id': course.id,
                'nombre': course.nombre,
                'profesor': {
                    'nombre': course.profesor.first_name,
                    'apellido': course.profesor.last_name
                },
                'inicio': course.fecha_inicio,
                'fin': course.fecha_fin,
                'activo': course.activo
            }
            for course in courses
        ]
    else:
        courses = Curso_alumno.objects.filter(FK_alumno=usr_id)
        courses2 = []

        for course in courses:
            courses2.append(course.FK_curso)

        response = [
            {
                'id': course.id,
                'nombre': course.nombre,
                'profesor': {
                    'nombre': course.profesor.first_name,
                    'apellido': course.profesor.last_name
                },
                'inicio': course.fecha_inicio,
                'fin': course.fecha_fin,
                'activo': course.activo
            }
            for course in courses2
        ]

    if len(response) == 0:
        response = {
            'Status': 'No courses for current user'
        }

    return response


def update_course(course_id, data):
    course = Curso.objects.get(id=course_id)

    course.update(data)

    return ALL_OK


def delete_course(course_id):
    course = Curso.objects.get(id=course_id)

    course.delete()

    return ALL_OK


'''
def get_note_instance(user, home):
    return 
'''


def get_instance(model, pk):
    try:
        instance = model.objects.get(pk=pk)
    except Exception as e:
        print(e)
        return None
    return instance


def get_notes(curso, user=None):
    notes = None
    response = None
    if user is not None:
        try:
            notes = Calificacion.objects.filter(FK_curso=curso, FK_alumno=user)
        except Calificacion.DoesNotExist as e:
            return None

        response = [
            {
                'tarea': note.FK_tarea.nombre,
                'nota': note.nota
            }
            for note in notes
        ]

    if len(response) == 0:
        response = {
            'Status': 'No notes for this user'
        }
    else:
        try:
            notes = Calificacion.objects.filter(FK_curso=curso)
        except Calificacion.DoesNotExist as e:
            return None

        response = [
            {
                'tarea': note.FK_tarea.nombre,
                'alumno': note.FK_user.first_name + ' ' + note.FK_user.last_name,
                'nota': note.nota
            }
            for note in notes
        ]

    return response


def update_note(course, user, home, note):
    try:
        note = Calificacion.objects.get(
            FK_curso=course, FK_user=user, FK_tarea=home)
        note.update(note)
    except Calificacion.DoesNotExist as e:
        return SERVER_ERROR

    return ALL_OK


def update_homework(home_id, data):
    home = Tarea.objects.get(pk=home_id)
    home.update(data)
    return ALL_OK


def delete_homework(home_id):
    home = Tarea.objects.get(pk=home_id)
    home.delete()

    return ALL_OK


def generate_token(request, email):
    now = datetime.now()

    expiration = now + timedelta(weeks=26)

    payload = {
        "id": request.session.session_key,
        "email": email,
        'generation': str(now),
        'expiration': str(expiration),
    }

    return jwt.encode(payload, JWT_KEY, algorithm='HS256').decode('utf-8')