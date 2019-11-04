import time
import urllib.request
import urllib.error
import socket
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def getUrl(url,header={},proxy=None,cookie=None,timeout=None,data=None):
    '''A simple getUrl function.

    5 agrument:url,header=None,,proxy=None,cookie=None,timeout=None
        url             url,
        header=None     add header, example: header={'User-Agent':'chrome'}
        proxy=None      add prxoy,
        cookie=None     set cookie,
        timeout=None    timeout,
        data=None       POST request.
    '''
    global response
    if proxy != None:
        print('This argument useless yet!')
    elif cookie != None:
        print('This argument useless yet!')

    else:
        req = urllib.request.Request(url,data=None,headers=header)
        try:
            response = urllib.request.urlopen(req,timeout)
        except urllib.error.HTTPError as e:
            print('\nHTTP Error : ' + '\t' + str(e.code) + ' ' + str(e.reason))
            print()
        except urllib.error.URLError as e:
            if isinstance(e.reason,socket.timeout): #import socket
                print('TIME OUT')
            else:
                print('URLError' + str(e.reason))
        else:
            pass
    return(response)

#https://cdn-node-status.s.upyun.com/node-stats.html #监控地址
#https://cdn-node-status.s.upyun.com/node-pings?down=1 #异常数据来源
#异常数据内容 #字符串  #node_post = [{"ping1":594.5,"node":"ntt-cn-hkg","ping2":2500,"n":"边缘节点","ip":"157.119.232.6","pubtime":"2018-02-09 08:40:00"}]

[{"ping1":594.5,"node":"ntt-cn-hkg","ping2":2500,"n":"边缘节点","ip":"157.119.232.6","pubtime":"2018-02-09 08:40:00"}]


expect_node = ['ntt-cn-hkg'] #此处排除节点  有些正常的节点报宕机

while True:
    try:
        url = 'https://cdn-node-status.s.upyun.com/node-pings?down=1'
        #下载宕机数据的网页
        html = getUrl(url,header={'Cookie':'_ga=GA1.2.410581199.1517732476; Hm_lvt_09e47f90c12c9a15516512c0d87f6791=1517732476,1517732480; _oauth2_proxy=eWRfbW9uaXRvckB1cGFpLmNvbQ==|1517989853|EBqomqYqv32GTmI7L72HVxjc8e0=','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'})
        html = html.read().decode('utf-8') #解码

        if len(html) < 3:
            print('节点正常 无宕机...     ' + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))


        else: #
            mail_host="smtp.163.com"  #设置服务器
            mail_user="wevie_9@163.com"    #用户名
            mail_pass="Aa123456"   #口令

            sender = 'wevie_9@163.com' #发件人 最好写全
            receivers = ['noc@verycloud.cn']  # 接收者邮箱

            for i in eval(html): #字符转转换格式
                warn_node =  i['node']

            if  warn_node in expect_node:
                print(warn_node + '  此节点忽略...')
                continue

            print(warn_node + '  宕机 请查看邮件......')

            content = '节点： ' + warn_node + '\n时间： ' + str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) + '\n查看： https://cdn-node-status.s.upyun.com/node-stats.html'
            title = '又拍云节点无法提供服务！'

            def sendEmail():
                message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
                message['From'] = "{}".format(sender)
                message['To'] = ",".join(receivers)
                message['Subject'] = title

                try:
                    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
                    smtpObj.login(mail_user, mail_pass)  # 登录验证
                    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
                    print("mail has been send successfully.")
                except smtplib.SMTPException as e:
                    print(e)

            if __name__ == '__main__':
                sendEmail()
            time.sleep(300)

    except urllib.error.HTTPError as e:
        print('HTTPError' + str(e))
    else:
        pass
    time.sleep(20)
