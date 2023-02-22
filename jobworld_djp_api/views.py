from django.http import JsonResponse

from jobworld_djp_api.models import User_personal_info, coursetypes,state_info,city_info,area_info,qualif_info,courses,branches,skills,user_skill
from jobworld_djp_api.Serializer import User_personal_info_Serializer

from rest_framework.decorators import api_view

@api_view(['POST'])
def register_user(request):
        input = request.data
        serializer = User_personal_info_Serializer(data=input)
        valid = serializer.is_valid()
        if valid == False:
            print(serializer.errors)
            return JsonResponse({"error":"invalid data","reason":serializer.errors})
        userName = input.get('email_id')
        # check user name in users table
        userExist = User_personal_info.objects.filter(email_id__exact=userName).exists()
        if(userExist == True):
            response = {"error":"user found, please login"}
            return JsonResponse(response,safe=False) 
        #if no user    
        return create__personal_info(request)

@api_view(['POST'])
def login_user(request):
    input= request.data
    userName = input.get("email_id")
    passWord = input.get("password")
    
    # validate request format
    if len(userName) == 0 or len(passWord) == 0 :
        return JsonResponse({"error":"invalid input"})

    if len(passWord) != 8:
        return JsonResponse({"error":"password is  invalid"})

    #check user_id existance in the table   

    isExist = User_personal_info.objects.filter(email_id__exact = userName).exists()
    
    if isExist == False:
        return JsonResponse({"error":"user not found"})

    dbRow = User_personal_info.objects.filter(email_id__exact = userName).values()
    dbData = dbRow.first()
    dbPassword = dbData["password"]
    
     # validate user name and password with DB data 
    if dbPassword == passWord :
        response = {}
        response["status"] = 1 
        response["user_id"] = dbData["user_id"]
        return JsonResponse(data = response,status = 200)    
   
    # if not throw "error:invalid user//re-enter correct password"
    return JsonResponse({"error":"password not matched"})

def getError(errorMsg):
  return {"error":errorMsg}

def create__personal_info(request):
    input = request.data 
    firstName = input.get('first_name','')
    if len(firstName) == 0:
        return JsonResponse(getError("First Name is missing"))
    secondName = input.get('second_name','')
    if len(secondName) == 0:
        return JsonResponse(getError("Second Name is missing"))
    mobileNo = input.get('mobile_num','')
    if len(mobileNo) != 10:
        return JsonResponse(getError("Mobile No is invalid"))
    userIdenttity = input.get('email_id','')
    if len(userIdenttity) == 0:
        return JsonResponse(getError("email is missing"))
    password = input.get('password','')
    if len(password) == 0:
        return JsonResponse(getError("Password is missing"))
    state = input.get('state_id','')
    if state == 0:
        return JsonResponse(getError("State Name is missing"))
    city = input.get('city_id','')
    if city == 0:
        return JsonResponse(getError("City Name is missing"))
    area = input.get('area_id','')
    if area == 0:
        return JsonResponse(getError("Area Name is missing"))

    if request.method == 'POST':
        Obj1 = User_personal_info(first_name = firstName,second_name = secondName,mobile_num = mobileNo, email_id = userIdenttity, password = password,state_id = state,city_id = city,area_id = area)
        Obj1.save()
        return JsonResponse(status = 201,data={"status":1,"UserId":Obj1.user_id})
    
    elif request.method == 'PUT':
        userId = input.get('user_id',0)
        if userId == 0 :
            return  JsonResponse(getError("UserId is missing"))

        Obj2 = User_personal_info(user_id= userId,first_name = firstName,second_name = secondName,mobile_num = mobileNo, email_id = userIdenttity, password = password,state_id = state,city_id = city,area_id = area)
        Obj2.save()
        return JsonResponse(status = 201,data={"firstName":Obj2.first_name},safe=False)


@api_view(['GET'])  
def get_personal_info(request):
    input = request.query_params
    userId = input['user_id']
    queryList = User_personal_info.objects.filter(user_id__exact = userId).values()
    print(type(queryList))
    PList = []
    for item in queryList:
        PList.append(item)
    return JsonResponse(data = PList,status=201,safe=False)

    
