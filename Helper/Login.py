import requests
from bs4 import BeautifulSoup
from PIL import Image
import urllib.request


class Student(object):
    def __init__(self):
        self.name = ''
        self.password = ''
        self.code = ''
        self.session = requests.session()
        self.captcha = ''

    def set_account(self):
        self.name = input('请输入用户名：')
        self.password = input('请输入密码：')


class Login(Student):
    def __init__(self):
        Student.__init__(self)
        self.url = 'http://xk.autoisp.shu.edu.cn/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
        self.html = self.session.get(self.url).content
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.url2 = self.soup.find('img', {"id": "Img2"}).get("src")
        self.url3 = urllib.request.urljoin(self.url, self.url2)

    def login(self):
        self.set_account()
        while True:
            try:
                with open('code.jpg', 'wb') as f:
                    f.write(self.session.get(self.url3).content)
                im = Image.open('code.jpg')
                im.show()
                self.captcha = input("请输入验证码：")
                data = {'txtUserName': self.name,
                        'txtPassword': self.password,
                        'txtValiCode': self.captcha}
                resp = self.session.post(self.url, data=data, headers=self.headers)
                b = BeautifulSoup(resp.content, 'html.parser')
                a = b.findAll('div', {'style': 'line-height: 23px;'})
                if a == None:
                    pass
                else:
                    print("Login success!")
                    break
            except AttributeError:
                pass

