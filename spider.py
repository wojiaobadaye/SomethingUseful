import re
with open('1.txt', 'r+', encoding='utf-8') as f:
    a = f.read()

obj3 = re.compile(r'◎译　　名(?P<movie_name>.*?)/.*?◎年　　代(?P<year>.*?)<br />'
                  r'.*?href="(?P<download>.*?)"><strong>', re.S)

res = obj3.search(a)
print(res.group('movie_name'))