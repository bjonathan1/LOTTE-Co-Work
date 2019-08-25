#from . import tasks
from django.shortcuts import render, redirect
from demoapp import firedb
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

db = firedb.db
storage = firedb.storage

'''

#임의로 김성우로 지정

'''


user_name = "김성우" #사람을 변경하고 싶다면 여기에 이름 바
user_key = ""
user_projects = {}

session = db.child("Members").get().val()
for keys in session:
    if session[keys]['name'] == user_name:
        user_key = keys

user_projects = db.child("Members").child(user_key).child('project').get().val()

def index(request):
    context = {}

    # user_key = request.session.get('_user')
    count = 1
    img_url = db.child("Members").get().val()
    if user_projects:
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
    if request.method == 'POST':
        request.session['_old_post'] = request.POST['msg']
        return redirect('/dashboard/')
    project_id = request.session.get('_old_post')

    members = db.child("Members").get().val()
    tasks = db.child("Project").child(project_id).child("Task").get().val()
    count = 1

    for task in tasks:
        task_num = "task" + str(count)
        count += 1
        context[task_num] = {
            "task_name" : tasks[task]['task_name'],
            "task_content" : tasks[task]['task_content'],
            "task_manager" : members[tasks[task]['task_manager']]['name'],
            "task_managerurl": members[tasks[task]['task_manager']]['image'],
            "task_createdate" : tasks[task]['task_createdate'],
            "task_enddate" : tasks[task]['task_enddate'],
            "task_ddate" : str(int(tasks[task]['task_enddate']) - int(tasks[task]['task_createdate'])),
            "task_attachment" : tasks[task]['task_attachment'],
            "task_bookmark" : tasks[task]['task_bookmark'],
            "task_state" : tasks[task]['task_state'],
        }
    print(context)
    return render(request, 'demoapp/dashboard.html', {'tasks' : context})

def meeting(request):
    context = {}
    return render(request, 'demoapp/meeting.html', context)

def issue(request):
    context = {}

    projects = db.child('Project').get().val()
    project_context = {}
    task_context = {}
    for project in user_projects.keys():
        project_name = project
        project_key = user_projects[project]
        project_issue = projects[project_key]['Issued']
        if project_issue['TF'] == 'True':
            issued_date = project_issue['issued_date']
            issued_content = project_issue['issued_content']
            project_context[project_name] = {"issued_date": issued_date, "issued_content": issued_content}
            continue

        tasks = projects[project_key]['Task']
        for task in tasks.keys():
            task_name = tasks[task]['task_name']
            task_issue = tasks[task]['Issued']
            if task_issue['TF'] == 'True':
                task_issued_date = task_issue['issued_date']
                task_issued_content = task_issue['issued_content']
                task_context[task_name] = {"project_name": project_name,"issued_date": task_issued_date, "issued_content": task_issued_content}

    context['project'] = project_context
    context['task'] = task_context

    print(project_context)
    print(task_context)
    print(context)

    return render(request, 'demoapp/issue.html', context)

def drive(request):
    context = {}
    return render(request, 'demoapp/drive.html', context)

def timeline(request):
    context = {}

    user_projects = db.child("Members").child(user_key).child('project').get().val()
    projects = db.child("Project").get().val()

    for project in user_projects.keys():
        project_name = project
        project_key = user_projects[project]
        if projects[project_key]['Issued']['TF'] == 'True':
            continue
        tasks = projects[project_key]['Task']
        temp = {}
        for task in tasks:
            if tasks[task]['Issued']['TF'] == 'True':
                continue
            task_info = {}
            task_info['start'] = tasks[task]['task_createdate']
            task_info['end'] = tasks[task]['task_enddate']
            temp[tasks[task]['task_name']] = task_info

        context[project_name] = temp
        print(context)
    return render(request, 'demoapp/timeline.html', {"context": context})

def login(request):
    context = {}
    return render(request, 'demoapp/login.html', context)

def login_ok(request):
    context = {}
    if request.method == 'POST':
        id = request.POST['id']
        pw = request.POST['pw']

        members = db.child('Members').get().val()
        for member in members:
            if members[member]['name'] == id and members[member]['pw'] == pw:
                request.session['_user'] = member
    return redirect('/main/')


if __name__ == "__main__":
    #index("a")
    # timeline("a")
    issue("a")