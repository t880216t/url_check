#-*-coding:utf-8-*-
import smtplib,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 发送邮件
def Send_Mail(Message, path,mailConfigData):
    msg = MIMEMultipart()
    CURRENTDAY = time.strftime("%Y-%m-%d",time.localtime())
    # 邮件附件
    # att = MIMEText(open(path, 'rb').read(), 'base64', 'utf-8')  # 设置附件的目录
    # att['content-type'] = 'application/octet-stream'
    # att['content-disposition'] = 'attachment;filename="%s result.html"'%CURRENTDAY  # 设置附件的名称
    # msg.attach(att)

    content = str(Message)  # 正文内容
    # body = MIMEText(content, 'plain', 'utf-8')  # 设置字符编码
    body = MIMEText(content, 'html', 'utf-8')  # 设置字符编码
    msg.attach(body)
    msgto = mailConfigData['mail_to_user']+mailConfigData['mail_cc_user']  # 收件人地址多个联系人，格式['aa@163.com'; 'bb@163.com']
    msgfrom = mailConfigData['mail_From']  # 寄信人地址 ,
    msg['subject'] = CURRENTDAY + mailConfigData['mail_subject']  # 主题
    msg['From'] = u'%s <%s>'%(mailConfigData['mail_From_user'],msgfrom) # 主题
    msg['To'] = ";".join(mailConfigData['mail_to_user'])
    msg['Cc'] = ";".join(mailConfigData['mail_cc_user'])#抄送人地址 多个地址不起作用
    msg['date'] = time.ctime()  # 时间

    mailuser = mailConfigData['user_name']  # 用户名
    mailpwd = mailConfigData['user_password']  # 密码
    try:
        smtp = smtplib.SMTP()
        smtp.connect(r'%s'% mailConfigData['mail_server'])  # smtp设置
        smtp.login(mailuser, mailpwd)  # 登录
        smtp.sendmail(msgfrom, msgto, msg.as_string())  # 发送
        smtp.close()
        print("success mail")
    except Exception as e:
        print(e)