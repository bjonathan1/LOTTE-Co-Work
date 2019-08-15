import pyrebase
import time
from datetime import datetime
import os
import json


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

  for keys in member_data:
      pj_data = {
        "project" : {project_name : project_key['name']}
      }
      db.child("Members").child(member_data[keys]).child('project').child(project_name).set(project_key['name'])

if __name__ == "__main__":
  #add_project("롯데백화점 협업툴 제작", ["김성우", "김익준", "박예은", "박형준", "정용원"], today, "20190829", "롯데백화점만의 협업 툴 LCW를 제작하기 위한 프로젝트")
  #add_person("박형준", "01099588015", "../../../staticfiles/assets/img/hj.jpg", "담당", "본사", "디지털사업부문", "빅데이터팀")
  #data = db.child("Members").get().val()
  #for i in data:
  #  db.child("Members").child(i).child("image").set("../../../staticfiles/assets/img/.jpg")


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