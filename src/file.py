import requests
import json
import sys
import wave
args = sys.argv
audio_name = args[1]
json_name = args[2]
oauth_url = 'https://api.ce-cotoha.com/v1/oauth/accesstokens'
model_id = 'ja-gen_tf-16'
hostname = 'https://api.ce-cotoha.com/api/'
url = hostname + 'asr/v1/speech_recognition/' + model_id
with open(json_name) as f:
    credential = json.load(f)
client_id = credential['client_id']
client_secret = credential['client_secret']
domain_id = credential['domain_id']
Interval = 0.24  # 1メッセージあたり240msの音声データ
wf = wave.open(audio_name, 'rb')
rate = wf.getframerate()
wf.close()

headers = {"Content-Type": "application/json;charset=UTF-8"}
obj = {'grantType': 'client_credentials', 'clientId': client_id, 'clientSecret': client_secret}
data_json = json.dumps(obj).encode("utf-8")
response = requests.post(url=oauth_url, data=data_json, headers=headers)
access_token = response.json()['access_token']

MIMETYPE_JSON = 'application/json'
MIMETYPE_AUDIO = 'application/octet-stream'
headers = {'Authorization': 'Bearer '+access_token}
request_json = {
        "msg": {
            "msgname": "start"
        },
        "param": {
            "baseParam.samplingRate": rate,
            "recognizeParameter.domainId": domain_id,
            "recognizeParameter.enableContinuous": True
        }
}
command_json = {
        "msg": {
            "msgname": "stop"
        }
}
wf = wave.open(audio_name, 'rb')
fileDataBinary = wf.readframes(wf.getnframes())
wf.close()
files = [

        ('parameter', (None, json.dumps(request_json), MIMETYPE_JSON)),
        ('audio', (None, fileDataBinary, MIMETYPE_AUDIO)),
        ('command', (None, json.dumps(command_json), MIMETYPE_JSON))
]
response = requests.post(url, headers=headers, files=files)

if response.status_code == 200:  # statusが200のときのみresponseにjsonが含まれる
    for res in response.json():
        if res['msg']['msgname'] == 'recognized' and res['result']['sentence'] != []:  # type=2ではsentenceの中身が空の配列の場合がある
            print(res['result']['sentence'][0]['surface'])
else:
    print("STATUS_CODE:", response.status_code)
    print(response.text)
