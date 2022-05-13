from django.http import JsonResponse
from django.db.models import Q
from cursos.models import Course, Post
from tareas.models import Homework
from lib.extras import MainClass
from lib.responses import *

from authentication.models import User

from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


class NewCourse(MainClass):
    login_required = True
    data_required = True
    fields_required = (
        'name',
        'description',
    )

    def post(self, request, user, data, *args, **kwargs):
        print(user)
        if user.type == 3:
            return JsonResponse(FORBIDDEN, status=403)

        try:
            course = Course.objects.create(**data)
            course.professor.add(user)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        response = {
            'course': {
                'id': course.id,
                **data
            },
            **ALL_OK
        }

        return JsonResponse(response)


class GetAllAvailableCourses(MainClass):

    login_required = True

    def get(self, request, *args, **kwargs):
        try:
            courses = Course.objects.filter(activate=True)

        except Course.DoesNotExist:
            return JsonResponse(NO_ACTIVE_COURSES)

        try:

            response = [
                {
                    'id': course.id,
                    'name': course.name,
                    'professor': {
                        'name': course.professor.all()[0].get_full_name()
                    },
                    'password': True if course.password is not None else False,
                    'password_str': course.password
                }
                for course in courses
            ]
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        return JsonResponse({'courses': response})


class GetUserCourses(MainClass):
    login_required = True

    def get(self, request, user, *args, **kwargs):
        response = {
            'professor': [],
            'student': [],
            **ALL_OK
        }

        try:

            professor = user.course_professor.all()
            student = user.student_courses.all()

            for course in professor:
                if course.end >= datetime.now().date():
                    response['professor'].append(
                        {
                            'id': course.id,
                            'name': course.name,
                            'professor': {
                                'name': user.get_full_name()
                            },
                            'start': course.start,
                            'end': course.end,
                            'active': course.active,
                            'password': True if course.password is not None else False,
                            'password_str': course.password,
                            'homework': [
                                {
                                    'title': h.title,
                                    'limit': h.limit
                                }
                                for h in course.homework.all() if h.limit > utc.localize(datetime.now() - timedelta(days=1))
                            ]
                        }
                    )

            for course in student:
                if course.end >= datetime.now().date():
                    response['student'].append(
                        {
                            'id': course.id,
                            'name': course.name,
                            'professor': {
                                'name': course.professor.all()[0].get_full_name()
                            },
                            'start': course.start,
                            'end': course.end,
                            'active': course.active,
                            'password': True if course.password is not None else False,
                            'password_str': course.password,
                            'homework': [
                                {
                                    'title': h.title,
                                    'limit': h.limit
                                }
                                for h in course.homework.all() if h.limit > utc.localize(datetime.now() - timedelta(days=1))
                            ]
                        }
                    )
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        return JsonResponse(response)


class GetCourseDetails(MainClass):
    login_required = True

    def get(self, request, user, course, *args, **kwargs):
        try:
            course = Course.objects.get(id=course)

            response = {
                **ALL_OK,
                'id': course.id,
                'name': course.name,
                'professor': {
                    'name': course.professor.all()[0].get_full_name()
                },
                'description': course.description,
                'posts': [
                    {
                        'id': posts.id,
                        'title': posts.title,
                        'description': posts.content,
                        'dateCreated': posts.timestamp
                    }
                    for posts in course.post.all()
                ],
                'owner': True if user == course.professor.all()[0] else False,
                'has_password': True if course.password is not None else False,
                'password': course.password,
                'enrolled': True if user in course.students.all() else False
            }
        except Course.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        except IndexError:
            return JsonResponse(DEV_ERROR, status=500)

        return JsonResponse(response)


class UpdateCourse(MainClass):
    login_required = True
    data_required = True
    fields_required = (
        'id',
    )

    def post(self, request, user, data, *args, **kwargs):
        try:
            if user.profile_type == 3:
                return JsonResponse(FORBIDDEN, status=403)

            try:
                course = Course.objects.filter(
                    Q(id=data['id']) & Q(professor=user)
                ).update(**data)
            except Exception as e:
                print(e)
                return JsonResponse(BAD_REQUEST, status=400)

            response = {
                **ALL_OK,
                'course': {
                    'status': 'updated',
                    **data
                }
            }

            return JsonResponse(response)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)


class DeleteCourse(MainClass):
    login_required = True

    def get(self, request, user, course, *args, **kwargs):
        try:
            Course.objects.filter(
                Q(id=course) & Q(professor=user)
            ).delete()
        except Course.DoesNotExist:
            return JsonResponse(NOT_FOUND, status=404)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)

        return JsonResponse(ALL_OK)


class StudentEnroll(MainClass):
    login_required = True
    data_required = True
    fields_required = (
        'course',
        'password'
    )

    def post(self, request, user, data, *args, **kwargs):
        try:
            if user.profile_type == 2:
                return JsonResponse(FORBIDDEN, status=403)

            try:
                course = Course.objects.get(id=data['course'])
                if len(course.students.filter(email=user.email)) > 0:
                    return JsonResponse(USER_ALREADY_ENROLLED)

                if course.password == None or course.password == data['password']:
                    course.students.add(user)
                else:
                    return JsonResponse(INVALID_PASSWORD, status=403)
            except Course.DoesNotExist:
                return JsonResponse(NOT_FOUND, status=404)
            except Exception as e:
                print(e)
                return JsonResponse(BAD_REQUEST, status=400)

            response = {
                **ALL_OK,
                'course': {
                    'status': 'enrolled',
                    'name': course.name,
                    'start': course.start,
                    'end': course.end
                }
            }

            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)


class NewPost(MainClass):
    login_required = True
    data_required = True
    fields_required = (
        'course',
        'title',
        'content'
    )

    def post(self, request,  user, data, *args, **kwargs):
        try:
            print(request)
            if user.type == 3:
                return JsonResponse(FORBIDDEN, status=403)

            course = Course.objects.get(
                Q(id=data['course']) & Q(professor=user)
            )
            homework = Homework.objects.create(
                title=data['title'],
                description=data['content'],
                limit=datetime.now() + timedelta(days=365),
            )
            post = Post.objects.create(
                homework=homework,
                title=data['title'],
                content=data['content'],
            )

            course.post.add(post)
            course.save()

            response = {
                **ALL_OK,
                'post': {
                    'status': 'created',
                    **data
                }
            }

            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)


class GetPost(MainClass):
    login_required = True

    def get(self, request, user, post, *args, **kwargs):
        try:
            post = Post.objects.get(id=post)

            print(type(post.title))

           
            try:
                r = post.homework.response.filter(student__id=user.id)[0]
                print(r)
                re = {
                    'id': r.id,
                    'graded': True if r.grade is not None else False,
                    'grade': r.grade,
                    'student': {
                        'name': r.student.get_full_name()
                    },
                    'answer': r.answer
                }
            except Exception as e:
                re = {}
                print(e)

            response = {
                **ALL_OK,
                'title': post.homework.title,
                'description': post.homework.description,
                'dateCreated': post.timestamp,
                'id': post.homework.id,
                'response': {
                    **re
                }
            }

            print(response)

            return JsonResponse(response)
        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)


class GetPosts(MainClass):
    login_required = True

    def get(self, request, user, course, *args, **kwargs):
        try:
            course = Course.objects.get(id=course)

            response = {
                **ALL_OK,
                'posts': []
            }

            for post in course.posts.all():
                print("HERE")
                if post.ptype == 0:
                    print(post.title)
                    response['posts'].append(
                        {
                            'id': post.id,
                            'title': post.title,
                            'content': post.content,
                            'timestamp': post.timestamp,
                            'type': post.ptype
                        }
                    )
                else:
                    print(post.title)
                    response['posts'].append(
                        {
                            'id': post.id,
                            'title': str(post.homework.title),
                            'content': post.homework.description,
                            'timestamp': post.homework.limit,
                            'type': post.ptype
                        }
                    )
            return JsonResponse(response)

        except Exception as e:
            return JsonResponse(BAD_REQUEST, status=400)


class UpdatePost(MainClass):
    login_required = True
    data_required = True
    body = 'request'
    fields_required = (
        'post',
    )

    def post(self, request,  user, data, *args, **kwargs):
        try:
            if user.profile_type == 3:
                return JsonResponse(FORBIDDEN, status=403)

            file = None

            if 'file' in request.FILES:
                file = request.FILES.get('file')
            post = Post.objects.get(id=data['post'])

            if post.ptype == 0:
                print('0')
                if 'title' in data:
                    post.title = data['title']
                if 'content' in data:
                    post.content = data['content']
                if 'file' in data:
                    post.file = file

                post.save()
            else:
                print(1)

                homework = Homework.objects.get(id=post.homework.id)
                if 'title' in data:
                    homework.title = data['title']
                if 'content' in data:
                    homework.description = data['content']
                if 'file' in data:
                    homework.file = data['file']

                print(type(data['title']))

                homework.save()

            response = {
                **ALL_OK,
                'post': {
                    'status': 'updated',
                    **data
                }
            }

            return JsonResponse(response)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)


class DeletePost(MainClass):
    login_required = True

    def get(self, request, user,  post, *args, **kwargs):
        try:
            if user.profile_type == 3:
                return JsonResponse(FORBIDDEN, status=403)

            try:
                delpost = Post.objects.get(
                    Q(id=post) & Q(course__professor=user)
                )
            except Exception as e:
                print(e)
                return JsonResponse(DATA_NOT_FOUND)

            delpost.delete()

            return JsonResponse(DATA_DELETED)

        except Exception as e:
            print(e)
            return JsonResponse(BAD_REQUEST, status=400)
