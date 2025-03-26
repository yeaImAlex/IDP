import cv2
import os
import argparse
import sys

#parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--imgdir',default='Pics')
parser.add_argument('--resolution', default = '1440x12800')
args = parser.parse_args()

#validate resolution input
dirname = args.imgdir
if not 'x' in args.resolution:
    print('please specify resolution as WxH.(example: 1920x1080)')
    sys.exit()
imW = int (args.resolution.split('x')[0])
imH = int (args.resolution.split('x')[1])

#create img save directory
cwd = os.getcwd()
dirpath = os.path.join(cwd, dirname)
if not os.path.exists(dirpath):
    os.makedirs(dirpath)

#avoid overwriting existing images
basename = dirname
imnum = 1
img_exists = True

while img_exists:
    imname = dirname + '_' + str(imnum) + '.jpg'
    impath = os.path.join(dirpath,imname)
    if os.path.exists(impath):
        imnum = imnum + 1
    else:
        img_exists = False

#initialize webcam & set resolution
cap = cv2.VideoCapture(1)
ret = cap.set(3, imW)
ret = cap.set(4, imH)

#create a display window
winname = 'Press "p" to take pic'
cv2.namedWindow(winname)
cv2.moveWindow(winname,50,30)

#print user instruction
print('Press p to take a picture. Pictures will automatically be saved in the %s folder.' % dirname)
print('Press q to quit.')

#capture & display webcam feed
while True:
    hasFrame, frame = cap.read()
    cv2.imshow(winname, frame)

    #handle user input for taking pic/exiting
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('p'):
        #take pic
        filename = dirname + '_' + str(imnum) + '.jpg'
        savepath = os.path.join(dirpath, filename)
        cv2.imwrite(savepath, frame)
        print('Pic taken and saved as %s' %filename)
        imnum = imnum + 1

cv2.destroyAllWindows()
cap.release()

