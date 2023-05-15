import re, uuid, datetime
import string
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.contrib.auth.hashers import make_password
from mainapp.models import *
from mainapp.hasher import hash_fun


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


    def validate(self, data):
        errors = []

        """Проверка имени"""
        first_name = data["first_name"]
        if not first_name.isalpha():
            errors.append({"first_name": ["Incorrect field value."]})
        
        """Проверка фамилии"""
        last_name = data["last_name"]
        if not last_name.isalpha():
            errors.append({"last_name": ["Incorrect field value."]})
        
        """Проверка email"""
        user_email = User.objects.filter(email=data["email"])
        if user_email.exists():
            errors.append({"email": ["Already exists."]})
        
        """Проверка телефона"""
        phone = data["phone"]
        rule = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
        if not rule.search(phone):
            errors.append({"phone": ["Incorrect field value."]})
        
        """Сложность пароля"""
        password = data["password"]

        upper_case = any([1 if i in string.ascii_uppercase else 0 for i in password])
        lower_case = any([1 if i in string.ascii_lowercase else 0 for i in password])
        digits = any([1 if i in string.digits else 0 for i in password])

        rule_password = upper_case and lower_case and digits and len(password) > 6
        if not rule_password:
            errors.append({"password": ["Too easy password"]})
        
        if errors:
            raise ValidationError(errors)

        return data
    

    def create(self, validated_data):
        """Вариант хэширование через встроенный django"""
        # validated_data['password'] = make_password(validated_data['password'])

        """Своя функция хэширования"""
        validated_data['password'] = hash_fun(validated_data['password'])
        
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class UserAllViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        errors = []

        """Сложность пароля"""
        password = data["password"]

        upper_case = any([1 if i in string.ascii_uppercase else 0 for i in password])
        lower_case = any([1 if i in string.ascii_lowercase else 0 for i in password])
        digits = any([1 if i in string.digits else 0 for i in password])

        rule_password = upper_case and lower_case and digits and len(password) > 6
        if not rule_password:
            errors.append({"password": ["Incorrect password"]})

        if errors:
            raise ValidationError(errors)
        
        return data
        

class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserForgotPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_repeat = serializers.CharField()

    def validate(self, data):
        errors = []

        """Сложность пароля"""
        password = data["password"]

        upper_case = any([1 if i in string.ascii_uppercase else 0 for i in password])
        lower_case = any([1 if i in string.ascii_lowercase else 0 for i in password])
        digits = any([1 if i in string.digits else 0 for i in password])

        rule_password = upper_case and lower_case and digits and len(password) > 6
        if not rule_password:
            errors.append({"password": ["Incorrect password"]})

        if errors:
            raise ValidationError(errors)
        
        return data
    

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


    def validate(self, data):
        errors = []

        """Проверка имени"""
        first_name = data["first_name"]
        if not first_name.isalpha():
            errors.append({"first_name": ["Incorrect field value."]})
        
        """Проверка фамилии"""
        last_name = data["last_name"]
        if not last_name.isalpha():
            errors.append({"last_name": ["Incorrect field value."]})
        
        """Проверка email"""
        user_email = User.objects.filter(email=data["email"])
        if user_email.exists():
            errors.append({"email": ["Already exists."]})
        
        """Проверка телефона"""
        phone = data["phone"]
        rule = re.compile(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")
        if not rule.search(phone):
            errors.append({"phone": ["Incorrect field value."]})
        
        if errors:
            raise ValidationError(errors)
        return data
    
    def create(self, validated_data):
        # validated_data["token_complite_signup"] = uuid.uuid4()
        # validated_data["token_complite_signup_created_at"] = datetime.datetime.now()
        return User.objects.create(**validated_data)


class UserCompliteSignUpSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_repeat = serializers.CharField()

    def validate(self, data):
        errors = []

        """Сложность пароля"""
        password = data["password"]

        upper_case = any([1 if i in string.ascii_uppercase else 0 for i in password])
        lower_case = any([1 if i in string.ascii_lowercase else 0 for i in password])
        digits = any([1 if i in string.digits else 0 for i in password])

        rule_password = upper_case and lower_case and digits and len(password) > 6
        if not rule_password:
            errors.append({"password": ["Incorrect password"]})

        if errors:
            raise ValidationError(errors)
        
        return data


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


    def create(self, validated_data):
        return Task.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.workers = validated_data.get("workers", instance.workers)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance