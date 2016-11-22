from sklearn.externals import joblib
from sklearn import datasets
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter

# Загружаем данные
dataset = datasets.fetch_mldata("MNIST Original")

# делаем массивы numpy
features = np.array(dataset.data, 'int16') 
labels = np.array(dataset.target, 'int')

# используем hog
list_hog_fd = []
for feature in features:
    fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    list_hog_fd.append(fd)
hog_features = np.array(list_hog_fd, 'float64')

print("Count of digits in dataset", Counter(labels))

# Создаем SVM обьект
clf = LinearSVC()

# Запускаем тренировку
clf.fit(hog_features, labels)

# Сохраняем классификатор
joblib.dump(clf, "digits_cls.pkl", compress=3)