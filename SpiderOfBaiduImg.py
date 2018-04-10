import requests, os, re

i = 0
wd = input('请输入关键字:')
num = int(input('请输入下载数量：'))
path = 'D:\\img\\%s' % wd

for page in range(0, num, 20):

    # 准备好url和请求头
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + str(wd) + '&pn=' + str(page) +'&ic=0&lm=-1&width=&height=&v=flip'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

    # 将文件保存在以关键字命名的文件夹，如果不存在就新建一个
    os.makedirs('D:\\img\\%s' % wd, exist_ok=True)

    # get方法获得网页内容并通过正则筛选图片链接
    response = requests.get(url, headers=header)
    imgReg = re.compile(r'(http:[^\s]+?(jpg))', re.I)
    img = imgReg.findall(response.text)
    for n in range(len(img)):
        imgUrl = img[n][0]

        # 判断下载数量是否达到需求
        if i == num:
            break
        else:

            # 处理无效链接或响应超时引发的异常
            try:
                response = requests.get(imgUrl, headers=header, timeout=5)
            except requests.exceptions.ConnectionError:
                print("这条链接无效：", imgUrl)
                continue
            except requests.exceptions.ReadTimeout:
                print("这条链接超时：", imgUrl)
                continue

            # 打印当前下载进度
            i = i + 1
            print('正在下载第%s条' % i, imgUrl)

            # 保存并通过命名去重
            imageFile = open(os.path.join(path, os.path.basename(imgUrl)), 'wb')
            imageFile.write(response.content)  # response.content以字节形式写入
            imageFile.close()

print("搞定啦！共下载%s张图片。" % i)
