import datetime, uuid
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from mainapp.serializers import *
from mainapp.models import *
from mainapp.hasher import hash_fun
from mainapp.mailsender import *
# from mainapp.permissions import IsAdminUser


def is_valid_uuid(uuid_to_valid, version=4):
    try:
        uuid_obj = uuid.UUID(uuid_to_valid, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_valid


class UserCompliteSignUpView(APIView):
    def post(self, request, **kwargs):
        serializer = UserCompliteSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        password = hash_fun(serializer.data["password"])
        password_repeat = hash_fun(serializer.data["password_repeat"])

        token = kwargs.get("token_complite_signup", None)

        if not is_valid_uuid(token):
            return Response({"error": "Invalid token"}, status=400)
        
        if not token:
            return Response({"error": "Token not found"}, status=400)
        
        try:
            token_complite = TokensCompliteSignUp.objects.get(token_complite_signup=token)
        except TokensCompliteSignUp.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)
        
        user = token_complite.user

        if user.is_verify == True:
            return Response({"error": "User is already verify"}, status=400)
        
        date1 = datetime.datetime.now()
        date2 = token_complite.token_complite_signup_created_at
        date1_utc = date1.astimezone(datetime.timezone.utc)
        date2_utc = date2.astimezone(datetime.timezone.utc)
        diff = date1_utc - date2_utc
        print(diff)
        
        if not password == password_repeat:
            return Response({"error": "Passwords don't match"}, status=400)
        
        user.password = password
        user.is_verify = True
        token_complite.delete()
        user.save()
        user.refresh_from_db()
        
        return Response(status=200)
    

class UserForgotPasswordView(APIView):
    def post(self, request, **kwargs):
        serializer = UserForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = hash_fun(serializer.data["password"])
        password_repeat = hash_fun(serializer.data["password_repeat"])

        token = kwargs.get("token_reset", None)

        # if not is_valid_uuid(token):
        #     return Response({"error": "Invalid token"}, status=400)
        
        if not token:
            return Response({"error": "Token not found"}, status=400)
        
        try:
            token_reset = TokensReset.objects.get(token_reset=token)
        except TokensReset.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)
        
        user = token_reset.user
        date1 = datetime.datetime.now()
        date2 = token_reset.token_reset_created_at
        date1_utc = date1.astimezone(datetime.timezone.utc)
        date2_utc = date2.astimezone(datetime.timezone.utc)
        diff = date1_utc - date2_utc
        print(diff)
        
        if not password == password_repeat:
            return Response({"error": "Passwords don't match"}, status=400)
        
        user.password = password
        user.save()
        token_reset.delete()
        user.refresh_from_db()
        
        return Response(status=200)
    

