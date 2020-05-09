import matplotlib.pyplot as plt
import numpy as np
import cv2
import io


def fig2img(fig, dpi=180):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    buf.close()
    img = cv2.imdecode(img_arr, 1)
    return img


data = {'2020-05-04': 2, '2020-05-05': 10, '2020-05-06': 0, '2020-05-07': 7}
names = list(data.keys())
values = list(data.values())

fig, ax = plt.subplots()
ax.bar(names, values)
ax.set_facecolor("darkgray")

img = fig2img(fig, 100)
cv2.imshow('', img)
cv2.waitKey(0)



