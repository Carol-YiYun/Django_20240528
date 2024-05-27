from django.shortcuts import render

# Create your views here.

from smtplib import SMTP, SMTPAuthenticationError, SMTPException

from email.mime.text import MIMEText


def sendmail(request):
    smtp = "smtp.gmail.com: 587" # Gmail 主機位置
    account = "iceshuang@gmail.com" # 輸入 Gmail 帳號
    password = "xhac nwji tzgu fhpv" # 雙驗證後Google系統自動產生的密碼 for Carol的Windows筆電 的應用程式密碼
    
    content = "非常感謝您的訂購，我們將快速出貨！"
    msg = MIMEText(content) # 郵件的內容
    
    msg['Subject'] = "Carol快樂購物網－訂單成立" # 郵件主旨
    
    mailto = "iceshuang@gmail.com" # 寄給單獨的使用者
    #mailto = ["iceshuang@gmail.com", "xxx@gmail.com"] 寄給多個使用者
    
    server = SMTP(smtp) # 建立 SMTP 連線
    server.ehlo() # 與 SMTP 主機溝通
    server.starttls() # 使用 TTLS 安全認證
    
    try:
        server.login(account, password) # 登入，身分確認
        server.sendmail(account, mailto, msg.as_string()) # 寄信
        sendMsg = "郵件已寄出"
        
    except SMTPAuthenticationError:
        sendMsg = "帳號密碼認證錯誤"
    except:
        sendMsg = "郵件發生錯誤"
        
    server.quit() # 關閉 Server 連線
    
    return render(request, "sendMail.html", locals())
        
        
        
        
        
        
        
        
        
        
        
        
        
        