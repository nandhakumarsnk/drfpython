from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework.generics import *
from hrms.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.views import APIView
from django.views import View
from django.contrib.auth.models import Group


@method_decorator(csrf_exempt, name="dispatch")
class test_api(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'HELLO'})
    
            
@method_decorator(csrf_exempt, name="dispatch")
class user_login(View):

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(f"user ---- {user}")

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Admin').exists():
                return JsonResponse({'emp_id':user.id,'username':user.username,'role':'Admin', 'message': 'Login successful'}, status=status.HTTP_200_OK)
            elif user.groups.filter(name='HR').exists():
                return JsonResponse({'emp_id':user.id,'username':user.username,'role':'HR', 'message': 'Login successful'}, status=status.HTTP_200_OK)
            elif user.groups.filter(name='Manager').exists():
                return JsonResponse({'emp_id':user.id,'username':user.username,'role':'Manager', 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'emp_id':user.id,'username':user.username,'role':'Employee','message': 'Login successful'}, status=status.HTTP_200_OK)
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=200)

        
@method_decorator(csrf_exempt, name="dispatch")
class user_logout(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
# =============================

@method_decorator(csrf_exempt, name="dispatch")
class subscription_list(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = subscriptionserializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@method_decorator(csrf_exempt, name="dispatch")
class category_list(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = categoryserializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class category_fooditems(APIView):
    def get(self, request, category_id):
        try:
            queryset = Items.objects.filter(category_id=category_id)
            
            serializer = items_serializer(queryset, many=True)  

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Items.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)


