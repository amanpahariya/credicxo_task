from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework import generics,viewsets,status
from .serialziers import *
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings





class RegisterTeacherViewSet(viewsets.ModelViewSet):
    '''
    here only admin can register the teacher
    and in get request admin can see all the users
    '''
    permission_classes = [IsAdminUser]
    serializer_class = CustomTeacherSerializer

    def get_queryset(self):
        return User.objects.all()

class RegisterStudentViewSet(viewsets.ModelViewSet):

    '''
    here admin and teacher can add the student 
    and student is restricted on this api
    '''

    '''
    hear admin can see all the users and 
    teacher can see only the students 
    '''
    serializer_class = CustomStudentSerializer

    def get_queryset(self):
        if User.objects.filter(email=self.request.user).values_list('is_superuser')[0][0]:
            return User.objects.all()
        elif User.objects.filter(email=self.request.user).values_list('is_teacher')[0][0]:
            return User.objects.filter(is_student=True).all()

    '''
    by default only admin have permision but if user is teacher then they also have permssion by the function get_permission and 
    student is restricted from this api
    '''
    def get_permissions(self):
        self.permission_classes = [IsAdminUser]
        try:
            if (User.objects.filter(email=self.request.user).values_list('is_teacher')[0][0] or User.objects.filter(email=self.request.user).values_list('is_superuser')[0][0]):
                self.permission_classes = [IsAuthenticated]
        except:
            pass
        return super(self.__class__, self).get_permissions()

class UserDetailsViewSet(viewsets.ModelViewSet):

    '''
    here only user can see his data and user have ready only permission
    '''
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return User.objects.filter(email=self.request.user).all()

    serializer_class=UserSerializer


class ForgotPasswordViewSet(APIView):

    '''
    this api is create for creating forgot password url
    '''
    permission_classes=[AllowAny]

    def post(self,request,format='json'):
        try:
            user = User.objects.get(email=request.user)
            if user:
                user_data = User.objects.get(email=request.user)
                # assigning access token to user
                token = RefreshToken.for_user(user_data).access_token
                # forgot password url
                current_site = 'http://'+str(get_current_site(request))+'/api/resetpassword/?token='+str(token)
                data={
                    'forgotpasswordlink':str(current_site)
                }

                return Response(data, status=status.HTTP_201_CREATED)      
        except:
            # if email is not registered 
            data={
                'response':'this email is not registered'
            }
            return Response(data,status=status.HTTP_404_NOT_FOUND)


class ResetPasswordViewSet(APIView):
    permission_classes=[AllowAny]

    def post(self,request,format='json'):
        token=request.GET.get('token')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm password')
        # matching password and checking is  password is not none
        if (pass1 == pass2) and pass1 is not None :
            try:
                # decoing password
                payload = jwt.decode(token,settings.SECRET_KEY,verify=True,algorithms='HS256')
                user = User.objects.get(id=payload['user_id'])
                # set user password
                user.set_password(pass1)
                user.save()  
                data={
                        'response':'password changes successfully'
                }
                return Response(data, status=status.HTTP_201_CREATED) 
            except jwt.ExpiredSignatureError as identifier:
                # if token is expired
                return Response({'error':'link is expired'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.DecodeError as identifier:
                # if token is invalid
                return Response({'error':'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if password did not match
            return Response({'error':'password and confirm password did not match'},status=status.HTTP_406_NOT_ACCEPTABLE)

            