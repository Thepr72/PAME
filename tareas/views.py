from dataclasses import field
from http.client import BAD_REQUEST, FORBIDDEN, NOT_FOUND
from pydoc import describe
from re import M
from tempfile import TemporaryFile
from turtle import home
from urllib import response
from xmlrpc.client import ResponseError
from django.http import JsonResponse
from django.db.models import Q
from tareas.models import Homework, Response
from cursos.models import Course

from lib.extras import MainClass, date_convert
from lib.responses import *


class NewHomework(MainClass):
    body = 'request'
    login_required = True
    data_required = True
    fields_required = (
        'course',
        'title',
        'description',
        'limit',
    )

    def post(self, request, user, data, *args, **kwargs):

        if user.profile_type == 3:
            return JsonResponse(FORBIDDEN, status=403)

        file = None

        if 'file' in request.FILES:
            file = request.FILES.get('file')

        try:
            course = Course.objects.get(id=data['course'])
        except Course.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)
        
        try:
            homework = Homework.objects.create(
                title=data['title'],
                description=data['description'],
                limit=date_convert(data['limit']),
                file=file

            )

            course.homework.add(homework)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)
        
        response = {
            **ALL_OK,
            'homework': {
                'id': homework.id,
                **data,
                'file': None if file is None else file.name
            }
        }

        return JsonResponse(response)


class GetHomework(MainClass):
    login_required = True

    def get(self, request, user, course, *arg, **kwargs):

        try:
            course = Course.objects.get(id=course)
        except Course.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        try:
            homework = course.homework.all()
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        response = {
            **ALL_OK,
            'homework': [
                {
                    'id': h.id,
                    'title': h.title,
                    'description': h.description,
                    'limit': h.limit,
                    'closed': h.closed,
                    'responses': [
                        {
                            'id': r.id,
                            'student': r.student.get_full_name(),
                            'sent': r.sent,
                            'grade': r.grade,
                            'graded': True if r.grade is not None else False,
                            'file': r.file.url if r.file else None,
                            'answer': r.answer
                        }
                        for r in h.response.all()
                    ]
                }
                for h in homework
            ]
        }

        if user.profile_type == 3:
            response = {
                **ALL_OK,
                'homework': [
                    {
                        'id': h.id,
                        'title': h.title,
                        'description': h.description,
                        'limit': h.limit,
                        'closed': h.closed,
                        'response': [
                            {
                                'id': r.id,
                                'sent': r.sent,
                                'grade': r.grade,
                                'graded': True if r.grade is not None else False,
                                'file': r.file.url if r.file else None,
                                'answer': r.answer
                            }
                            for r in h.response.filter(student=user)
                        ]
                    }
                    for h in homework
                ]
            }

        return JsonResponse(response)

    

class GetHomeworkDetails(MainClass):
    login_required = True

    def get(self, request, user, homework, *args, **kwargs):
        try:
            homework = Homework.objects.get(
                Q(id=homework) &
                Q(
                    Q(course_professor=user) |
                    Q(course_students_in=[user])
                )
            )
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)
        
        response = {
            **ALL_OK,
            'homework': {
                'id': homework.id,
                'title': homework.title,
                'description': homework.description,
                'file': homework.file.urls if homework.file else None,
                'limit': homework.limit,
                'kind': homework.kind,
                'closed': homework.closed,
                'response': [
                    {
                        'id': r.id,
                        'answer': r.answer,
                        'file': r.file.url if r.url else None,
                        'sent': r.sent,
                        'grade': r.grade,
                        'graded': True if r.grade is not None else False
                    }
                    for r in homework.response.all()
                ]
            }
        }

        return JsonResponse(response)

class UpdateHomework(MainClass):
    body = 'request'
    login_required = True
    data_required = True
    fields_required = (
        'id',
    )

    def post(self, request, user, data, *arg, **kwargs):
        if user.profile_type == 3:
            return JsonResponse(FORBIDDEN, status=403)
        
        file = None

        if 'file' in request.FILES:
            file = request.FILES.get('file')
            data['file'] = file
        
        try:
            Homework.objects.filter(
                Q(id=data['id'] & Q(course_professor=user))
            ).update(**data)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)
        
        response= {
            **ALL_OK,
            'homework': {
                'status': 'updated',
                **data,
                'file': None if file is None else file.name
            }
        }

        return JsonResponse(response)


class DeleteHomework(MainClass):
    login_reuired = True

    def get(self, request, user, homework, *arfs, **kwargs):
        try:
            Homework.objects.filter(
                Q(id=homework) & Q(course_professor=user)
            ).delete()
        
        except Homework.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)
        except Exception:
            return JsonResponse(BAD_REQUEST, status=400)
        

        return JsonResponse(ALL_OK)

class UploadResponse(MainClass):
    body = 'request'
    login_required = True
    data_required = True
    content_type = 'multipart/form-data'
    fiedls_required = (
        'homework',
        'answer'
    )

    def post(self, request, user, data, *args, **kwargs):
        
        print(type(data))

        try:

            r = {
                'student': user,
                'answer': data['answer'],
                'sent': True
            }

            r['file'] = None

            if 'file' in request.FILES:
                r['file'] = request.FILES.get('file')

            homework = Homework.objects.get(id=data['homework'])
            response = Response.objects.create(**r)
            homework.response.add(response)

        except Homework.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)
        
        response = {
            **ALL_OK,
            'response': {
                'id': response.id,
                **data,
                'file': None if r['file'] is None else r['file'].name
            }
        }

        return JsonResponse(response)

class UpdateResponse(MainClass):
    body = 'request'
    login_required = True
    data_required = True
    content_type = 'multipart/form-data'
    field_required = (
        'id',
    )

    def post(self, request, user, data, *args, **kwargs):
        try:
            r = {
                'id': data['id'],
                'answer': data['answer'],
                'sent': data['sent']

            }
            r['file'] = None
            if 'file' in request.FILES:
                r['file'] = request.FILES.get('file')

            response = Response.objects.filter(
                Q(id=data['id'] & Q(student=user))
            ).update(**data)
        
        except Response.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        response = {
            **ALL_OK,
            'response': {
                'status': 'updated',
                **data,
                'file': None if r['file'] is None else r['file'].name
            }
        }

        return JsonResponse(response)

class GradeResponse(MainClass):
    login_required = True
    data_required = True
    fields_required = (
        'id',
        'grade'
    )

    def post(self, request, user, data, *args, **kwargs):
        try:

            r = Response.objects.get(
                Q(id=data['id'])
            )
            r.grade = int(data['grade'])
            r.save()

            print(r)
        
        except Response.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        response ={
            **ALL_OK,
            'response': {
                'status': 'updated',
                **data
            }
        }

        print(response)

        return JsonResponse(response)

class GetResponse(MainClass):
    login_required = True

    def get(self, request, user, response, *args, **kwargs):
        try:
            r = Response.objects.get(
                Q(id=response) &
                Q(
                    Q(homework_course_professor=user) |
                    Q(homework_course_students_in=[user])
                )
            )
        except Response.DoesNotExist:
            return JsonResponse(NOT_FOUND,status=404)
        
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        response = {
            **ALL_OK,
            'response': {
                'id': r.id,
                'answer': r.answer,
                'file': r.file.url if r.file else None,
                'sent': r.sent,
                'grade': r.grade,
                'graded': True if r.grade is not None else False
            }
        }

        return JsonResponse(response)
