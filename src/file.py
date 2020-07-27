import requests
import json
import sys
import wave
from clean_response import clean_response
args = sys.argv
audio_name = args[1]
json_name = args[2]

oauth_url = 'https://api.ce-cotoha.com/v1/oauth/accesstokens'
model_id = 'ja-gen_tf-16' # 音声に合わせて適切なモデル名に変更が必要です。以下の中からお選びください。
# ja-gen_tf-16, ja-gen_sf-16, ja-gen_tf-08, ja-mdl1_nrw-08, ja-mdl2_nrw-08, en_en-gen_sf-16
# 各モデルの詳細はリファレンス(https://api.ce-cotoha.com/contents/reference/apireference.html)をご覧ください
hostname = 'https://api.ce-cotoha.com/api/'
url = hostname + 'asr/v1/speech_recognition/' + model_id

with open(json_name) as f:
    credential = json.load(f)
client_id = credential['client_id']
client_secret = credential['client_secret']
domain_id = credential['domain_id']
wf = wave.open(audio_name, 'rb')
rate = wf.getframerate()
wf.close()

# 一時辞書
ls_dict = []
if len(args)==4:
    temporary_dict_name = args[3]
    with open(temporary_dict_name) as f:
        words = f.readlines()
        for word in words:
            keys = ["surface","reading","prob"]
            values = word[:-1].split("\t")
            d = dict(zip(keys, values))
            ls_dict.append(d)

headers = {"Content-Type": "application/json;charset=UTF-8"}
obj = {'grantType': 'client_credentials',
       'clientId': client_id, 'clientSecret': client_secret}
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
            "baseParam.delimiter": False,
            "baseParam.punctuation": True,
            "baseParam.reading": True,
            "recognizeParameter.maxResults": 2,
        }
}
request_json['words'] = ls_dict

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
        if res['msg']['msgname'] == 'recognized':
            # type=2ではsentenceの中身が空の配列の場合がある
            if res['result']['sentence'] != []:
                print(clean_response(res['result']['sentence'][0]['surface'])) # 認識結果テキストのみを表示
                # print(res['result']) # resultを全て出力

else:
    print("STATUS_CODE:", response.status_code)
    print(response.text)
