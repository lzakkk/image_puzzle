import sys
import cv2
import random

def RandomFlip(img,type):
    dice = random.randrange(0,2)
    if dice==1:
        return cv2.flip(img, type)
    return img
def RandomRotation(img):
    dice = random.randrange(0,2)
    if dice==1:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img
def imgRandom(img):
    img = RandomFlip(img,0)
    img = RandomFlip(img, 1)
    img = RandomRotation(img)

    return img

if __name__ == "__main__":
    if len(sys.argv) <4:
        sys.exit("인자 [파일 이름] [열 갯수] [행 갯수] [출력 이름] 를 순서대로 넣어주세요")

    inputPath = sys.argv[1]
    col_num = int(sys.argv[2])
    row_num = int(sys.argv[3])
    outputName = sys.argv[4]

    img = cv2.imread(inputPath)
    if img is None:
        sys.exit("이미지를 찾을 수 없습니다")

    # 행,열에 맞춰서 자르기
    height,width,_ = img.shape
    height = height-height%row_num
    width = width-width%col_num
    img=img[0:height,0:width]
    print("height",height)
    print("width",width)

    print("widthNum",col_num)
    print("heightNum",row_num)
    num = col_num*row_num
    print("num",num)

    col_size = int(width/col_num)
    row_size = int(height/row_num)
    #랜덤으로 잘라서 저장
    randomList= list(range(0,num))
    random.shuffle(randomList)
    print(randomList)
    index=0
    for i in range(0,row_num):
        for j in range(0,col_num):

            y = i * row_size
            x = j * col_size
            print("x",x," y",y)
            cutImg=img[y:y+row_size,x:x+col_size]
            cutImg = imgRandom(cutImg)
            cv2.imwrite("output/"+outputName+"_"+str(randomList[index])+".png",cutImg)
            index=index+1


