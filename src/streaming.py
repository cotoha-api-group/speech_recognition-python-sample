# coding:utf-8
import requests
import json
import wave
import sys
import time
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


class Requester:  # 開始要求(start)、データ転送、停止要求(stop)を行うクラス
    def __init__(self):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        wf = wave.open(audio_name, 'rb')
        self.rate = wf.getframerate()
        wf.close()
        self.param_json = {"param": {
            "baseParam.samplingRate": self.rate,
            "recognizeParameter.domainId": domain_id,
            "recognizeParameter.enableContinuous": 'true'
            }}
        self.chunk = int(self.rate * Interval)

    def get_token(self):  # apigeeでトークンを取得
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        obj = {'grantType': 'client_credentials', 'clientId': self.client_id, 'clientSecret': self.client_secret}
        data_json = json.dumps(obj).encode("utf-8")
        response = requests.post(url=oauth_url, data=data_json, headers=headers)
        self.access_token = response.json()['access_token']

    def check_response(self):  # エラー発生時の処理
        if self.response.status_code != 200 and self.response.status_code != 204:
            print("STATUS_CODE:", self.response.status_code)
            print(self.response.text)
            exit()

    def start(self):  # 開始要求
        obj = self.param_json
        obj['msg'] = {'msgname': 'start'}
        data_json = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Bearer "+self.access_token}
        self.requests = requests.Session()
        self.response = self.requests.post(url=self.url, data=data_json, headers=headers)
        self.check_response()
        self.unique_id = self.response.json()[0]['msg']['uniqueId']  # uniqueIdはデータ転送、停止要求に必要

    def print_result(self):  # レスポンスをパースし認識結果を標準出力
        if self.response.status_code == 200:  # statusが200のときのみresponseにjsonが含まれる
            for res in self.response.json():
                if res['msg']['msgname'] == 'recognized' and res['result']['sentence'] != []:  # type=2ではsentenceの中身が空の配列の場合がある
                    print(res['result']['sentence'][0]['surface'])

    def stop(self):  # 停止要求
        headers = {"Unique-ID": self.unique_id, "Content-Type": "application/json;charset=UTF-8  ", "Authorization": "Bearer " + self.access_token}
        obj = {"msg": {"msgname": "stop"}}
        data_json = json.dumps(obj).encode("utf-8")
        self.response = self.requests.post(url=self.url, data=data_json, headers=headers)
        self.check_response()
        self.print_result()

    def post(self):  # レスポンスを読み取り、200番台であれば標準出力
        self.response = self.requests.post(url=self.url, data=self.data, headers=self.headers)
        self.check_response()
        self.print_result()

    def transfer(self):  # データ転送
        wf = wave.open(audio_name, 'rb')
        self.headers = {"Content-Type": "application/octet-stream", "Unique-ID": self.unique_id, "Authorization": "Bearer " + self.access_token}
        self.data = wf.readframes(self.chunk)
        try:
            while self.data:
                start = time.time()
                self.post()  # レスポンスを同期処理で待つ
                elapsed = time.time() - start
                self.data = wf.readframes(self.chunk)
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
