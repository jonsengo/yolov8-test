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
    
    # ��ȡ��Ƶ֡�Ŀ��Ⱥ͸߶�
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Load a pretrained YOLOv8n model   model = YOLO('best.pt') 
    #model = YOLO('yolov8n.pt')
    model = YOLO('best.pt')   #best.pt ģ���� �Լ�ѵ�������ڼ�� ���ӵ�ģ�͡�
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                break

            # ��ȡ��Ƶ֡������
            height, width, _ = frame.shape
            new_width = width // 2
            new_frame = frame[:, :new_width, :]
             # ��BGRͼ��ת��ΪRGBͼ��  
            rgb_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)     
            # ��RGBͼ�����뵽YOLOģ�ͽ���Ŀ����  
            results  = model(rgb_frame)     
            #���صĽ��  results ʵ������һ������Ϊ1����λ�� �б� ,������һ��Ԫ��[0]              
            # ��ԭʼ֡�ϻ��Ƽ�⵽��Ŀ���  
            #print(results) 
            #print(results[0].boxes.xyxy)
            if len(results[0].boxes.xyxy) > 0:   #���ﱾ��������������� ��� �ĳ��Ⱦ��Ǽ�
              
              for i in range(len(results[0].boxes.xyxy)):#���ͨ��ѭ����Ӧ�Ĵ��� ���� �� д��ǩ
                
                x1,y1,x2,y2 = results[0].boxes.xyxy[i]   #���� ����  ��Ҫת��Ϊ����
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                #print(x1,y1,x2,y2)
                cv2.rectangle(new_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                
  
                names = results[0].names              #�����൱�ڲ�� ��� ������Ӧ�� ��ǩ��ʲô
                label = int(results[0].boxes.cls[i])
                class_label = names[label]
                # �ھ��ο�����Ͻǻ�������ǩ
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
            # �ͷ���Դ  
            cap.release()
            #out.release()
            break 

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)