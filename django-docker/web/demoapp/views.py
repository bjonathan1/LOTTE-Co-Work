#from . import tasks
from django.shortcuts import render

from demoapp import firedb
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def public_api(request):
    if request.method=='POST':
       return HttpResponse('API hit with post method')

db = firedb.db
storage = firedb.storage

#임의로 김성우로 지정
user_name = "김성우"
user_key = ""
user_projects = {}

session = db.child("Members").get().val()
for keys in session:
    if session[keys]['name'] == user_name:
        user_key = keys

user_projects = db.child("Members").child(user_key).child('project').get().val()

def index(request):
    '''
    넘겨야 하는 내용들:
        task
        project name
        project enddate
        project content
        project members
        project members img url
    '''

    count = 1
    img_url = db.child("Members").get().val()
    context = {}

    for keys in user_projects:
        task_num = "task" + str(count) #task
        count += 1
        project_name = keys #proj name
        project = db.child("Project").child(user_projects[keys]).get().val()
        project_content = project['project_content'] #content
        project_createdate = project['project_createdate'] #createdate
        project_enddate = project['project_enddate'] #enddate

        #각 멤버들이 이름과 이미지 위치 출력
        members = project['project_member']
        project_members = [] #members
        project_urls = [] #img_urls
        for mem in members:
            project_members.append(mem)
            project_urls.append(img_url[members[mem]]['image'])

        context[task_num] = {
                "project_key" : user_projects[keys],
                "project_name" : project_name,
                "project_content" : project_content,
                "project_createdate" : project_createdate,
                "project_enddate" : project_enddate,
                "project_members" : project_members,
                "project_urls" : project_urls
            }


        print(context)
    return render(request, 'demoapp/project_display.html', {"tasks": context})

def dashboard(request):
    context = {}
    #project_id = request.POST['msg']
    #project_id = HttpRequest.readlines()
    project_id = request.POST.get('project_key', '')
    # project_id = '-LmIXx-2iy62TD4n7iHH'
    print(project_id)
    '''
    tasks = db.child("Project").child(project_id).child("Task").get().val()
    count = 1

    for task in tasks:
        task_num = "task" + str(count)
        count += 1
        context[task_num] = {
            "task_name" : tasks[task]['task_name'],
            "task_content" : tasks[task]['task_content'],
            "task_manager" : tasks[task]['task_manager'],
            "task_createdate" : tasks[task]['task_createdate'],
            "task_enddate" : tasks[task]['task_enddate'],
            "task_attachment" : tasks[task]['task_attachment'],
            "task_bookmark" : tasks[task]['task_bookmark'],
            "task_rank" : tasks[task]['task_rank'],
            "task_state" : tasks[task]['task_state'],
        }
    print(context)
    '''
    return render(request, 'demoapp/dashboard.html', context)

def meeting(request):
    context = {}
    return render(request, 'demoapp/meeting.html', context)

def issue(request):
    context = {}
    return render(request, 'demoapp/issue.html', context)

def drive(request):
    context = {}
    return render(request, 'demoapp/drive.html', context)

def timeline(request):
    context = {}
    return render(request, 'demoapp/timeline.html', context)


if __name__ == "__main__":
    dashboard("a")
