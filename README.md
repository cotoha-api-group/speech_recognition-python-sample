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


## dictionary.py
ユーザ辞書登録APIを利用して，tsvファイルからユーザ辞書登録 及び ユーザ辞書クリアAPIを利用して，ユーザ辞書を削除するPythonプログラムです．  

### ユーザ辞書登録
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json] ../resources/sample_dict.tsv`を実行してください．
 1. 登録成功の場合は，レスポンス200を返します．

### ユーザ辞書クリア
 1. `/src` ディレクトリに移動し，コマンド `python3 dictionary.py [your_json]` を実行してください．
 1. 辞書クリア成功の場合は，レスポンス200を返します． 


# Requirements
- Python 3.x
- requests
