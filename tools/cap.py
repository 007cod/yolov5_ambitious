from PIL import Image
import cv2
import imageio


def get_cap(path):
    """ 读取视频和模型初始化predictor """
    if isinstance(path, str):
        cap = imageio.get_reader(path, 'ffmpeg')
    else:
        cap = cv2.VideoCapture(path)  # 视频流
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))  #读取视频格式
        # 设置分辨率
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
    return cap