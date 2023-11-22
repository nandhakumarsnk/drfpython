"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from hrms.views import *
from food.views import *
#from hrms.views import UserViewSet
from rest_framework.routers import DefaultRouter


admin.site.site_header  =  "BIITS HRMS"  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/emplogin',user_login.as_view(), name='user login'),
    path('api/emplogout',user_logout.as_view(), name='user logout'),

    path('api/testapi',test_api.as_view(), name='test api'),

    path('api/empregister',user_register.as_view(), name='user register'),
    path('co_user',user_list.as_view(), name='user list'),
    path('co_user/<int:pk>',user_retrieve.as_view(), name='user retrieve'),
    path('co_user/update/<int:pk>',user_update.as_view(), name='user update'),
    path('co_user/delete/<int:pk>',user_delete.as_view(), name='user delete'),


    path('leavetype',leavetype_list.as_view(), name='leavetype list'),
    path('leavetypeUpdate/<int:pk>',leavetype_update.as_view(), name='leavetype update'),
   
    path('api/leave_application',leave_application.as_view(), name='leave Application'),
    path('api/leave_application_list',leave_application_list.as_view(), name='leave application list'),
    path('api/leave_application_list/<int:pk>',leave_application_retrieve.as_view(), name='leave application retrieve'),
    path('api/leave_applicationupdate/<int:pk>',leave_application_update.as_view(), name='leave application update'),
    path('api/leave_applicationdelete/<int:pk>',leave_application_delete.as_view(), name='leave application delete'),

    # path('api/my_leaves',emp_leave.as_view(), name='Emp Leave'),
    # path('api/emp_leave_list',emp_leave_list.as_view(), name='Emp Leave list'),emp_leave_retrieve_forHR
    path('api/emp_leave_list',emp_leave_retrieve.as_view(), name='Emp Leave retrieve'),
    
    path('api/emp_leavebalance/<int:pk>',emp_leavebalance_retrieve.as_view(), name='Emp LeaveBalance retrieve'),
    # path('api/emp_leavebalance',emp_leavebalance_retrieve.as_view(), name='Emp LeaveBalance retrieve'),

    # for HR PURPOSE                   
    path('api/all_leave_applications',emp_leave_retrieve_forHR.as_view(), name='Emp Leave retrieve for HR'),
    path('api/all_leave_approvedlist',emp_leave_approvedlist_forHR.as_view(), name='Emp Leave ApprovedList for HR'),
    path('api/all_leave_rejectedlist',emp_leave_rejectedlist_forHR.as_view(), name='Emp Leave RejectedList for HR'),
    path('api/emps_leavebalance',emp_leavebalancelist_forHR.as_view(), name='Emps Leave balance'),

    path('api/mgconformation_pending',emp_leave_retrieve_forManager.as_view(), name='Emp Leave retrieve for HR'),
    path('api/manager_leaveconformation/<int:pk>',emp_leave_manager_conformation.as_view(), name='Manager Leave conformation'),
    # path('api/manager_leave_notapproved/<int:pk>',leave_rejectByManager.as_view(), name='Manager Leave Not Approved'),

    path('api/assign_leave/<int:pk>',emp_leave_update.as_view(), name='Emp Leave update'),
    path('api/reject_leave/<int:pk>',emp_leave_reject.as_view(), name='Emp Leave reject'),
    path('api/emp_leavedelete/<int:pk>',emp_leave_delete.as_view(), name='Emp Leave delete'),

    path('api/all_entitlements',leave_entitlement_list.as_view(), name='leave entitlement retrieve'),
    path('api/leave_entitlementupdate/<int:pk>',leave_entitlement_update.as_view(), name='leave entitlement update'),
    path('api/add_entitlement/<int:pk>',leave_entitlement_add.as_view(), name='leave entitlement add'),

    path('api/empdocuments', employeeDocumentsUpload.as_view(), name='create_employee'),
    path('api/empdocument_update/<int:pk>', employeeDocumentsUpdate.as_view(), name='create_employee'),
    path('api/emp_profile/<int:pk>', UserProfileDetails.as_view(), name='employee profile'),
    
    path('api/emponboardingform', Employee_Onboardingform_filling.as_view(), name='Onboarding form'),
    # path('api/empformdetails', Employee_formDetails.as_view(), name='Employee details form')
    path('api/empformdetails', empOnboarding_pending.as_view(), name='Employee pending verification'),
    path('api/empformverify/<int:pk>', employee_verification.as_view(), name='Employee form verification'),



    # =========== FOOD APPLICATION =================
    path('api/subscription', subscription_list.as_view(), name='Subscription list'),
    path('api/category', category_list.as_view(), name='Category list'),
    path('api/fooditems/<int:category_id>', category_fooditems.as_view(), name='category food items'),

]  


# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# urlpatterns = router.urls

