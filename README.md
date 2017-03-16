# 验证码识别程序
程序启动一个server来监听验证码图片buffer, 用来识别验证码(主要是amazon)， 30%左右成功率
# REQUIREMENT
- tesseract ocr
```
sudo apt-get install -y tesseract-ocr
```
- pil
```
sudo apt-get install -y  libjpeg8-dev zlib1g-dev    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
```
- python
```
sudo pip install -r requirements.txt
```
# START
```
git clone 
python captcha_monitor.py
```

# USAGE
```
usage: captcha_monitor.py [-h] [-s SETTINGS] [-d]
                          [{stop,start,restart,status}]

positional arguments:
  {stop,start,restart,status}

optional arguments:
  -h, --help            show this help message and exit
  -s SETTINGS, --settings SETTINGS
  -d, --daemon

```
配合scrapy验证码中间件使用
