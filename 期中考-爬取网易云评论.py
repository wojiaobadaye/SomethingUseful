import requests
import csv
from Crypto.Cipher import AES
import json
from base64 import b64encode

url = 'https://music.163.com/weapi/comment/resource/comments/get?'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.52'
}
# post实际上请求的数据
data = {
    'csrf_token': "",
    'cursor': "-1",
    'offset': "0",
    'orderType': "1",
    'pageNo': "1",
    'pageSize': "20",
    'rid': "R_SO_4_28773613",
    'threadId': "R_SO_4_28773613"
}
# 加密过程
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341' \
    'f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b' \
    '97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = "yry1JqhkzgfwtTIt"


def get_encSecKey():  # 需要的三个参数分别是data, e, f,由function c实现
    return "96d12beda5be6d368c9aeac38fc65892d04aa072298911ec245ee2c177a21a66c3a0dc1c7025ebe35707c083e003da8f2959a4" \
           "accb0f14b15e4398331e9f7aa3df5656faeffe909fb6d74b92d1fad1309e6adeff2d6f0ad4dec90de42a0a83232f58a02f2215e" \
           "b184a61a1f11b2d8970aa0ab4102635b677f4a626cdebbeed57"


def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


def get_encText(data):
    first = get_enc(data, g)
    second = get_enc(first, i)
    return second


def get_enc(data, key):
    iv = "0102030405060708"
    da = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), IV=iv.encode('utf-8'), mode=AES.MODE_CBC)
    bs = aes.encrypt(da.encode('utf-8'))
    return str(b64encode(bs), 'utf-8')


resp = requests.post(url, data={
    'params': get_encText(json.dumps(data)),
    'encSecKey': get_encSecKey()
})
print(resp.text)


"""!function() {
    function a(a) { # 返回随机的16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b) # c是密钥----b也是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a) # 数据
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d, # 偏移量
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {  #第一个参数是数据；e = '010001'
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
    function e(a, b, d, e) {
        var f = {};
        return f.encText = c(a + e, b, d),
        f
    }
    window.asrsea = d,
    window.ecnonasr = e
}();"""
