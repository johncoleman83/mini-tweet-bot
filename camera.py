import cv2


def take_picture():
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    for i in range(ramp_frames):
        temp = camera.read()[1]
    while True:
        img = camera.read()[1]
        if img is not None:
            break
    file = "./uploads/image_upload.png"
    cv2.imwrite(file, img)
    del(camera)
    return file
