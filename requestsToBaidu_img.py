import requests, os, re

for page in range(0, 100, 20):
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=孙俪&pn=' + str(page) + \
      '&ic=0&lm=-1&width=&height=&v=flip'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    os.makedirs('D:\\img', exist_ok=True)

    print('Downloading page %s...' % url)
    response = requests.get(url, headers=header)
    response.raise_for_status()
    response.encoding = 'utf-8'
    soup = response.text
    #print(soup)
    srcReg = re.compile(r'(http:[^\s]+?(jpg))', re.I)
    src = srcReg.findall(soup)
    for n in range(20):
        if src is None:
            print("Noen")
        else:
            srcUrl = src[n][0]
            print('正在下载：', srcUrl)
            try:
                response = requests.get(srcUrl, headers=header, timeout=5)
            except requests.exceptions.ConnectionError:
                print("这条连接无效：", srcUrl)
            imageFile = open(os.path.join('D:\\img', os.path.basename(srcUrl)), 'wb')
            for chunk in response.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()


print("done")

