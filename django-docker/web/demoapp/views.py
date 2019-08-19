#from . import tasks
from django.shortcuts import render
from demoapp import firedb

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
    index("a")
