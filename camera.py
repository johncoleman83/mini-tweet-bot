import cv2


def take_picture():
    camera_port = 0
    ramp_frames = 20
    camera = cv2.VideoCapture(camera_port)
    for i in range(ramp_frames):
        temp = camera.read()[1]
    camera_capture = camera.read()[1]
    file = "./uploads/image_upload.png"
    cv2.imwrite(file, camera_capture)
    del(camera)
    return file
