#from . import tasks
from django.shortcuts import render, redirect
from demoapp import firedb
import urllib
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import time
import requests
import json
from os import path
from pydub import AudioSegment
from parse import compile
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import re
import pandas as pd
import numpy as np
import io
import os
from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from konlpy import init_jvm
from konlpy.tag import Kkma


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
            if project['Issued']['TF'] == "True":
                continue
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
    if (tasks):
        for task in tasks:
            if tasks[task]['Issued']['TF'] == 'True':
                continue
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
                "task_key" : task,
            }
    print(context)
    return render(request, 'demoapp/dashboard.html', {'tasks' : context, 'projectkey': project_id})

def meeting(request):
    context = {}
    try:
        data2 = {'apiId': 'skku-api-id', 'apiKey': '5fe8577c35784d07a840e0783bda56c7'}

        link = storage.child('wav').child('files').get_url(1)

        storage.child("wav").child('files').download("staticfiles/assets/wavfile/file.wav")

        response = urllib.request.urlopen(link)
        print(response)


        r2 = requests.post("https://api.maum.ai/api/dap/diarize", data=data2, files={"reqVoice": response})
        rescode = r2.status_code
        if (rescode == 200):
            rescode = r2.status_code

            if (rescode == 200):
                contents = r2.content
                ##print(contents)
                res = json.loads(contents.decode('utf-8'))
                from pprint import pprint
                pprint(res)
                ##print(res["data"])
                with open(r'staticfiles/assets/wavfile/diarization.txt', 'w', encoding='utf-8') as f:
                    for i in res["data"]:
                        f.write(str(i))
            else:
                print("Error Code:" + rescode)
            ## 마음api 사용해서 화자 분리하기
        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"] = r"demoapp/Cloud speech to text-408a4dd1362d.json"
        ## 구글 API json 가져오기

        AUDIO_FILE = path.join(path.dirname(path.realpath(r'staticfiles/assets/wavfile')),
                                "file" + ".wav")
        ##print(AUDIO_FILE)

        ## 화자 분리 시간별 endtime이랑 speaker  list 화 시키기
        f = open(r'staticfiles/assets/wavfile/diarization.txt', 'r')
        frequency = {}
        line = f.read().lower()
        ##print(line)
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', line)

        for word in match_pattern:
            count = frequency.get(word, 0)
            frequency[word] = count + 1

        frequency_list = frequency.keys()
        ##print(frequency["endtime"])
        loopnumber = frequency["endtime"]

        p = compile(("{'speaker': {}, 'starttime': {}, 'endtime': {}}") * loopnumber)
        result = p.parse(line)
        ##print(list(result))

        li = np.array(list(result))
        li = li.reshape(loopnumber, 3)
        a = pd.DataFrame(li, columns=['1', '2', '3'])['3']
        b = pd.DataFrame(li, columns=['1', '2', '3'])['1']
        ##print(a)
        ##print(b)
        endpoint = a.tolist()
        speaker_tag = b.tolist()
        ##print(speaker_tag)
        ##print(endpoint)
        f.close()
        endpoint = list(map(float, endpoint))
        ##print(endpoint)

        for i in range(len(endpoint)):
            endpoint[i] = endpoint[i] * 1000
        ## 밀리세컨즈 곱하기 1000

        ##print(endpoint)
        s = ''

        for i in range(len(endpoint)):
            sound = AudioSegment.from_wav('staticfiles/assets/wavfile/file.wav')
            # sound = response.read()
            print(sound)
            ## 시간별 오디오 파일 자르고 (리스트 인덱스로 엔드포인트랑 화자 매치시켜주고 자른 오디오는 newSong으로 매번  덮어씌어서 저장)
            if i == 0:
                newAudio = sound[:endpoint[i]]
                newAudio.export(r'staticfiles/assets/wavfile/newSong.wav', format="wav")

                client = speech.SpeechClient()
                file_name = os.path.join(r'staticfiles/assets/wavfile/newSong.wav')
                with io.open(file_name, 'rb') as diarize_file:
                    content = diarize_file.read()
                    diarize = types.RecognitionAudio(content=content)

                config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    audio_channel_count=1,
                    enable_separate_recognition_per_channel=True,
                    language_code='ko-KR')

                response = client.recognize(config, diarize)

                for result in response.results:
                    ##print('speaker: {}'.format(result.alternatives[0].transcript))
                    s1 = 'speaker' + speaker_tag[i] + ': {}'.format(result.alternatives[0].transcript)
                    s1 = s1.replace("니다", "니다.")
                    s1 = s1.replace("에요", "에요.")
                    s1 = s1.replace("니까", "니까,")
                    s1 = s1.replace("어요", "어요.")
                    s1 = s1.replace("세요", "세요.")
                    s1 = s1.replace("데요", "데요.")
                    s1 = s1.replace("아요", "아요.")
                    s1 = s1.replace("디야", "디야?")
                    s1 = s1.replace("거야", "거야.")
                    s1 = s1.replace("고요", "고요,")
                    s1 = s1.replace("여요", "여요.")
                    s1 = s1.replace("잖아", "잖아,")
                    s1 = s1.replace("네", "네,")
                    s1 = s1.replace("았어", "았어.")
                    s1 = s1.replace("므로", "므로,")
                    s1 = s1.replace("거든", "거든,")
                    s1 = s1.replace("시피", "시피,")
                    s1 = s1.replace("언정", "언정,")
                    s1 = s1.replace("서니", "서니,")
                    s1 = s1.replace("느니", "느니,")
                    s1 = s1.replace("는데", "는데,")
                    s1 = s1.replace("든요", "든요.")
                    s1 = s1.replace("구요", "구요.")
                    s1 = s1.replace("까요", "까요?")
                    s1 = s1.replace("았어", "았어.")
                    s1 = s1.replace("게요", "게요.")
                    s1 = s1.replace("했조", "했조.")
                    s1 = s1.replace("죠", "죠.")
                    s1 = s1.replace("았조", "았조.")
                    s1 = s1.replace("냐", "냐?")
                    s1 = s1.replace("이다", "이다.")
                    s1 = s1.replace("있다", "있다.")
                    s1 = s1.replace("했다", "했다.")
                    s1 = s1.replace("했고", "했고,")
                    s = s + s1 + '\n'
                    ## s에 화자 분리 스피커 구간 계속 쌓아가기
            else:
                newAudio = sound[endpoint[i - 1]:endpoint[i]]
                newAudio.export(r'staticfiles/assets/wavfile/newSong.wav', format="wav")

                client = speech.SpeechClient()
                # file_name = os.path.join(
                #     os.path.dirname(r'staticfiles/assets/wavfile'),
                #     'diarization',
                #     'newSong.wav')
                with io.open(file_name, 'rb') as diarize_file:
                    content = diarize_file.read()
                    diarize = types.RecognitionAudio(content=content)

                config = types.RecognitionConfig(
                    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    audio_channel_count=1,
                    enable_separate_recognition_per_channel=True,
                    language_code='ko-KR')

                response = client.recognize(config, diarize)

                for result in response.results:
                    ##print('speaker: {}'.format(result.alternatives[0].transcript))
                    s1 = 'speaker' + speaker_tag[i] + ': {}'.format(result.alternatives[0].transcript)
                    s1 = s1.replace("니다", "니다.")
                    s1 = s1.replace("에요", "에요.")
                    s1 = s1.replace("니까", "니까,")
                    s1 = s1.replace("어요", "어요.")
                    s1 = s1.replace("세요", "세요.")
                    s1 = s1.replace("데요", "데요.")
                    s1 = s1.replace("아요", "아요.")
                    s1 = s1.replace("디야", "디야?")
                    s1 = s1.replace("거야", "거야.")
                    s1 = s1.replace("고요", "고요,")
                    s1 = s1.replace("여요", "여요.")
                    s1 = s1.replace("잖아", "잖아,")
                    s1 = s1.replace("네", "네,")
                    s1 = s1.replace("았어", "았어.")
                    s1 = s1.replace("므로", "므로,")
                    s1 = s1.replace("거든", "거든,")
                    s1 = s1.replace("시피", "시피,")
                    s1 = s1.replace("언정", "언정,")
                    s1 = s1.replace("서니", "서니,")
                    s1 = s1.replace("느니", "느니,")
                    s1 = s1.replace("는데", "는데,")
                    s1 = s1.replace("든요", "든요.")
                    s1 = s1.replace("구요", "구요.")
                    s1 = s1.replace("까요", "까요?")
                    s1 = s1.replace("았어", "았어.")
                    s1 = s1.replace("게요", "게요.")
                    s1 = s1.replace("했조", "했조.")
                    s1 = s1.replace("죠", "죠.")
                    s1 = s1.replace("았조", "았조.")
                    s1 = s1.replace("냐", "냐?")
                    s1 = s1.replace("이다", "이다.")
                    s1 = s1.replace("있다", "있다.")
                    s1 = s1.replace("했다", "했다.")
                    s1 = s1.replace("했고", "했고,")
                    s = s + s1 + '\n'

        print(s)

        q = open(r'staticfiles/assets/wavfile/diarizationresult1.txt', 'w')
        q.write(s)
        q.close()

        ## 화자 분리 파일 저장
        #
        # ## 형태소 분석해서 키워드와 주요문장 뽑아내기
        # class SentenceTokenizer(object):
        #
        #     def __init__(self):
        #         self.kkma = Kkma()
        #         self.twitter = Twitter()
        #         self.stopwords = ["speaker", "백화점", "롯데", "아", "휴", "아이구", "아이쿠", "아이고", ]
        #
        #     def url2sentences(self, url):
        #         article = Article(url, language='ko')
        #         article.download()
        #         article.parse()
        #         sentences = self.kkma.sentences(article.text)
        #
        #         for idx in range(0, len(sentences)):
        #             if len(sentences[idx]) <= 10:
        #                 sentences[idx - 1] += (' ' + sentences[idx])
        #                 sentences[idx] = ''
        #
        #         return sentences
        #
        #     def txt2sentences(self, txt):
        #         text = text(txt, language='ko')
        #         text.download()
        #         text.parse()
        #         sentences = self.kkma.sentences(article.text)
        #
        #         for idx in range(0, len(sentences)):
        #             if len(sentences[idx]) <= 10:
        #                 sentences[idx - 1] += (' ' + sentences[idx])
        #                 sentences[idx] = ''
        #
        #         return sentences
        #
        #     def text2sentences(self, text):
        #         sentences = self.kkma.sentences(text)
        #         for idx in range(0, len(sentences)):
        #             if len(sentences[idx]) <= 10:
        #                 sentences[idx - 1] += (' ' + sentences[idx])
        #                 sentences[idx] = ''
        #
        #         return sentences
        #
        #     def get_nouns(self, sentences):
        #         nouns = []
        #         for sentence in sentences:
        #             if sentence != '':
        #                 nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence))
        #                                        if noun not in self.stopwords and len(noun) > 1]))
        #         return nouns
        #
        # class GraphMatrix(object):
        #     def __init__(self):
        #         self.tfidf = TfidfVectorizer()
        #         self.cnt_vec = CountVectorizer()
        #         self.graph_sentence = []
        #
        #     def build_sent_graph(self, sentence):
        #         tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        #         self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        #         return self.graph_sentence
        #
        #     def build_words_graph(self, sentence):
        #         cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        #         vocab = self.cnt_vec.vocabulary_
        #         return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word]: word for word in vocab}
        #
        # class Rank(object):
        #     def get_ranks(self, graph, d=0.85):  # d = damping factor
        #         A = graph
        #         matrix_size = A.shape[0]
        #         for id in range(matrix_size):
        #             A[id, id] = 0  # diagonal 부분을 0으로
        #             link_sum = np.sum(A[:, id])  # A[:, id] = A[:][id]
        #             if link_sum != 0:
        #                 A[:, id] /= link_sum
        #             A[:, id] *= -d
        #             A[id, id] = 1
        #         B = (1 - d) * np.ones((matrix_size, 1))
        #         ranks = np.linalg.solve(A, B)  # 연립방정식 Ax = b
        #         return {idx: r[0] for idx, r in enumerate(ranks)}
        #
        # class TextRank(object):
        #     def __init__(self, text):
        #         self.sent_tokenize = SentenceTokenizer()
        #         if text[:5] in ('http:', 'https'):
        #             self.sentences = self.sent_tokenize.url2sentences(text)
        #         else:
        #             self.sentences = self.sent_tokenize.text2sentences(text)
        #         self.nouns = self.sent_tokenize.get_nouns(self.sentences)
        #         self.graph_matrix = GraphMatrix()
        #         self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        #         self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        #         self.rank = Rank()
        #         self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        #         self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        #         self.word_rank_idx = self.rank.get_ranks(self.words_graph)
        #         self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)
        #
        #     def summarize(self, sent_num=1):
        #         summary = []
        #         index = []
        #         for idx in self.sorted_sent_rank_idx[:sent_num]:
        #             index.append(idx)
        #         index.sort()
        #         for idx in index:
        #             summary.append(self.sentences[idx])
        #         return summary
        #
        #     def keywords(self, word_num=3):
        #         ## 워드 넘버로 키워드 갯수 조정
        #         rank = Rank()
        #         rank_idx = rank.get_ranks(self.words_graph)
        #         sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        #         keywords = []
        #         index = []
        #         for idx in sorted_rank_idx[:word_num]:
        #             index.append(idx)
        #         # index.sort()
        #         for idx in index:
        #             keywords.append(self.idx2word[idx])
        #         return keywords
        #
        # summary = ''
        # if(s):
        #     textrank = TextRank(s)
        #     for row in textrank.summarize(3):
        #         ##summarize 넘버로 주요 문장 숫자 조정
        #         ##print(row)
        #         summary = summary + row + '\n'
        #     ##print('keywords :',textrank.keywords())
        #     keywords = ('keywords :', textrank.keywords())
        #
        #     summary = summary.replace('speaker0:', "")
        #     summary = summary.replace('speaker1:', "")
        #     summary = summary.replace('speaker2:', "")
        #     summary = summary.replace('speaker3:', "")
        #     summary = summary.replace('speaker4:', "")
        #     summary = summary.replace('speaker5:', "")
        #
        #     final = open(r'staticfiles/assets/wavfile/textfile.txt', 'w')
        #     final.write(s + '\n')
        #     final.close()

        os.remove(r'staticfiles/assets/wavfile/diarizationresult1.txt')
        os.remove(r'staticfiles/assets/wavfile/newSong.wav')

        context["summary"] = s
    except AttributeError:
        context["summary"] = ""
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

        tasks = db.child("Project").child(project_key).child("Task").get().val()
        if(tasks):
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
        tasks = db.child("Project").child(project_key).child("Task").get().val()
        temp = {}
        if (tasks):
            for task in tasks:
                if tasks[task]['Issued']['TF'] == 'True':
                    continue
                task_info = {}
                task_info['start'] = tasks[task]['task_createdate']
                task_info['end'] = tasks[task]['task_enddate']
                task_info['manager'] = db.child("Members").child(tasks[task]['task_manager']).child('name').get().val()
                temp[tasks[task]['task_name']] = task_info

        context[project_name] = temp
        print(context)
    return render(request, 'demoapp/timeline.html', {"context": context})

def login(request):
    context = {}
    return render(request, 'demoapp/login.html', context)

import wave

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
    # index("a")
    # timeline("a")
    # timeline("a")
    # issue("a")
    meeting("a")