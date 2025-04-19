import os
import sys
import argparse
import glob
import time
import cv2
import numpy as np
from ultralytics import YOLO

# Hardcoded model path
model_path = "C:\\Users\\User\\Desktop\\IDP\\my_model\\my_model.pt"  # Replace with your actual path

parser = argparse.ArgumentParser()
parser.add_argument('--source', default='webcam', help='Source: "test.jpg", "test_dir", "testvid.mp4", "webcam"')
parser.add_argument('--thresh', default=0.5, help='Minimum confidence threshold')
parser.add_argument('--resolution', default=None, help='Resolution WxH')
parser.add_argument('--record', action='store_true', help='Record video output')

args = parser.parse_args()
img_source = args.source
min_thresh = float(args.thresh)
user_res = args.resolution
record = args.record

if not os.path.exists(model_path):
    print('ERROR: Model not found.')
    sys.exit(0)

model = YOLO(model_path, task='detect')
labels = model.names

resize = False
if user_res:
    resize = True
    resW, resH = map(int, user_res.split('x'))

if record and not user_res:
    print('Specify resolution to record.'); sys.exit(0)
if record:
    recorder = cv2.VideoWriter('demo1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

cap = cv2.VideoCapture(0)  # Use the default webcam
if user_res:
    cap.set(3, resW)
    cap.set(4, resH)

bbox_colors = [(164,120,87), (68,148,228), (93,97,209), (178,182,133)]

while True:
    ret, frame = cap.read()
    if not ret:
        print('No frame read, exiting.'); break
    
    if resize:
        frame = cv2.resize(frame, (resW, resH))
    
    results = model(frame, verbose=False)
    detections = results[0].boxes
    
    for i in range(len(detections)):
        xyxy = detections[i].xyxy.cpu().numpy().astype(int).squeeze()
        classidx = int(detections[i].cls.item())
        classname = labels[classidx]
        conf = detections[i].conf.item()

        if conf > min_thresh:
            color = bbox_colors[classidx % len(bbox_colors)]
            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
            cv2.putText(frame, f'{classname}: {int(conf*100)}%', (xyxy[0], xyxy[1]-7),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    cv2.imshow('YOLO Detection', frame)
    if record: recorder.write(frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