class UserResetPasswordView(APIView):
    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]

        if not email:
            return Response({"error": "Invalid email"}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except:
            return Response({"error": "User not found"}, status=400)
        
        TokensReset.objects.create(user=user)
        token_reset = TokensReset.objects.get(user=user)
        
        url = f"http://127.0.0.1:8000/api/v1/user/{token_reset.token_reset}/forgotpassword/"

        send_to_reset_password(to_send=email, url=url)

        return Response({"done": url}, status=200)
    

class UsersApiView(APIView):
    # permission_classes = [IsAdminUser,]

    def get(self, request):
        users = User.objects.all()
        return Response(UserAllViewSerializer(users, many=True).data, status=200)
    
    """Для complite signup когда создает юзер"""
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data['id']
        user = User.objects.get(pk=user_id)
        TokensCompliteSignUp.objects.create(user=user)
        token_complite = TokensCompliteSignUp.objects.get(user=user_id)
        
        url = f'http://127.0.0.1:8000/api/v1/users/{token_complite.token_complite_signup}/complitesingup/'
        print(url)

        send_to_complite_signup(to_send=serializer.data['email'], url=url)

        return Response({"ok": url}, status=200)


class UserAuthView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        password = serializer.data["password"]

        if not email:
            return Response({"Error": "Error email"}, status=400)
        if not password:
            return Response({"Error": "Error password"}, status=400)
        
        hash_password = hash_fun(password)

        try:
            user = User.objects.get(email=email, password=hash_password)
        except:
            return Response({"error": "User not found"}, status=400)
        
        if not user.is_verify == True:
            return Response({"Error": "User is not verify"}, status=400)
        
        if not user.is_enable == True:
            return Response({"Error": "User is not enable"}, status=400)
        
        token = uuid.uuid4()
        # session = Sessions.objects.create(user_id=user, token=token)

        # return Response({"session": session.token}, status=200)
        return Response(status=200)


class UserVerifyEmailView(APIView):
    def get(self, request, **kwargs):
        token_verify = kwargs.get("token_verify", None)

        if not is_valid_uuid(token_verify):
            return Response({"error": "Invalid token"}, status=400)
        
        if not token_verify:
            return Response({"error": "Token not found"}, status=400)

        try:
            token_verify = TokensVerify.objects.get(token_verify=token_verify)
        except TokensVerify.DoesNotExist:
            return Response({"error": "Token not found"}, status=400)

        # if user.is_verify == True:
        #     return Response({"error": "User is already verify"}, status=400)
        
        # date1 = datetime.datetime.now()
        # date2 = user.token_verify_created_at
        # date1_utc = date1.astimezone(datetime.timezone.utc)
        # date2_utc = date2.astimezone(datetime.timezone.utc)
        # diff = date1_utc - date2_utc
        # print(diff)
        # time_obj = datetime.datetime.strptime(str(diff), '%H:%M:%S.%f').time()
        # hours = time_obj.strftime('%H')

        # if int(hours) > 2:
        #     return Response({"error": "time's up"}, status=400)
        user = token_verify.user
        user.is_enable=True
        user.is_verify=True
        user.save()
        token_verify.delete()
        user.refresh_from_db()
        return Response(status=200)


class UserSignUpView(APIView):
    def post(self, request):    
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_id = serializer.data['id']
        user = User.objects.get(pk=user_id)
        TokensVerify.objects.create(user=user)
        token_verify = TokensVerify.objects.get(user=user_id)
        
        to_send = serializer.data['email']
        url = f'http://127.0.0.1:8000/api/v1/user/{token_verify.token_verify}/verify/'
        print(url)
        send_for_verify(to_send=to_send, url=url)

        return Response(status=status.HTTP_201_CREATED)


class UserPostView(APIView):
    # permission_classes = [IsAdminUser,]
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        
        try:
            instance = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})
        
        serializer = UserSerializers(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"put": serializer.data})
    
    def get(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "User not found"})
        
        try:
            user_id = User.objects.get(pk=pk)
        except:
            return Response({"error": "User not found"}, status=404)
        
        return Response(UserSerializers(user_id).data)
    
    def delete(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "This ID does not exist"})
        
        try:
            user_id = User.objects.get(pk=pk)
        except:
            return Response({"error": "Fail"})
        
        user_id.delete()
        return Response({"done": "User deleted"})


class TaskCreateView(APIView):
    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)
    
    
class TaskGPDView(APIView):
    def delete(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "This ID does not exist"}, status=400)
        
        try:
            task_id = Task.objects.get(pk=pk)
        except:
            return Response({"error": "Task not found"}, status=400)
        
        task_id.delete()
        return Response({"done": "User deleted"}, status=200)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"}, status=405)
        
        try:
            instance = Task.objects.get(pk=pk)
        except:
            return Response({"error": "Task does not exist"}, status=400)
        
        serializer = TaskCreateSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"put": serializer.data}, status=200)
    
    def get(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "This ID does not exist"}, status=400)
        
        try:
            task_id = Task.objects.get(pk=pk)
        except:
            return Response({"error": "User not found"}, status=404)
        
        return Response(UserSerializers(task_id).data)