@api_view(['POST','GET'])  
def get_state_info(request):
    if request.method == 'POST':
        input = request.data
        state = input.get("state_name")
        obj = state_info(state_name=state)
        obj.save()
        return JsonResponse(data={"State_Id":obj.state_id},status = 201,safe=False)
    
    queryList = state_info.objects.all()
    aList = []
    for item in queryList:
        temp = {"State_Id":item.state_id,"State":item.state_name}
        aList.append(temp)
    return JsonResponse(data = aList,status=200,safe=False)

   

@api_view(['POST','GET'])  
def get_city_info(request):
    if request.method == 'POST':
        input = request.data
        city = input.get("city_name")
        stateId = input.get("state_id")
        obj = city_info(state_id = stateId ,city_name = city)
        obj.save()
        return JsonResponse(data={"City_Id":obj.city_id},status = 201,safe=False)

    input = request.query_params
    stateId = input['state_id']
    
    if len(stateId) != 0 :
        queryList = city_info.objects.filter(state_id__exact = stateId).values()
        CList = []
        for item in queryList:
            CList.append(item)
            
        return JsonResponse(data =CList ,status=200,safe=False)

    queryList = city_info.objects.all()
    CList = []
    for item in queryList:
        temp = {"StateId":item.state_id,"CityId":item.city_id,"CityName":item.city_name}
        CList.append(temp)
    return JsonResponse(data=CList,status=200,safe=False)
    
@api_view(['POST','GET'])  
def get_area_info(request):
    input = request.data
    if request.method == 'POST':
        cityId = input.get("city_id",'')
        area = input.get("area_name",'')
        Obj = area_info(city_id = cityId,area_name = area)
        Obj.save()
        return JsonResponse(data={"Area_Id":Obj.area_id},status = 201,safe=False)

  
    input = request.query_params
    cityId = input.get('city_id','')
    if len(cityId) != 0 :
        queryList = area_info.objects.filter(city_id__exact = cityId).values()
        AList = []
        for item in queryList:
            AList.append(item)
        return JsonResponse(data =AList ,status=200,safe=False)

    queryList = area_info.objects.all()
    AList = []
    for item in queryList:
        temp= {"City":item.city_id,"Area":item.area_id,"AreaName":item.area_name}
        AList.append(temp)
    return JsonResponse(data = AList ,status=200,safe=False)


@api_view(['POST','PUT'])  
def CUqualif_info(request):
    input = request.data 
    userId = input.get('user_id',0)
    if userId == 0:
        return JsonResponse(getError("UserId is missing in request"))
    
    userExist = User_personal_info.objects.filter(user_id__exact = userId).exists()
    if userExist == False:
        return JsonResponse(getError("user not found"))

    courseTypeId = input.get('coursetype_id',0)
    if courseTypeId == 0:
        return JsonResponse(getError("CourseTypeId is missing in request"))

    courseId = input.get('course_id',0)
    if courseId == 0:
        return JsonResponse(getError("CourseId is missing in request"))

    branchId = input.get('branch_id',0)
    if branchId == 0:
        return JsonResponse(getError("BranchId is missing in request"))
    
    year = input.get('passout_year',0)
    if year == 0:
        return JsonResponse(getError("Year is missing in request"))

    qualif = input.get('highest_qualif','')
    if qualif == " ":
        return JsonResponse(getError("Qualification is  missing in request"))

    aggre = input.get('aggregate',0)
    if (aggre!=0 and aggre > 99 ):
        return JsonResponse(getError("invalid Aggregate"))

    if request.method == 'POST':
        Obj2 = qualif_info(user_id = userId, coursetype_id = courseTypeId ,course_id = courseId,branch_id = branchId,passout_year = year,highest_qualif = qualif,aggregate = aggre)
        Obj2.save()
        response = {"qualification_id":Obj2.qualif_id}
        return JsonResponse(status = 201,data = response)
        
    elif request.method == 'PUT':
        qualificationId = input.get('quailfication_id',0)
        if qualificationId == 0 :
            return  JsonResponse(getError("qualificationId is missing"))
        Obj3 = qualif_info(qualif_id = qualificationId,user_id = userId, coursetype_id = courseTypeId ,course_id = courseId,branch_id = branchId,passout_year = year,highest_qualif = qualif,aggregate = aggre)
        Obj3.save()
        return JsonResponse(status = 201,data = Obj3)
    

