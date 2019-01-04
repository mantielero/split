#!/usr/bin/env python
#!-*-coding:utf-8-*-

#from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os
import sys


# Ordenamos las líneas por cercanía a la central teórica

def gen_sort_key( mid ):
    def sort_key(data):
        Ax, Ay, Bx, By = data
        return abs(Ax-mid) + abs(Bx-mid)
    return sort_key


def split( fname="-000.png" ):
    image = cv2.imread( fname )
    mid = image.shape[1]/2.
    height = image.shape[0]
    width = image.shape[1]

    sort_key = gen_sort_key(mid)
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
    vertical_lines = []
    for i in range(a):
        Ax, Ay, Bx, By = lines[i][0]
        m = (By-Ay)/(Bx-Ax)
        ang = np.arctan(m) * 180./np.pi
        if abs(ang) > 80.:
            #cv2.line(lines_img,
            #         (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]),
            #         (255, 0, 0),
            #         3,
            #         cv2.LINE_AA)
            vertical_lines.append( (Ax*ratio,Ay*ratio, Bx*ratio,By*ratio) )
        #cv2.imwrite('',gray)

    #print("VERTICAL LINES: ",vertical_lines)
    # Si no hay líneas verticales, nos quedamos con la línea media:

    if len(vertical_lines) == 0:
        vertical_lines = [ (mid,0, mid,height) ]

    vertical_lines.sort(key=sort_key)
    #print("Sorted:", vertical_lines)

    MIN_VERTICAL_SIZE= 100

    n = len(vertical_lines)
    vlines = []
    if n >1:
        for i in range(n):
            Ax, Ay, Bx, By = vertical_lines[i]
            #print(vertical_lines[i])
            if abs( By-Ay ) > MIN_VERTICAL_SIZE:
                vlines.append(vertical_lines[i])

    #if len(vlines)
    #print("VLINES: ",vlines)
    line = vlines[0]
    #print("LINE: ", line)

    # Extendemos la línea al borde de la imagen: y = mx + b
    Ax, Ay, Bx, By = line
    _m = (By-Ay)/(Bx-Ax)
    _b = By - _m * Bx

    # y=0
    # COORDENADAS DE LA LÍNEA
    Ax = int(-_b/_m)
    Ay = int(0.)
    Bx = int( (height - _b)/_m )
    By = int(height)

    #print(Ax,Ay,Bx,By)

    # Cortamos la página
    image = cv2.imread(fname)
    Xmax = max(Ax,Bx)
    Xmin = min(Ax,Bx)
    img1 = np.copy(image[ 0:int(height), 0:Xmax ])
    img2 = np.copy(image[0:int(height), min(Ax,Bx):width ])

    p1 = [Xmax,0]
    p2 = [Xmax,int(height)]
    if Xmax == Ax:
        p3 = [Xmin,By]
    else:
        p3 = [Xmin,Ay]
    puntos = np.array([[p1,p2,p3]], dtype=np.int32)
    cv2.fillPoly(img1, pts=puntos, color=(255,255,255) )

    p1 = [Xmin-Xmin,0]
    p2 = [Xmin-Xmin,int(height)]
    if Xmax == Ax:
        p3 = [Xmax-Xmin,Ay]
    else:
        p3 = [Xmax-Xmin,By]
    puntos = np.array([[p1,p2,p3]], dtype=np.int32)
    cv2.fillPoly(img2, pts=puntos, color=(255,255,255) )

    name = os.path.splitext(fname)[0]
    #print('%s_0.png' % name)
    cv2.imwrite('%s_0.png' % name, img1)
    cv2.imwrite('%s_1.png' % name, img2)

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
    split(name)
