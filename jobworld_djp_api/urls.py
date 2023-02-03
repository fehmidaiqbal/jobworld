from django.urls import include, path

from rest_framework import routers

from jobworld_djp_api.views import CUqualif_info, get_area_info, get_branches, get_city_info, get_courses, get_coursetypes, get_personal_info, get_qualif_info, get_state_info, get_userskill, login_user, register_user, skill_info

router = routers.DefaultRouter()

urlpatterns = [
   path('', include(router.urls)),
   path(r'register',register_user), 
   path(r'Login',login_user),
   path(r'getPersonalInfo',get_personal_info),
   path(r'getLocations',get_state_info),
   path(r'getSubLocation',get_city_info),
   path(r'getAreaLocation',get_area_info),
   path(r'Qualif',CUqualif_info),
   path(r'getQualif',get_qualif_info),
   path(r'getCoursetype',get_coursetypes),
   path(r'Course',get_courses),
   path(r'Branch',get_branches),
   path(r'SkillList',skill_info),
   path(r'Userskill',get_userskill)


]
   
   
   