# -*- coding: gbk -*-
from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():

    
    #cap = cv2.VideoCapture('out.mp4')
    cap = cv2.VideoCapture(0)
    
    # 获取视频帧的宽度和高度
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Load a pretrained YOLOv8n model   model = YOLO('best.pt') 
    #model = YOLO('yolov8n.pt')
    model = YOLO('best.pt')   #best.pt 模型是 自己训练的用于检测 盒子的模型。
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                break

            # 截取视频帧的左半边
            height, width, _ = frame.shape
            new_width = width // 2
            new_frame = frame[:, :new_width, :]
             # 将BGR图像转换为RGB图像  
            rgb_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)     
            # 将RGB图像输入到YOLO模型进行目标检测  
            results  = model(rgb_frame)     
            #返回的结果  results 实际上是一个长度为1个单位的 列表 ,里面有一个元素[0]              
            # 在原始帧上绘制检测到的目标框  
            #print(results) 
            #print(results[0].boxes.xyxy)
            if len(results[0].boxes.xyxy) > 0:   #这里本次推理输出几个框 这边 的长度就是几
              
              for i in range(len(results[0].boxes.xyxy)):#因此通过循环对应的次数 画框 和 写标签
                
                x1,y1,x2,y2 = results[0].boxes.xyxy[i]   #框是 张量  需要转换为数字
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                #print(x1,y1,x2,y2)
                cv2.rectangle(new_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                
  
                names = results[0].names              #这里相当于查表 获得 这个框对应的 标签是什么
                label = int(results[0].boxes.cls[i])
                class_label = names[label]
                # 在矩形框的左上角绘制类别标签
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                label_size = cv2.getTextSize(class_label, font, font_scale, font_thickness)[0]
                cv2.putText(new_frame, class_label, (x1, y1 - label_size[1]), font, font_scale, (0, 255, 0), font_thickness)
      
  
                    
            _, encoded_image = cv2.imencode('.jpg', new_frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + encoded_image.tobytes() + b'\r\n')

        except Exception as e:
            print(e)
            # 释放资源  
            cap.release()
            #out.release()
            break 

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
