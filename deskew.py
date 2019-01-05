#!/usr/bin/env python
#!-*-coding:utf-8-*-

#from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os
import sys
from PIL import Image

# Ordenamos las líneas por cercanía a la central teórica

def gen_sort_key( mid ):
    def sort_key(data):
        Ax, Ay, Bx, By = data
        return abs(Ax-mid) + abs(Bx-mid)
    return sort_key


def deskew( fname="-000.png" ):
    #print("Deskewing: ", fname)
    image = cv2.imread( fname )
    mid = image.shape[1]/2.
    height = image.shape[0]
    width = image.shape[1]

    #sort_key = gen_sort_key(mid)
    #print("Shape: ", image.shape)  # h,w,RGB
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height = 500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    minLineLength=100
    lines = cv2.HoughLinesP( image=edged
                           , rho=1
                           , theta=np.pi/180
                           , threshold=100
                           , lines=np.array([])
                           , minLineLength=minLineLength
                           , maxLineGap=80)

    a,b,c = lines.shape
    #horizontal_lines = []
    angs = []
    #lines_img = np.copy(image)
    for i in range(a):
        Ax, Ay, Bx, By = lines[i][0]
        if (Bx - Ax) > 0.0001:
            m = (By-Ay)/(Bx-Ax)
            ang = np.arctan(m) * 180./np.pi
            #print(ang)
            if abs(ang) < 15.:
                #cv2.line(lines_img,
                #         (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
                #         (255, 0, 0),
                #         3,
                #         cv2.LINE_AA)
                #horizontal_lines.append( (Ax*ratio,Ay*ratio, Bx*ratio,By*ratio) )
                #if ang != 0.0:
                angs.append( ang )
        #cv2.imwrite('',gray)
    #cv2.imshow( "Lines: ", lines_img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    if len(angs) == 0:
        angs = [0.0]

    ang = np.mean( angs)
    im = Image.open(fname)
    #im.show()
    #print("ANG: ", ang)
    if abs(ang) > 0.1:
        new = im.rotate(ang)
        new.save(fname)
    #print(ang)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Detects the center line to split a page')
    parser.add_argument( 'infile', nargs='?', type=argparse.FileType('r'),
                         default=sys.stdin )
    #parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                   help='an integer for the accumulator')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                   const=sum, default=max,
    #                   help='sum the integers (default: find the max)')
    args = parser.parse_args()

    name = args.infile.name
    args.infile.close()
    deskew(name)
