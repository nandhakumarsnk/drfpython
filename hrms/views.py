from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import *
from rest_framework.generics import *
from hrms.models import *
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
import json
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from django.views import View
from django.contrib.auth.models import Group
from datetime import datetime, timedelta


@method_decorator(csrf_exempt, name="dispatch")
class test_api(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'HELLO'})
    
            
@method_decorator(csrf_exempt, name="dispatch")
class user_login(View):

    def post(self, request, *args, **kwargs):

        # username = request.POST.get('username')
        # password = request.POST.get('password')
        data = json.loads(request.body)  # Parse the JSON data from the request body
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

# ======================================= CUSTOMUSER_API =================================

@method_decorator(csrf_exempt, name="dispatch")
class user_register(CreateAPIView):
    # queryset = CustomUser.objects.all()
    serializer_class = customuserserializer

    def create(self, request, *args, **kwargs):
        request.data['password']=make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            user_role = request.data.get('user_role')
            if user_role is None:
                return Response({'error': 'user_role is required', 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
            
            userRegister = self.create(request, *args, **kwargs)
            # a=userRegister.__dict__
            # print(f"dataaaa {a['data']['id']} {type(a)}")

            user_id = userRegister.data['id']

            # user_role = request.data.get('user_role') 

            if user_role == '1':
                admin_group = Group.objects.get(name='Admin')
                admin_group.user_set.add(user_id)
            elif user_role == '2':
                hr_group = Group.objects.get(name='HR')
                hr_group.user_set.add(user_id)
            elif user_role == '3':
                emp_group = Group.objects.get(name='Employee')
                emp_group.user_set.add(user_id)
            elif user_role == '4':
                manager_group = Group.objects.get(name='Manager')
                manager_group.user_set.add(user_id)

            return Response({'emp_id':user_id, 'status': 'Registration successful'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            if str(e):
                if 'username' in str(e):
                    return Response({'error': 'User already exists', 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'email' in str(e):
                    return Response({'error': 'Email already exists', 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'error':str(e),'error1': 'An error occurred', 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

  

@method_decorator(csrf_exempt, name="dispatch")
class user_list(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class user_retrieve(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer


@method_decorator(csrf_exempt, name="dispatch")
class emp_leavebalancelist_forHR(ListAPIView):
    serializer_class = customuserserializer

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)  # Get the original response
        
        custom_data = []  
        for item in response.data:
            custom_data.append({
                'emp_id': item['id'],
                'username': item['username'],
                'casual_leave_balance': item['leave_balance1'],
                'sick_leave_balance': item['leave_balance2'],
            })

        response.data = custom_data  # Modify the response data
        return response


    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class emp_leavebalance_retrieve(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)  # Get the original response
        
        custom_data = {
            'emp_id': response.data['id'],
            'username': response.data['username'],
            'casual_leave_balance': response.data['leave_balance1'],
            'sick_leave_balance': response.data['leave_balance2'],
        }

        response.data = custom_data 
        return response


# class emp_leavebalance_retrieve(APIView):            WORKING CODE

#     def post(self, request, *args, **kwargs):
#         emp_id = request.data.get('emp_id')

#         if emp_id is None:
#             return Response({'error': 'emp_id is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.get(id=emp_id)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = customuserserializer(user)
#         custom_data = {
#             'emp_id': serializer.data['id'],
#             'username': serializer.data['username'],
#             'casual_leave_balance': serializer.data['leave_balance1'],
#             'sick_leave_balance': serializer.data['leave_balance2'],
#         }

#         return Response(custom_data)

# ======================================================================================

@method_decorator(csrf_exempt, name="dispatch")
class user_update(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer
    #by default will lookup the pk refer https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview

    def partial_update(self, request, *args, **kwargs):
        if 'password' in request.data:
            request.data['password']=make_password(request.data['password'])
        return super().partial_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("hiiiii")
        return self.partial_update(request, *args, **kwargs)
    
@method_decorator(csrf_exempt, name="dispatch")
class user_delete(DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    

# ====================================== LEAVETYPES =========================================

@method_decorator(csrf_exempt, name="dispatch")
class leavetype_list(ListAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = leavetypeserializer

    def get_leavetypelist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
@method_decorator(csrf_exempt, name="dispatch")
class leavetype_update(UpdateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = leavetypeserializer

    def put_leavetypeUpdate(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
# ====================================== LEAVE_APPLICATION =========================================

class leave_application(CreateAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = leave_applicationserializer

    def validate_leave_balance(self, user, leave_typename_id, no_of_days):
        print(leave_typename_id)
        print(user.leave_balance1) 
        print(no_of_days)
        if leave_typename_id == 1:
            if user.leave_balance1 < no_of_days:
                raise serializers.ValidationError({'status':"Leave balance is less for Casual Leave"})
        elif leave_typename_id == 2: 
            if user.leave_balance2 < no_of_days:
                raise serializers.ValidationError({'status':"Leave balance is less for Sick Leave"})
            
    def calculate_no_of_days(self, start_date, end_date):
        no_of_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() != 6:  # 6 corresponds to Sunday (0 is Monday, 1 is Tuesday, and so on)
                no_of_days += 1
            current_date += timedelta(days=1)
        return no_of_days

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d').date()
        # no_of_days = (end_date - start_date).days + 1
        no_of_days = self.calculate_no_of_days(start_date, end_date)  # Calculate no_of_days excluding Sundays

        emp_leave_data = {
            'emp_id': request.data['emp_id'], 
            'start_date': start_date,
            'end_date': end_date,
            'application_date': request.data['application_date'],
            'leave_typename': request.data['leave_typename'],  
            'no_of_days': no_of_days
        }
        
        emp_leave_serializer = applyemp_leaveserializer(data=emp_leave_data)
        emp_leave_serializer.is_valid(raise_exception=True)
        emp_leave_data = emp_leave_serializer.validated_data
        user = emp_leave_data['emp_id']
        leave_typename_id = emp_leave_data['leave_typename'].leave_id

        self.validate_leave_balance(user, leave_typename_id, no_of_days)

        emp_leave_serializer.save()
        leave_application_instance = serializer.save()

        return Response({'application_id':leave_application_instance.id,'emp_id':user.id, 'status': 'Leave application successful'})
        

    def post_applyleave(self, request, *args, **kwargs):
        try:
            self.create(request, *args, **kwargs)
            return Response({'status': 'Leave Apply successful'}, status=status.HTTP_201_CREATED)
        except:
            return Response({ 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST)

    #    ================================================ 

@method_decorator(csrf_exempt, name="dispatch")
class leave_application_list(ListAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = leave_applicationserializer

    def get_leave_applicationlist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class leave_application_retrieve(RetrieveAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = leave_applicationserializer

@method_decorator(csrf_exempt, name="dispatch")
class leave_application_update(UpdateAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = leave_applicationserializer

    def put_leaveUpdate(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
@method_decorator(csrf_exempt, name="dispatch")
class leave_application_delete(DestroyAPIView):
    queryset = Leave_Application.objects.all()
    serializer_class = leave_applicationserializer

    def delete_empDelete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 
    

# ====================================== EMP_LEAVES =========================================
from django.db.models import Q          

class emp_leave_retrieve(APIView):
    def post(self, request, *args, **kwargs):
        serializer = emp_leaveserializer(data=request.data)
        if serializer.is_valid():
            startdate = serializer.validated_data.get('start_date')
            enddate = serializer.validated_data.get('end_date')
            leavetypename = serializer.validated_data.get('leave_typename')
            status = serializer.validated_data.get('status')
            empid = serializer.validated_data.get('emp_id').id
            print(empid)
            print(leavetypename)
            # print(leavetypename.leave_id)

            # queryset = Emp_leaves.objects.filter(
            #     start_date__gte=startdate,
            #     # end_date__lte=enddate,
            #     leave_typename=leavetypename,
            #     status=status,
            #     emp_id=empid
            # )

            filters = Q()

            if startdate is not None and startdate !="":
                filters &= Q(start_date__gte=startdate)
            if enddate is not None and enddate !="":
                filters &= Q(end_date__lte=enddate)
            if leavetypename is not None and leavetypename !="":
                filters &= Q(leave_typename=leavetypename)
            if status is not None and status !="":
                filters &= Q(status=status)
            if empid is not None and empid !="":
                filters &= Q(emp_id=empid)

            queryset = Emp_leaves.objects.filter(filters)

            custom_user = CustomUser.objects.get(id=empid)  
            leave_balance1 = custom_user.leave_balance1
            leave_balance2 = custom_user.leave_balance2
            print(leave_balance1,leave_balance2)

            serialized_data = emp_leaveserializer(queryset, many=True).data

            custom_response = []
            for item in serialized_data:
                # leave_typename = item['leave_typename']
                # leave_type = LeaveType.objects.filter(leave_typename=leave_typename).first()

                custom_item = {
                    'emp_id': item['emp_id'],
                    'application_date': item['application_date'],
                    'no_of_days': item['no_of_days'],
                    'start_date': item['start_date'],
                    'end_date': item['end_date'],
                    'leave_typename': item['leave_typename'],
                    # 'leave_typename': leave_type.leave_id,
                    'status': item['status'],
                    'hr_comments': item['hr_comments'],
                    'approved_date': item['approved_date'],
                }
              
                if leavetypename is not None and leavetypename !="":
                    if int(leavetypename) == 1:
                        custom_item['leave_balance'] = leave_balance1
                    elif int(leavetypename) == 2:
                        custom_item['leave_balance'] = leave_balance2

                    # if leavetypename.leave_id == 1:
                    #     custom_item['leave_balance'] = leave_balance1
                    # elif leavetypename.leave_id == 2:
                    #     custom_item['leave_balance'] = leave_balance2
                # if leavetypename == '1':
                #     custom_item['leave_balance'] = leave_balance1
                # elif leavetypename == '2':
                #     custom_item['leave_balance'] = leave_balance2

                custom_response.append(custom_item)

            return Response(custom_response)
        else:
            return Response(serializer.errors, status=400)
        
# ==================== LEAVE APPLICATION LISTS FOR HR =====================
#    (for Approval Pending List for Manager)
@method_decorator(csrf_exempt, name="dispatch")
class emp_leave_retrieve_forManager(ListAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        # queryset = Emp_leaves.objects.filter(mg_conformation='3')
        queryset = Emp_leaves.objects.filter(Q(mg_conformation='3') & Q(status='3'))
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        custom_data = []  
        for item in response.data:
            try:
                user = CustomUser.objects.get(id=item['emp_id'])
                username = user.username
            except CustomUser.DoesNotExist:
                username = None

            try:
                comments = Leave_Application.objects.get(id=item['id']).comments
            except Leave_Application.DoesNotExist:
                comments = None

            try:
                mg_comments = Emp_leaves.objects.get(id=item['id']).mg_comments
            except Leave_Application.DoesNotExist:
                comments = None

            custom_data.append({
                'emp_id': item['emp_id'],
                'leave_application_id': item['id'],
                'start_date': item['start_date'],
                'end_date': item['end_date'],
                'application_date': item['application_date'],
                'no_of_days': item['no_of_days'],
                'leave_typename': item['leave_typename'], 
                'username': username,
                'comments': comments,
                'mg_comments':mg_comments,
            })


        response.data = custom_data
        return response

    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#    (for Approval Pending List for HR)
@method_decorator(csrf_exempt, name="dispatch")
class emp_leave_retrieve_forHR(ListAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(status='3')
        return queryset
        
        # user = self.request.user
        # print(user)
        # if user.groups.filter(name="HR").exists():
        #     queryset = Emp_leaves.objects.filter(status='3')
        # else:
        #     queryset = Emp_leaves.objects.filter(mg_conformation='3')

        # return queryset
       

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        custom_data = []  
        for item in response.data:
            try:
                user = CustomUser.objects.get(id=item['emp_id'])
                username = user.username
            except CustomUser.DoesNotExist:
                username = None

            try:
                comments = Leave_Application.objects.get(id=item['id']).comments
            except Leave_Application.DoesNotExist:
                comments = None

            try:
                mg_comments = Emp_leaves.objects.get(id=item['id']).mg_comments
            except Leave_Application.DoesNotExist:
                comments = None

            custom_data.append({
                'emp_id': item['emp_id'],
                'leave_application_id': item['id'],
                'start_date': item['start_date'],
                'end_date': item['end_date'],
                'application_date': item['application_date'],
                'no_of_days': item['no_of_days'],
                'leave_typename': item['leave_typename'], 
                'username': username,
                'comments': comments,
                'mg_comments':mg_comments,
            })


        response.data = custom_data
        return response

    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
# --------
#    (for Approved List)
@method_decorator(csrf_exempt, name="dispatch")
class emp_leave_approvedlist_forHR(ListAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(status='5')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        custom_data = []  
        for item in response.data:
            try:
                user = CustomUser.objects.get(id=item['emp_id'])
                username = user.username
            except CustomUser.DoesNotExist:
                username = None

            try:
                comments = Leave_Application.objects.get(id=item['id']).comments
            except Leave_Application.DoesNotExist:
                comments = None

            custom_data.append({
                'emp_id': item['emp_id'],
                'leave_application_id': item['id'],
                'start_date': item['start_date'],
                'application_date': item['application_date'],
                'end_date': item['end_date'],
                'no_of_days': item['no_of_days'],
                'leave_typename': item['leave_typename'], 
                'username': username,
                'comments': comments,
                'approved_date': item['approved_date'],
            })


        response.data = custom_data
        return response

    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
# --------
#    (for Rejected List)
@method_decorator(csrf_exempt, name="dispatch")
class emp_leave_rejectedlist_forHR(ListAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(status='1')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        custom_data = []  
        for item in response.data:
            try:
                user = CustomUser.objects.get(id=item['emp_id'])
                username = user.username
            except CustomUser.DoesNotExist:
                username = None

            try:
                comments = Leave_Application.objects.get(id=item['id']).comments
            except Leave_Application.DoesNotExist:
                comments = None

            custom_data.append({
                'emp_id': item['emp_id'],
                'leave_application_id': item['id'],
                'start_date': item['start_date'],
                'application_date': item['application_date'],
                'end_date': item['end_date'],
                'no_of_days': item['no_of_days'],
                'leave_typename': item['leave_typename'], 
                'username': username,
                'comments': comments,
            })


        response.data = custom_data
        return response

    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# ============================ leave approval ==========================
# ===== MANAGER  ======
class emp_leave_manager_conformation(RetrieveUpdateAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(id=self.kwargs['pk'])
        return queryset

    # (use patch method)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.mg_conformation == '3': 
                instance.mg_conformation = '5'
                instance.mg_comments = request.data.get('mg_comments')
                instance.save()

            serializer = self.get_serializer(instance)
            return JsonResponse({'leave_application_id': instance.id, 'leave_status': 'Manager Conformation Approved'}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ===== HR ======
class emp_leave_update(RetrieveUpdateAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(id=self.kwargs['pk'])
        return queryset

    # (use patch method)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.status == '3': 
                instance.status = '5'
                instance.hr_comments = request.data.get('hr_comments')
                instance.approved_date = request.data.get('approved_date')
                instance.save()

            user = instance.emp_id 
            print(instance.leave_typename)

            if instance.leave_typename_id == 1: 
                user.leave_balance1 -= instance.no_of_days
            elif instance.leave_typename_id == 2:  
                user.leave_balance2 -= instance.no_of_days
            else:
                print("nothing")

            user.save()
        

            serializer = self.get_serializer(instance)
            return JsonResponse({'leave_application_id': instance.id, 'leave_status': 'Approved'}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================ leave rejection ==========================
# ====== HR LEAVE REJECT =================
class emp_leave_reject(RetrieveUpdateAPIView):
    serializer_class = emp_leaveserializer

    def get_queryset(self):
        queryset = Emp_leaves.objects.filter(id=self.kwargs['pk'])
        return queryset

    # (use patch method)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.status == '3': 
                instance.status = '1'
                instance.hr_comments = request.data.get('hr_comments')
                instance.approved_date = request.data.get('approved_date')
                instance.save()

            serializer = self.get_serializer(instance)
            return JsonResponse({'leave_application_id': instance.id, 'leave_status': 'Rejected'}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ====================================================

@method_decorator(csrf_exempt, name="dispatch")
class emp_leave_delete(DestroyAPIView):
    queryset = Emp_leaves.objects.all()
    serializer_class = emp_leaveserializer

    def delete_emp_leaveDelete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs) 
    
# ====================================== LEAVE ENTITLEMENT =========================================
@method_decorator(csrf_exempt, name="dispatch")
class leave_entitlement_update(UpdateAPIView):
    queryset = Leave_Entitlement.objects.all()
    serializer_class = emp_leave_entitlementserializer

    def put_empUpdate(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
# FETCHING ALL THE ENTITLEMENTS (WORKING CODE)
@method_decorator(csrf_exempt, name="dispatch")  
class leave_entitlement_list(ListAPIView):
    queryset = Leave_Entitlement.objects.all()
    serializer_class = emp_leave_entitlementserializer

    def get_leave_entitlementslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

# FETCHING PARTICULAR ENTITLEMENTS (WORKING CODE)
# class leave_entitlement_list(APIView):
#     def post(self, request, *args, **kwargs):
#         leavetypename = request.data.get('leave_typename')  
#         print(leavetypename)

#         queryset = Leave_Entitlement.objects.filter(leave_typename=leavetypename)
#         serialized_data = emp_leave_entitlementserializer(queryset, many=True).data

#         return Response(serialized_data)

# =====================================================================================================

class leave_entitlement_add(UpdateAPIView):
        queryset = CustomUser.objects.all()
        serializer_class=customuserserializer
        
        def partial_update(self, request, *args, **kwargs):
            if request.data['ets']=='e1':
                
                a=Leave_Entitlement.objects.get(ent_id=1)
                self.get_object().entitlement.add(a)
                print(f"ent1111111 {request.data}")

            elif request.data['ets']=='e2':
               
                a=Leave_Entitlement.objects.get(ent_id=2)
                self.get_object().entitlement.add(a)
                print(f"ent2222222 {request.data}")

            else:
                pass
            
            return super().partial_update(request, *args, **kwargs)

        def patch(self, request, *args, **kwargs):
            l1 = self.partial_update(request, *args, **kwargs)
            a=l1.__dict__
            print(f"dataaaa {a['data']} {type(a)}")
            return l1


# =============================================================================================
#multipart/form-data
class employeeDocumentsUpload(CreateAPIView):
    queryset = Employee_documents.objects.all()
    serializer_class = Employee_documentSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'success': True, 'message': 'Document uploaded successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Update the emp documents
@method_decorator(csrf_exempt, name="dispatch")
class employeeDocumentsUpdate(UpdateAPIView):
    queryset = Employee_documents.objects.all()
    serializer_class = Employee_documentSerializer

    def put_employeeDocumentUpdate(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
# # retrieve the employee details with documents details also
# class UserProfileDetails(RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserWithDocumentsSerializer

# class UserProfileDetails(APIView):                                           WORKING CODE
#     def post(self, request, *args, **kwargs):
#         emp_id = request.data.get('emp_id')

#         if emp_id is None:
#                 return Response({'error': 'emp_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
#         try:
#             user = CustomUser.objects.get(id=emp_id)
#             serializer = CustomUserWithDocumentsSerializer(user)
#             return Response(serializer.data)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'CustomUser not found'}, status=status.HTTP_404_NOT_FOUND)    
        

# ====================== 08-09-2023 (LEAVE APPLICATION) ================== 
# from django.db.models import Count

# class leave_application(CreateAPIView):
#     queryset = Leave_Application.objects.all()
#     serializer_class = leave_applicationserializer

#     def validate_leave_balance(self, user, leave_typename_id, no_of_days):
#         print(leave_typename_id)
#         print(user.leave_balance1) 
#         print(no_of_days)
#         if leave_typename_id == 1:
#             if user.leave_balance1 < no_of_days:
#                 raise serializers.ValidationError({'status':"Leave balance is less for Casual Leave"})
#         elif leave_typename_id == 2: 
#             if user.leave_balance2 < no_of_days:
#                 raise serializers.ValidationError({'status':"Leave balance is less for Sick Leave"})
            
#     def calculate_no_of_days(self, start_date, end_date):
#         no_of_days = 0
#         current_date = start_date
#         while current_date <= end_date:
#             if current_date.weekday() != 6:  # 6 corresponds to Sunday (0 is Monday, 1 is Tuesday)
#                 no_of_days += 1
#             current_date += timedelta(days=1)
#         return no_of_days

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d').date()
#         end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d').date()
#         # no_of_days = (end_date - start_date).days + 1
#         no_of_days = self.calculate_no_of_days(start_date, end_date)  # Calculate no_of_days excluding Sundays

#         emp_leave_data = {
#             'emp_id': request.data['emp_id'], 
#             'start_date': start_date,
#             'end_date': end_date,
#             'application_date': request.data['application_date'],
#             'leave_typename': request.data['leave_typename'],  
#             'no_of_days': no_of_days
#         }
        
#         emp_leave_serializer = emp_leaveserializer(data=emp_leave_data)
#         emp_leave_serializer.is_valid(raise_exception=True)
#         emp_leave_data = emp_leave_serializer.validated_data
#         user = emp_leave_data['emp_id']
#         leave_typename_id = emp_leave_data['leave_typename'].leave_id

#         # ======
#         # Check if the user has already applied for the same leave type within the month
#         today = datetime.now()
#         print(today)
#         first_day_of_month = today.replace(day=1)
#         print(first_day_of_month)

#         leave_applications_this_month = Leave_Application.objects.filter(
#             emp_id=user,
#             leave_typename=leave_typename_id,
#             start_date__gte=first_day_of_month,
#             end_date__lte=today
#         ).aggregate(total_days=Count('leave_typename'))['total_days'] or 0
#         print(Count('leave_typename'))
#         print(leave_applications_this_month)

#         if leave_typename_id == 1:  # Casual Leave
#             if leave_applications_this_month + no_of_days > 2:
#                 return Response({'status': 'Cannot apply for more than 2 days of Casual Leave in a month'}, status=status.HTTP_400_BAD_REQUEST)
#         elif leave_typename_id == 2:  # Sick Leave
#             if leave_applications_this_month + no_of_days > 3:
#                 return Response({'status': 'Cannot apply for more than 3 days of Sick Leave in a month'}, status=status.HTTP_400_BAD_REQUEST)
#         # =======

#         self.validate_leave_balance(user, leave_typename_id, no_of_days)

#         # emp_leave_serializer.save()
#         # leave_application_instance = serializer.save()

#         # return Response({'application_id':leave_application_instance.id,'emp_id':user.id, 'status': 'Leave application successful'})
#         return Response({'emp_id':user.id, 'status': 'Leave application successful'})

#     def post_applyleave(self, request, *args, **kwargs):
#         try:
#             self.create(request, *args, **kwargs)
#             return Response({'status': 'Leave Apply successful'}, status=status.HTTP_201_CREATED)
#         except:
#             return Response({ 'status': 'Unsuccessful'}, status=status.HTTP_400_BAD_REQUEST) 

# ========================
        
class UserProfileDetails(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = customuserserializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)  
        
        custom_data = {
            'username': response.data['username'],
            'email': response.data['email'],
            'phone': response.data['phone'],
            'casual_leave_balance': response.data['leave_balance1'],
            'sick_leave_balance': response.data['leave_balance2'],
            'first_name': response.data['first_name'],
            'last_name': response.data['last_name'],
            'biits_id': response.data['biits_id'],
            'department': response.data['department'],
            'job_title': response.data['job_title'],
            'reporting_manager': response.data['reporting_manager'],
            'work_location':response.data['work_location'],
            'joining_date': response.data['joining_date'],
            'gender': response.data['gender'],
        }

        response.data = custom_data 
        return response
    
# ======================= (20/09/2023) ===================

#multipart/form-data
class Employee_Onboardingform_filling(CreateAPIView):
    queryset = Emp_Onboardingform.objects.all()
    serializer_class = Employee_OnboardingformSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'success': True, 'message': 'Employee Onboarding form submitted successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# class Employee_formDetails(APIView):                WORKING CODE
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         phone = request.data.get('phone')

#         if email is None:
#                 return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
#         if phone is None:
#                 return Response({'error': 'phone is required'}, status=status.HTTP_400_BAD_REQUEST)
            
#         try:
#             user = Emp_Onboardingform.objects.get(Q(email=email) & Q(phone=phone))
#             serializer = Employee_OnboardingformSerializer(user)
#             return Response(serializer.data)
#         except Emp_Onboardingform.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        
@method_decorator(csrf_exempt, name="dispatch")
class empOnboarding_pending(ListAPIView):
    serializer_class = Employee_OnboardingformSerializer

    def get_queryset(self):
        queryset = Emp_Onboardingform.objects.filter(hr_verification ='Pending')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # custom_data = []  
        # for item in response.data:
        #     custom_data.append({
        #         'id': item['id'],
        #         'name': item['name'],
        #     })
        # response.data = custom_data
        return response

    def get_userslist(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
# ========================
    
class employee_verification(RetrieveUpdateAPIView):
    serializer_class = Employee_OnboardingformSerializer

    def get_queryset(self):
        queryset = Emp_Onboardingform.objects.filter(id=self.kwargs['pk'])
        return queryset

    # (use patch method)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if instance.hr_verification == 'Pending': 
                instance.hr_verification = 'Verified'
                instance.save()

            serializer = self.get_serializer(instance)
            return JsonResponse({'Onboardingform_id': instance.id,
                                 'username': instance.username, 
                                 'first_name': instance.first_name,
                                 'last_name': instance.last_name,
                                 'phone': instance.phone,
                                 'status': 'Verified'}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

         
      


