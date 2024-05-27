from django.shortcuts import render,redirect

from cart import models
from product.models import Goods
from django.http import HttpResponseRedirect

from django.utils.html import format_html # for 263 行


# 搭配 ECPay 的設定
import os
basedir = os.path.dirname(__file__) # 抓取預設目錄的位置
file = os.path.join(basedir, 'ecpay_payment_sdk.py')

# 嵌入 ECPay 的 SDK 設定
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

# 嵌入 ECPay 的 SDK 設定－結束


# Create your views here.

cartlist = list() #購物車的內容
customname = '' #顧客姓名
customphone = '' #顧客電話
customaddress = '' #顧客地址
customemail = '' #顧客email

orderTotal = 0 # 信用卡刷卡金額

goodsTitle = list() # 存放購物車訂單內容商品項目名稱



def cart(request): #顯示購物車內容
    global cartlist #設定cartlist是全域變數
    allcart = cartlist
    total = 0
    
    #unit[0] 商品名稱
    #unit[1] 價格
    #unit[2] 數量
    #unit[3] 價格 x 數量
    
    for unit in cartlist:
        total += int(unit[3])
    granttotal = total + 100 #運費100元
    return render(request, 'cart.html', locals())
    
def addtocart(request, ctype=None, productid=None):
    global cartlist
    
    if ctype == "add": #當將商品加入購物車後
        product = Goods.objects.get(id=productid)
        flag = True #預設購物車中沒有相同商品，表示此商品不存在於購物車
        
        #先檢查購物車中的商品是否有重複
        for unit in cartlist:
            if product.title == unit[0]: #表示有這個商品
                unit[2] = str(int(unit[2]) + 1) #數量再加1
                unit[3] = str(int(unit[3]) + product.price) #累計金額
                flag = False #表示此商品已加入購物車
                break
            
        if flag:
            templist = list()
            templist.append(product.title)
            templist.append(str(product.price))
            templist.append('1')
            templist.append(str(product.price))
            cartlist.append(templist)
            
            
        request.session['cartlist'] = cartlist #將購物車內容存入Session中，Session是暫存
        return redirect('/cart/')            
        
    elif ctype == "update":
        n=0
        for unit in cartlist: #修改 cartlist 內的數量和總金額
            unit[2] = request.POST.get('qty'+str(n), '1')
            unit[3] = str( int(unit[1]) * int(unit[2]) )
            n += 1
        request.session['cartlist'] = cartlist
        return redirect('/cart/')      
            
    # redirect 直接跳到指定的網址，沒有帶任何參數
    # render 跳到指定網址，並將要求(request)的參數內容傳過去

    elif ctype == "empty":
        cartlist = list() #指向空的串列
        request.session['cartlist'] = cartlist
        return redirect('/cart/')      

    elif ctype == "remove":
        del cartlist[int(productid)] #將放入的商品索引值刪除
        request.session['cartlist'] = cartlist
        return redirect('/cart/')  
    



    
def cartorder(request): #結帳頁面

    #結帳是要登入的，沒有登入不能結帳
    if "isAlive" in request.session :
    
        global cartlist, customname, customphone, customaddress, customemail
        allcart = cartlist
        total = 0
        for unit in cartlist:
            total += int(unit[3])
        granttotal = total + 100  #100是運費
        
        name = customname
        phone = customphone
        address = customaddress
        email = customemail
    
        return render(request, 'cartorder.html', locals())
    else:
        return HttpResponseRedirect('/login')
    
    
def cartok(request):
    
    global cartlist, customname, customphone, customaddress, customemail
    
    global orderTotal, goodsTitle # 為了綠界測試
    
    total = 0
    for unit in cartlist:
        total += int(unit[3])
    granttotal = total + 100  #100是運費
    
    orderTotal = granttotal # 為了綠界測試
    
    customname = request.POST.get('cuName','')
    customphone = request.POST.get('cuPhone','')
    customaddress = request.POST.get('cuAddr','')
    customemail = request.POST.get('cuEmail','')
    payType = request.POST.get('payType','')
    
    #新增資料到資料表中
    unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, granttotal=granttotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=payType)
    
    for unit in cartlist:
        goodsTitle.append(unit[0]) #將訂單內容的商品細項名稱加到 goodsTitle 中，為了綠界測試
        total = int(unit[1]) * int(unit[2])
        unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
        

    orderid = unitorder.id #取得訂單編號
    name = unitorder.customname
    email = unitorder.customemail
    cartlist = list()
    
    request.session['cartlist'] = cartlist
    
    
    return HttpResponseRedirect('/creditcard')
    #return render(request, 'cartok.html', locals())
    

def cartordercheck(request):
    orderid = request.GET.get('orderid','')
    customemail = request.GET.get('customemail','')

    if orderid == ' ' and customemail == ' ':
        firstsearch = 1
    else:
        order = models.OrdersModel.objects.filter(id=orderid).first() #抓取第一筆資料
        # order = models.OrdersModel.objects.filter(id=orderid, customemail=customemail) 上一行的另一種寫法
        if order == None or order.customemail != customemail:
            notfound = 1
        else:
            details = models.DetailModel.objects.filter(dorder=order)
            
    return render(request, 'cartordercheck.html', locals())
    
    
    
def ECPayCredit(request):
    
    global goodsTitle
    
    Title = ""
    for i in goodsTitle:
        Title += i + "#"
    
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"), # 訂單編號(主鍵，以交易時間為值)，正式環境下要將此資料存在資料庫中
        'StoreID': '', # 商店編號，正式環境下要將此資料存在資料庫中
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal, #測試交易金額，正式環境下要將此資料存在資料庫中
        'TradeDesc': 'Carol-Django 訂單測試', #自訂
        'ItemName': Title, #測試商品名稱，正式環境下要將此資料存在資料庫中
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet', #為了測試自訂
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet', #為了測試自訂
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註', #測試自訂交易備註，正式環境下要將此資料存在資料庫中
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet', #為了測試自訂
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    goodsTitle = list() # 把goodsTitle清空

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9', # 正式環境下會另外提供
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        html = format_html(html) # 格式化 html 將文字的 html 轉換為 html
        
        return render(request, 'ECPayCredit.html', locals())
    
    except Exception as error:
        print('An exception happened: ' + str(error))
    

def myorder(request):
    
    # 判斷 myMail 是否存在於 session 中
    msg = "沒有session"
    if "myMail" in request.session:
        
        # 抓取 session 的對應值
        email = request.session["myMail"]
        isalive = request.session["isAlive"]
        
        #order = models.OrdersModel.objects.filter(id=orderid)
        
        
        order = models.OrdersModel.objects.filter(customemail=email)
        if not (order == None):
            msg = "有訂單資料"
        
    return render(request, 'myorderlist.html', locals())


    
    