@api_view(['GET'])  
def get_qualif_info(request):
    input = request.query_params
    userId= input['user_id']
    if len(userId) == 0:
        return JsonResponse(getError("UserId is missing in request"))

    queryList = qualif_info.objects.filter(user_id__exact = userId).values()
    Qlist = []
    for item in queryList:
        Qlist.append(item)
        return JsonResponse(data = Qlist,status=200,safe=False)


@api_view(['POST','GET'])  
def get_coursetypes(request):
    if request.method == 'POST':
        input = request.data
        courseType = input.get("coursetype_name",'')
        courseDuration = input.get("coursetype_duration",0)
       
        Obj = coursetypes(coursetype_name = courseType,coursetype_duration = courseDuration)
        Obj.save()
        return JsonResponse(data={"coursetype_id":Obj.coursetype_id},status = 201,safe=False)
    
    queryList = coursetypes.objects.all()
    aList = []
    for item in queryList:
        temp = {"CourseType" : item.coursetype_name,"CourseTypeId": item.coursetype_id,"CourseDuration" : item.coursetype_duration}
        aList.append(temp)
    return JsonResponse(data = aList,status=200,safe=False)


@api_view(['POST','GET'])  
def get_courses(request):
    input = request.data
    if request.method == 'POST':
        courseTypeId = input.get('coursetype_id',0)
        courseName = input.get('course_name','')
        temp = courses(course_name = courseName,coursetype_id = courseTypeId)
        temp.save()
        return JsonResponse(data={"course_id":temp.course_id},status = 201,safe=False)

    input = request.query_params
    req_coursetype_id = input.get('coursetype_id',0)
    if len(req_coursetype_id) == 0:
        return JsonResponse(getError("CourseTypeId is missing in request"))

    queryList = courses.objects.filter(coursetype_id__exact = req_coursetype_id).values()
    responseCoursesList = []
    for item in queryList:
        responseCoursesList.append(item)
    return JsonResponse(data = responseCoursesList,status =200,safe = False)
    
@api_view(['POST','GET'])  
def get_branches(request):
    input = request.data
    if request.method == 'POST':
        courseId = input.get('course_id',0)
        branchName = input.get('branch_name','')
        temp = branches(branch_name = branchName,course_id = courseId)
        temp.save()
        return JsonResponse(data={"branch_id":temp.branch_id},status = 201,safe=False)

    input = request.query_params
    req_course_id = input.get('course_id','')
    if len(req_course_id) == 0:
        return JsonResponse(getError("CourseId is missing in request"))

    queryList = branches.objects.filter(course_id__exact = req_course_id).values()
    responseBranchesList = []
    for item in queryList:
        responseBranchesList.append(item)
     
    return JsonResponse(data = responseBranchesList,status =200,safe = False)

@api_view(['GET','POST'])  
def skill_info(request):
    if request.method == 'POST':
        input = request.data
        skill = input.get("skill",'')
        obj = skills(skill_name=skill)
        obj.save()
        return JsonResponse(data={"skill_id":obj.skill_id},status = 201,safe=False)
    queryList = skills.objects.all()
    aList = []
    for item in queryList:
        aSkill = {"skill_id":item.skill_id,"skill_name":item.skill_name}
        aList.append(aSkill)
    return JsonResponse(data = aList,status=200,safe=False)


@api_view(['POST','GET'])  
def get_userskill(request):
    if request.method == 'POST':
        input = request.data
        userId = input.get("user_id",0)
        skillId = input.get("skill_id",0)
        experience = input.get("experience",0)
        Obj = user_skill(user_id = userId,skill_id = skillId,experience = experience)
        Obj.save()
        USlist = {"UserId": Obj.user_id,"SkillId":Obj.skill_id,"Experience":Obj.experience}
        return JsonResponse(data=USlist,status =201,safe=False)

    if request.method == 'GET':
        input = request.query_params 
        userId = input.get('user_id',0)
        if userId == 0:
            return JsonResponse(getError("UserId is missing in request"))
        queryList = user_skill.objects.filter(user_id__exact = userId).values()
        USlist = []
        for item in queryList:
            USlist.append(item)
     
    return JsonResponse(data = USlist,status =200,safe=False)
    



