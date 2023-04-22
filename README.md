
# 智安检-基于X光的智能安检违禁品分拣系统

---

### 安装说明

我们支持 ```python3.6```环境，可以通过以下代码安装运行所需环境:
```
pip install -r requirements.txt
```

### 运行说明

因为代码运行需要安检机提供实时影像
这里我们提供了一个依赖该目录下```1.mp4```文件运行的demo，可以使用以下指令运行:
```
python demo-paddle.py
```

在安检机提供实时影像的情况下可以使用以下指令运行：

```
python demo.py
```

运行结果将在网页```127.0.0.1:5050```中实时呈现

---

### 开源代码与组件使用情况说明

##### 项目名称：YOLOv5 TensorRT Demo

版本号：v1.0

开源许可证类型：```Apache License 2.0（TensorRT Demo）```、```MIT License（YOLOv5）```

开源代码和组件来源：
```
YOLOv5：https://github.com/ultralytics/yolov5/releases/tag/v7.0
TensorRT Demo：https://github.com/wang-xinyu/tensorrtx/tree/master/yolov5
```

使用的版本号：
```
YOLOv5：v7.0
TensorRT：7.2.2
```
修改和补丁：本项目没有对使用的开源代码和组件进行任何修改和补丁。

依赖关系：TensorRT Demo依赖于```TensorRT C++ API```和```OpenCV```库。YOLOv5依赖于```PyTorch```深度学习框架、```NumPy```库和```Pillow```库。请确保正确安装这些依赖项后再运行本项目。

作者和贡献者：
```
YOLOv5：Ultralytics公司
TensorRT Demo：wang xinyu
```

安全性和漏洞：本项目未发现任何安全问题或漏洞。如需更新YOLOv5的预训练模型，请参考[YOLOv5的官方网站](https://github.com/ultralytics/yolov5)和[GitHub页面](https://github.com/ultralytics/yolov5/releases/tag/v7.0)。

---
##### 项目名称：YOLOv5

版本号：
```
YOLOv5: v7.0
```

开源许可证类型：```MIT License```

开源代码和组件来源：
```
https://github.com/ultralytics/yolov5/releases/tag/v7.0
```

使用的版本号：```v7.0```

修改和补丁：本项目没有对使用的开源代码和组件进行任何修改和补丁。

依赖关系：YOLOv5依赖于```PyTorch```深度学习框架、```NumPy```库和```Pillow```库。请确保正确安装这些依赖项后再使用本项目。

作者和贡献者：
```
YOLOv5由Ultralytics公司开发。
```
安全性和漏洞：本项目未发现任何安全问题或漏洞。
