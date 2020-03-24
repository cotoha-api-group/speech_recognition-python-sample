COTOHA API 音声認識サンプルクライアント
====


# Usage
`/src/sample.json`を参考にして`/src/`以下に、あなたの認証情報を記載したjsonファイルを任意の名前で作成してください。以後、このjsonファイルを`[your_json]`と表記します。
## file.py  
ファイル音声認識APIを利用して、wavファイルのテキスト化を行うPythonプログラムです。ただし、音声ファイルの長さが1分以内である必要があります。

1. `/src`ディレクトリに移動し、コマンド`python3 file.py ../resources/sample.wav [your_json]`を実行してください。
1. 認識結果が標準出力されます。


## streaming.py
ストリーミング音声認識APIを利用して、wavファイルのテキスト化を行うPythonプログラムです。
1. `/src`ディレクトリに移動し、コマンド`python3 streaming.py ../resources/sample.wav [your_json]`を実行してください。
1. 認識結果が標準出力されます。

## streaming_mic.py
ストリーミング音声認識APIを利用して，マイク入力からテキスト化を行うPythonプログラムです．  
`python3 streaming_mic.py [your_json]`を実行してください．

**出力例**
```bash
Now Recording
音声認識結果が逐次表示されます．
認識結果ごとに改行されて表示されます．
```

## dictionary.py
ユーザ辞書登録APIをコールするPythonプログラムです．  

### ユーザ辞書登録
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json] upload ../resources/sample_dict.tsv`を実行してください．
 1. 成功の場合は，レスポンス200を返します．

### ユーザ辞書クリア
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json] clear` を実行してください．
 1. 成功の場合は，レスポンス200を返します． 

### ユーザ辞書適用状態取得
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json] isset` を実行してください．
 1. 成功の場合は，レスポンス200でユーザ辞書適用状態を返します．

 ### ユーザ辞書ダウンロード
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json] download` を実行してください．
 1. 成功の場合は，レスポンス200でユーザ辞書を返します．  

# Requirements
- Python 3.x
- requests
