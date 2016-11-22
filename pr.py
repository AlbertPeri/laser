# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

def recognite(frame, tre, n = 10):
    # Загружаем классификатор
    clf = joblib.load("digits_cls.pkl")

    # Берем картинку 
    im = frame

    # Делаем картинку серой и сглаживаем
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

    # Делаем все черно белым
    if tre:
        ret, im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)
    else:
        im_th = im_gray

    # Находим котуры
    ret, ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Получаем прямоугольники из кажого контура
    rects = [cv2.boundingRect(ctr) for ctr in ctrs]
    print(rects)

    am =[] 
    # используем HOG и SVM алгоритм для распознования
    for rect in rects:
        if abs(rect[2]-rect[3]) < n: continue
        # Рисуем прямоугольники вокруг цифр
        cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 3) 
        # создаем регионы в прямоугольниках
        leng = int(rect[3] * 1.6)
        pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
        pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
        roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
        # Изменяем размеры изображения
        try:
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
        except:
            continue
        roi = cv2.dilate(roi, (3, 3))
        # вычисляем HOG
        roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
        nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
        am.append(nbr[0])
        cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)

    return im

if __name__ == '__main__':
    im = cv2.imread("m2.png")
    im = recognite(im,1)
    cv2.imshow("Result", im)
    cv2.waitKey()