import cv2


def get_image():
    retval, im = camera.read()
    return im


def take_picture():
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    for i in range(ramp_frames):
        temp = get_image()
    camera_capture = get_image()
    file = "image_upload.png"
    cv2.imwrite(file, camera_capture)
    del(camera)
