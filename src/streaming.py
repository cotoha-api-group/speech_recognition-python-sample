# coding:utf-8
import requests
import json
import wave
import sys
import time
from clean_response import clean_response
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
Interval = 0.24  # 240msの音声データを240ms間隔で送信する

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

class Requester:  # 開始要求(start)、データ転送、停止要求(stop)を行うクラス
    def __init__(self):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        wf = wave.open(audio_name, 'rb')
        self.rate = wf.getframerate()
        wf.close()
        self.param_json = {
        "param": {
            "baseParam.samplingRate": self.rate,
            "recognizeParameter.domainId": domain_id,
            "baseParam.delimiter": False,
            "baseParam.punctuation": True,
            "baseParam.reading": True,
            "recognizeParameter.enableProgress": True,
            "recognizeParameter.maxResults": 2,
            }
        }


        self.nframes = int(self.rate * Interval)  # 1回のリクエストで送信するフレーム数

    def get_token(self):  # apigeeでトークンを取得
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        obj = {'grantType': 'client_credentials', 'clientId': self.client_id,
               'clientSecret': self.client_secret}
        data_json = json.dumps(obj).encode("utf-8")
        response = requests.post(url=oauth_url, data=data_json,
                                 headers=headers)
        self.access_token = response.json()['access_token']

    def check_response(self):  # エラー発生時の処理
        if self.response.status_code not in [200, 204]:
            print("STATUS_CODE:", self.response.status_code)
            print(self.response.text)
            exit()

    def start(self):  # 開始要求
        obj = self.param_json
        obj['msg'] = {'msgname': 'start'}
        obj['words'] = ls_dict
        data_json = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "Authorization": "Bearer "+self.access_token}
        self.requests = requests.Session()
        self.response = self.requests.post(url=self.url, data=data_json,
                                           headers=headers)
        self.check_response()
        # uniqueIdはデータ転送、停止要求に必要
        self.unique_id = self.response.json()[0]['msg']['uniqueId']

    def print_result(self):  # レスポンスをパースし認識結果を標準出力
        # statusが200のときのみresponseにjsonが含まれる
        if self.response.status_code == 200:
            for res in self.response.json():
                if res['msg']['msgname'] == 'recognized':
                    # type=2ではsentenceの中身が空の配列の場合がある
                    if res['result']['sentence'] != []:
                        print(clean_response(res['result']['sentence'][0]['surface'])) # 認識結果テキストのみを表示
                        # print(res['result']) # resultを全て出力

    def stop(self):  # 停止要求
        headers = {"Unique-ID": self.unique_id,
                   "Content-Type": "application/json;charset=UTF-8  ",
                   "Authorization": "Bearer " + self.access_token}
        obj = {"msg": {"msgname": "stop"}}
        data_json = json.dumps(obj).encode("utf-8")
        self.response = self.requests.post(url=self.url, data=data_json,
                                           headers=headers)
        self.check_response()
        self.print_result()

    def post(self):  # レスポンスを読み取り、200番台であれば標準出力
        self.response = self.requests.post(url=self.url, data=self.data,
                                           headers=self.headers)
        self.check_response()
        self.print_result()

    def transfer(self):  # データ転送
        wf = wave.open(audio_name, 'rb')
        self.headers = {"Content-Type": "application/octet-stream",
                        "Unique-ID": self.unique_id,
                        "Authorization": "Bearer " + self.access_token}
        self.data = wf.readframes(self.nframes)
        try:
            while self.data:
                start = time.time()
                self.post()  # レスポンスを同期処理で待つ
                elapsed = time.time() - start
                self.data = wf.readframes(self.nframes)
                if elapsed < Interval:  # 最低でも240ms待つ
                    time.sleep(Interval - elapsed)
        except KeyboardInterrupt:  # Ctrl-Cで終了。その際に停止要求
                self.stop()
                print("\nstop")
                wf.close()
                exit()
        wf.close()


def main():
    requester = Requester()
    requester.get_token()
    requester.start()
    requester.transfer()
    requester.stop()


if __name__ == '__main__':
    main()
