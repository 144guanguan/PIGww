import requests
import simplejson
import json
import base64
from PIL import Image

# Face++的key和secret
# https://console.faceplusplus.com.cn/app/apikey/list
key = "WV2eIYImXLWOemZ1o_5ZTOlXvsS2wa2p"
secret = "G2JjsMnlDWbeO7z13R5L9PFk_7nCyf9D"

# 获取人脸关键点
def find_face(imgpath):
    # 测试是否进入函数
    # print("finding")

    # 调用所需要的基本数据
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": key,"api_secret": secret, "image_url": imgpath, "return_landmark": 1}
    files = {"image_file": open(imgpath, "rb")}

    # 调用URL，上传图片，调用API,调用方法：post
    # 返回值是一个json字符串
    response = requests.post(http_url, data=data, files=files)

    # 获取需要的数据
    # 编码类型
    req_con = response.content.decode('utf-8')
    # 从JSON对象解码数据类型实例的对象。
    req_dict = json.JSONDecoder().decode(req_con)

    # dumps是将json格式的数据(字典或字典组成的列表)转换成json字符串。
    this_json = simplejson.dumps(req_dict)
    # loads是将json字符串直接转换成Python数据类型。
    this_json2 = simplejson.loads(this_json)

    # 'faces'被检测出的人脸数组
    faces = this_json2['faces']
    list0 = faces[0]
    # 人脸矩形框的位置
    rectangle = list0['face_rectangle']

    # 测试用
    # print(rectangle)

    return rectangle

# 对人脸范围进行绘制框图
def show_face_rectangle(imgpath):
    im = Image.open(imgpath)
    # 获取人脸关键值
    rec = find_face(imgpath)

    im_new = im.copy()
    width, height = im_new.size
    # 绘制矩形框
    for i in range(width):
        if i >= rec['left'] and i <= (rec['left'] + rec['width']):
            im_new.putpixel((i, rec['top']), (255, 0, 0))
            im_new.putpixel((i, (rec['top']+rec['height'])), (255, 0, 0))
    for i in range(height):
        if i >= rec['top'] and i <= (rec['top'] + rec['height']):
            im_new.putpixel((rec['left'], i), (255, 0, 0))
            im_new.putpixel(((rec['left']+rec['width']), i), (255, 0, 0))

    im_new.show()

# 显示无范围框图像
def show_face_just(imgpath):
    im = Image.open(imgpath)
    im.show()

# number表示换脸的相似度
def merge_face(image_url_1, image_url_2, image_url, number):
    # 获取两个图像的人脸矩形框的位置
    ff1 = find_face(image_url_1)
    ff2 = find_face(image_url_2)
    # 将得到的位置信息（整型）重新组成字符串类型，以便于转换成json上传到face++进行merge
    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])

    # 测试用
    # print(rectangle1)
    # print(rectangle2)

    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"

    # 对两张图片的地址进行编码处理，以便于上传到face++调用相应的api
    # image1
    f1 = open(image_url_1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    # image2
    f2 = open(image_url_2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()
    # 根据使用文档整理出所需要上传到信息
    data = {"api_key": key, "api_secret": secret,
            "template_base64": f1_64, "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}

    # 调用URL，上传图片，调用API,调用方法：post
    response = requests.post(url_add, data=data)

    # 将调用API后返回的json字符串进行编码操作
    req_con = response.content.decode('utf-8')
    # # 从JSON对象解码数据类型实例的对象。
    req_dict = json.JSONDecoder().decode(req_con)

    result = req_dict['result']
    # 进行编码
    imgdata = base64.b64decode(result)

    # 对结果图像进行信息写入、保存和关闭操作
    file = open(image_url, 'wb')
    # 重新写入信息
    file.write(imgdata)
    file.close()

# 主函数
def test():

    # 保留背景的图像
    image2 = r"D:\PIGww\img\test_img\gxt.jpg"
    # 保留脸部信息的图像
    image1 = r"D:\PIGww\img\test_img\xz.jpg"
    # 换脸结果图
    image = r"D:\PIGww\img\result.jpg"

    # 调用merge_face()进行融合操作 merge_face(保留背景的图像, 保留脸部信息的图像, 结果图像, 合成度（1~100）)
    merge_face(image2, image1, image, 70)

    # 调用show_face()显示出三幅图像并且框出人脸部分
    # show_face_rectangle(image2)
    # show_face_rectangle(image1)
    # show_face_rectangle(image)

    # 显示没有范围框的图像
    # show_face_just(image2)
    # show_face_just(image1)
    show_face_just(image)