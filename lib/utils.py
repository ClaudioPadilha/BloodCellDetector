import matplotlib.image as mpimg
import json
import numpy as np

def crop_image_label (imgFile : str, labelFile : str, threshold : int) -> tuple:
    
    im = mpimg.imread(imgFile)

    X, Y, C = im.shape

    slice = im.sum(axis=2)[X // 2]

    for i in range(100, Y // 2):
        if slice[i] > 100:
            ystart = i
            break
    for i in range(Y - 100, Y // 2, -1):
        if slice[i] > 100:
            yend = i
            break
    Dy = yend - ystart

    with open(labelFile, 'rt') as f:
        labels = json.load(f)

    stop = False
    i = 0
    labelsList = []

    while (not stop):
        try:
            label = labels[f'Cell_{i}']
            xi = int(label['x1'])
            xf = int(label['x2'])
            yi = int(label['y1'])
            yf = int(label['y2'])
            dx = xf - xi
            dy = yf - yi


            l1, l2 = label['Label1'], label['Label2'] 
            try:
                l =  l1 + ' | ' + l2 if l1 != l2 else l1
            except TypeError:
                l = l1 if l1 is not None else l2

            xi = xi + dx // 3 - ystart
            yi = yi + dy // 3
            dx = dx // 3
            dy = dy // 3
            labelsList.append([l, xi, yi, dx, dy])
            # rect = patches.Rectangle((xi + dx // 3, yi + dy // 3), dx // 3, dy // 3, linewidth=2, edgecolor='b', facecolor='none')
            # ax[0].add_patch(rect)
            # ax[0].text(xi + dx // 3, yi + dy // 3, l)

            i += 1
        except KeyError as e:
            stop = True

    return (im[:,ystart:yend,:], labelsList)
