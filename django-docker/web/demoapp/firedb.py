import pyrebase
import time
from datetime import datetime
import os
import json

'''
Database 주의할 점
push - Unique Key가 해당 위치에 생기며 그 하위에 넣고자 하는 정보 들어감
set - Unique Key가 생기지 않고 바로 해당 위치 아래에 정보가 들어가나
    #해당 위치의 모든 정보가 사라지고 넣은 정보로 대체됨
'''
config = {
  'apiKey': "AIzaSyAD9cgR44bN3rFqgQ_UDSJDMi4Krv2q58k",
  'authDomain': "web-test-f1437.firebaseapp.com",
  'databaseURL': "https://web-test-f1437.firebaseio.com",
  'projectId': "web-test-f1437",
  'storageBucket': "web-test-f1437.appspot.com",
  "serviceAccount": "demoapp/web-test-f1437-firebase-adminsdk-0mv2u-06bd4466ee.json", #에러나면 여기에 demoapp/를 넣어줌
}

firebase = pyrebase.initialize_app(config)

#db와 storage 연결
db = firebase.database()
storage = firebase.storage()

today = datetime.today().strftime("%Y%m%d")
now = datetime.today().strftime("%Y%m%d_%H%M%S")

#사원 추가 기능
def add_person(name, phone, imageurl, position, division, dept, team, project="None"):
  data = {
    "name" : name,
    "phone" : phone,
    "image" : imageurl,
    "postion" : position,
    "division" : division,
    "dept" : dept,
    "team": team,
    "project" : project
  }
  db.child("Members").push(data)

#프로젝트 추가 기능
def add_project(project_name, project_member, project_createdate, project_enddate, project_content):
  members = db.child("Members").get().val()
  member_data = {}
  for mem in members:
    if members[mem]['name'] in project_member:
      member_data[members[mem]['name']] = mem
  print(member_data)

  data = {
    "project_name" : project_name,
    "project_member" : member_data,
    "project_createdate" : project_createdate,
    "project_enddate" : project_enddate,
    "project_content" : project_content,
  }
  project_key = db.child("Project").push(data)
  db.child("Project").child(project_key).child("Issued").set({"TF": "False", "issued_date": "None"})

  for keys in member_data:
      pj_data = {
        "project" : {project_name : project_key['name']}
      }
      db.child("Members").child(member_data[keys]).child('project').child(project_name).set(project_key['name'])


def add_task(project_key, task_name, task_content, task_manager, task_enddate, task_attachment="None", task_bookmark="False", task_rank="보통", task_state="해야할일"):

  project_members = db.child("Project").child(project_key).child("project_member").get().val()
  if task_manager in project_members.keys():
    task_manager = project_members[task_manager]

  data = {
    "task_name" : task_name,
    "task_content" : task_content,
    "task_manager" : task_manager,
    "task_createdate" : today,
    "task_enddate" : task_enddate,
    "task_attachment" : task_attachment,
    "task_bookmark" : task_bookmark,
    "task_rank" : task_rank,
    "task_state" : task_state,

  }

  task_key = db.child("Project").child(project_key).child("Task").push(data)
  db.child("Project").child(project).child("Task").child(task_key).child("Issued").set(
    {"TF": "False", "issued_date": "None"})


if __name__ == "__main__":
  # add_project("인천터미널점 오더나우 활성화", ["김성우", "박예은", "정용원"], "20190823", "20190911", "인천터미널점 오더나우를 활성화하고, 이를 통해 고객의 오프라인 매장 방문 유도")
  #add_person("박형준", "01099588015", "../../../staticfiles/assets/img/hj.jpg", "담당", "본사", "디지털사업부문", "빅데이터팀")
  #add_task("-Ln1gTOcWncu_RXsr3yv", "오더나우 앱 메인화면 버그개선", " ", "김성우", "20190826")
  # data = db.child("Project").get().val()
  # for project in data.keys():
  #   db.child("Project").child(project).child("Issued").set({"TF": "False", "issued_date": "", "issued_content": ""})
  #   tasks = db.child("Project").child(project).child("Task").get().val()
  #
  #   if (tasks):
  #     for task in tasks.keys():
  #       db.child("Project").child(project).child("Task").child(task).child("Issued").set({"TF": "False", "issued_date": "", "issued_content": ""})
  #for i in data:
  #  db.child("Members").child(i).child("image").set("../../../staticfiles/assets/img/.jpg")
  storage.child('wav').child('files').put('/Users/jonmac/Downloads/files.wav')

  '''
  img = "1.png"
  uploadfile = image_dir + img #upload file directory
  filename = now + os.path.splitext(uploadfile)[1] #현재시간 + 확장자 ex)20190810_160812.png

  #Storage 저장
  storage.child("img/" + filename).put(uploadfile) #올릴 파일 이름: filename / 올릴 파일 출처: uploadfile
  fileUrl = storage.child("img/" + filename).get_url(0) #fileurl 하면
  print(fileUrl)

  print(filename)
  filename = "hello"
  #데이터 json화 시키기
  d = []
  d.append(filename)
  data = json.dumps(d)
  print(data)
  #db 저장
  results = db.child("files").child(str(filename)).set("hi")
  print(results)

  # Retrieve data - 전체 파일목록을 출력해 보자. 안드로이드앱에서 출려하게 하면 된다.
  db = firebase.database()
  files = db.child("files").get().val() #딕셔너리로 반환된다.
  print(files)
  
  data = {
    "name" : "한석환",
    "phone" : "01094637283",
    "image" : "web/staticfiles/img/sh",
    "postion" : "담당",
    "division" : "본사",
    "dept" : "디지털사업부문",
    "team": "IT기획팀",
    "project" : "None"
  }
  db.child("Members").push(data)
  '''