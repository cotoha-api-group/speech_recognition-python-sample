# coding:utf-8
'''
COTOHA APIの認識結果を整形するためのスクリプト
'''
def clean_response(text):  # 全角を半角に変換
    OFFSET = ord('０')-ord('0')  # 全角コードと半角コードの差分を取得
    dic = {chr(ord('０')+i): chr(ord('０')+i-OFFSET) for i in range(10)}  # 数字
    dic.update({chr(ord('Ａ')+i): chr(ord('Ａ')+i-OFFSET) for i in range(26)})  # 英字大文字
    dic.update({chr(ord('ａ')+i): chr(ord('ａ')+i-OFFSET) for i in range(26)})  # 英字小文字
    text = text.translate(str.maketrans(dic))
    return text
