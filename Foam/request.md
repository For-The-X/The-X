# request
## 原理
### 网页请求方式
---
一般而言，我们所用的 HTTP 协议或 HTTPS 协议，使用的请求方式只有 GET 方式和 POST 方式。
GET 方式： 访问某个网页前不需要在浏览器里输入链接之外的东西，因为我们只是想向服务器获取一些资源，可能就是一个网页。
POST 方式：访问某个网页前需要在浏览器里输入链接之外的东西，因为这些信息是服务器需要的。 比如在线翻译，我们需要输入点英文句子，服务器才能翻译吧。


### 使用 requests 模块
---
```python
import requests
# 引入 requests，实现请求
URL = 'http://c.biancheng.net/uploads/course/python_spider/191009.html'
# 输入在浏览器的网址
res = requests.get(URL)
# 发送 GET 方式的请求，并把返回的结果(响应)存储在 res 变量里头
res.encoding = 'utf-8'
# 设置可接收的编码为 utf-8
file = open('《全身在格斗中的作用》.txt', 'a+')
# 创建一个名为《全身在格斗中的作用》的txt文档，指针放在文件末尾，追加内容。（Python 基础语法)
file.write(res.text)
# 将把 Reponse 对象的内容以 [字符串] 的形式写入文件
file.close()
# 关闭文档
```
打印结果 :
class 'requests.models.Response'

最关键的就是最后一个，Response 就是响应数据 res 的对象类型。

好，既然已经知道 res 是一个 Response 对象了，我们也就可以去了解TA的相应属性和方法了。

---
| 属性                 | 功能             | 例子                               |
| -------------------- | ---------------- | ---------------------------------- |
| Response.status_code | 检查请求是否成功 | `200` 代表正常，`404` 代表网页不存在。 |
| Response.encoding    | 定义编码         | 如果编码不对，网页就会乱码的。     |
| Response.content     | 把数据转成二进制 | 用于获取图片、音频类的数据。       |
| Response.text        | 把数据转为字符串 | 用于获取文本、网页原代码类的数据。 |


### 下载图片
---
```python
import requests
URL = 'https://gss2.bdstatic.com/9fo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike220%2C5%2C5%2C220%2C73/sign=a8ecb87e13dfa9ece9235e4503b99c66/6a600c338744ebf84073be5ddbf9d72a6059a756.jpg'
res = requests.get(URL)
# 发出请求，并把返回的结果放在变量res中
photo = open('Be careful.jpg','wb')
# 新建了一个文件Be careful.jpg，这里的文件没加路径，会被保存在程序运行的当前目录下。
photo.write(res.content)
# 将 Reponse 对象的内容以 [二进制数据] 的形式写入文件
photo.close()
# 关闭文档
```