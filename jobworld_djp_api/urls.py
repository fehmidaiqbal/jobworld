from django.urls import include, path

from rest_framework import routers

from jobworld_djp_api.views import create__personal_info, create_qualif_info, create_skill_info, get_area_info, get_branches, get_city_info, get_courses, get_coursetypes, get_personal_info, get_qualif_info, get_state_info, get_userskill, login_user, register_user, update_qualif_info, update_skill_info

router = routers.DefaultRouter()


urlpatterns = [
   path('', include(router.urls)),
   path(r'register',register_user), 
   path(r'Login',login_user),
   path(r'createPersonalInfo',create__personal_info),
   path(r'getPersonalInfo',get_personal_info),
   path(r'getLocations',get_state_info),
   path(r'getSubLocation',get_city_info),
   path(r'getAreaLocation',get_area_info),
   path(r'createQualif',create_qualif_info),
   path(r'updateQualif',update_qualif_info),
   path(r'getQualif',get_qualif_info),
   path(r'getCoursetype',get_coursetypes),
   path(r'getCourse',get_courses),
   path(r'getBranch',get_branches),
   path(r'createSkill',create_skill_info),
   path(r'updateSkill',update_skill_info),
   path(r'getskill',get_userskill)


]
   
   
   