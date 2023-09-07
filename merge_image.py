import sys
import cv2
import os
import numpy as np
class Piece:
    Top = None
    Right = None
    Bottom = None
    Left = None
    img = None

    def __init__(self, img):
        self.img = img


def target_rotate(desc,src,img):
    if desc ==src:
        return img
    target_index=locate_map.index(src)
    desc_index = locate_map.index(desc)
    rotate_index=desc_index-target_index
    while rotate_index!=0:
        if rotate_index >0:
            img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

            rotate_index-=1
        if rotate_index <0:

            img=cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
            rotate_index+=1

    return img
locate_array=['top','right','bottom','left','top','right','bottom','left']


locate_map=['top','right','bottom','left']
def compare_edge(line, img_edge_list):
    compare_edge_list = [compare_line(line, edge) for edge in img_edge_list]
    return compare_edge_list


def compare_line(line1, line2):
    if line1.shape != line2.shape:
        return 9999999

    sum = np.sum(np.abs(np.array(line1,np.int32) - np.array(line2,np.int32))) / line1.shape
    return sum


def img_edge(img):
    copy_img = img.copy()
    copy_img = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
    top = copy_img[0, :].flatten()
    bottom = np.flip(copy_img[-1:, :].flatten())
    left = np.flip(copy_img[:, 0].flatten())
    right = copy_img[:, -1:].flatten()
    return top, right, bottom, left, np.flip(top), np.flip(right), np.flip(bottom), np.flip(left)
def img_edge2(img):
    copy_img = img.copy()
    copy_img = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
    top = copy_img[1, :].flatten()
    bottom = np.flip(copy_img[-2:-1, :].flatten())
    left = np.flip(copy_img[:, 1].flatten())
    right = copy_img[:, -2:-1].flatten()
    return top, right, bottom, left, np.flip(top), np.flip(right), np.flip(bottom), np.flip(left)

def find_img(img_list, line,cut):
    compare_list=[]
    for idx, img in enumerate(img_list):
        edges = list(img_edge(img))
        compare_edge_list = compare_edge(line,edges)
        compare_list.append(compare_edge_list)


    if len(compare_list)==0:
        return None
    score=min([min(compare) for compare in compare_list])
    img_index=0
    line_index=0
    for idx, compare in enumerate(compare_list):
        if score in compare:
            line_index=compare.index(score)
            img_index=idx

    if score <5+cut:
        return [img_list[img_index], line_index,img_index]
    return None


def fill(piece, img_list):
    top, right, bottom, left, _, _, _, _ = img_edge(piece.img)
    top2, right2, bottom2, left2, _, _, _, _ = img_edge2(piece.img)

    if piece.Top is None:
        cut = compare_line(top,top2)
        result = find_img(img_list, top,cut)
        if not result is None:

            target_img, line_index,img_idx = result
            target_img = target_rotate('bottom',locate_array[line_index],target_img)
            if line_index < 4:
                target_img = cv2.flip(target_img, 1)

            del img_list[img_idx]


            next_piece=Piece(target_img)
            piece.Top=next_piece
            next_piece.Bottom=piece
            fill(next_piece,img_list)
    if piece.Right is None:
        cut = compare_line(right,right2)
        result = find_img(img_list, right,cut)
        if not result is None:


            target_img, line_index,img_idx = result
            target_img = target_rotate('left',locate_array[line_index],target_img)
            if line_index < 4:
                target_img = cv2.flip(target_img, 0)


            del img_list[img_idx]


            next_piece=Piece(target_img)
            piece.Right=next_piece
            next_piece.Left=piece
            fill(next_piece,img_list)
    if piece.Bottom is None:
        cut = compare_line(bottom,bottom2)
        result = find_img(img_list, bottom,cut)
        if not result is None:

            target_img, line_index,img_idx = result
            target_img = target_rotate('top',locate_array[line_index],target_img)
            if line_index < 4:
                target_img = cv2.flip(target_img, 1)

            del img_list[img_idx]


            next_piece=Piece(target_img)
            piece.Bottom=next_piece
            next_piece.Top=piece
            fill(next_piece,img_list)

    if piece.Left is None:
        cut = compare_line(left,left2)
        result = find_img(img_list, left,cut)
        if not result is None:

            target_img, line_index,img_idx = result
            target_img = target_rotate('right',locate_array[line_index],target_img)
            if line_index < 4:
                target_img = cv2.flip(target_img, 0)

            del img_list[img_idx]


            next_piece=Piece(target_img)
            piece.Left=next_piece
            next_piece.Right=piece
            fill(next_piece,img_list)



def fill_img(piece,x,y,locate_list):
    locate_list.append([x,y,piece.img])

    if not piece.Top is None:
        next_piece = piece.Top
        next_piece.Bottom=None
        fill_img(next_piece,x,y-1,locate_list)
    if not piece.Bottom is None:
        next_piece = piece.Bottom
        next_piece.Top = None
        fill_img(next_piece, x, y +1, locate_list)
    if not piece.Left is None:
        next_piece = piece.Left
        next_piece.Right = None
        fill_img(next_piece, x-1, y, locate_list)
    if not piece.Right is None:
        next_piece = piece.Right
        next_piece.Left = None
        fill_img(next_piece, x+1, y, locate_list)


if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit("인자 [파일 이름] 를 순서대로 넣어주세요")

    inputPath = sys.argv[1]

    path = "output/"
    file_list = os.listdir(path)
    img_name_list = [file for file in file_list if file.startswith(inputPath)]
    img_name_list.sort()

    img_list = [cv2.imread("output/" + img_name) for img_name in
                img_name_list]
    sample_img = img_list[0]
    for idx, img in enumerate(img_list):
        if img.shape != sample_img.shape:
            img_list[idx] = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    start = Piece(img_list[0])
    del img_list[0]
    fill(start,img_list)

    locate_list=[]
    fill_img(start,0,0,locate_list)

    min_x=0
    max_x=0
    min_y=0
    max_y=0

    for locate in locate_list:
        min_x=min([min_x,locate[0]])
        min_y=min([min_y,locate[1]])
        max_x=max([max_x,locate[0]])
        max_y=max([max_y,locate[1]])

    max_x-=min_x
    max_y -= min_y

    locate_list=[[locate[0]-min_x,locate[1]-min_y,locate[2]] for locate in locate_list]

    height, width,_ = sample_img.shape
    sum_img=np.zeros((height*(max_y+1),width*(max_x+1),3),dtype='uint8')

    for locate in locate_list:
        x,y,img=locate
        fil=sum_img[height*y:height*(y+1),width*x:width*(x+1)]
        sum_img[height*y:height*(y+1),width*x:width*(x+1),:]=img[:,:,:]
    cv2.imwrite('result.png',sum_img)


