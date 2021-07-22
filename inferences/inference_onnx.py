import numpy as np
import time
import cv2
import onnxruntime as ort


IMAGE_PATH = '/home/jetsonmapinai/Documents/AI Visual Inspection/dummy.png'
MODEL_PATH = '../models/TF220_centernet_inference_graph_1.onnx'

sess = ort.InferenceSession(MODEL_PATH)


def do_detect(image):
    # image = clahein(clahe)
    class_name = ["BG", "Keropos", "Kurokawa", "Dakon", "Scratch", "Hole", "D78", "Scratch_OK", "Water_Droplet",
                  "Ketsuniku", "Keropos_Casting", "Step", "PartingLine", "Karat"]
    ori = image.copy()
    image_onnx = np.expand_dims(image, 0)
    detections = sess.run(["detection_boxes", "detection_scores", "detection_classes"], {'input_tensor': image_onnx})
    boxes = detections[0][0]
    scores = detections[1][0]
    classes = detections[2][0].astype(int)
    cls_det = []
    bbox = []
    for i in range(len(boxes)):
        kelas = classes[i]
        if (scores[i] >= 0.2 and classes[i] == 1) or \
                scores[i] >= 0.3 and classes[i] == 2 or \
                scores[i] >= 0.3 and classes[i] == 3 or \
                scores[i] >= 0.5 and classes[i] == 4 or \
                scores[i] >= 0.3 and classes[i] == 9 or \
                scores[i] >= 0.3 and classes[i] == 10 or \
                scores[i] >= 0.3 and classes[i] == 11 or \
                scores[i] >= 0.3 and classes[i] == 12:
            box = boxes[i] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
            image = cv2.rectangle(image, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0, 0, 255), 2)
            image = cv2.putText(image, '%s %.2f' % (class_name[int(classes[i])], scores[i]),
                                (int(box[1]) - 10, int(box[0]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))
            cls_det.append(class_name[kelas])
            bbox.append(box)
    return ori, image, cls_det, bbox


def clahein(image):
    gridsize = 8
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(gridsize, gridsize))
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr


def warmup():
    dummy = cv2.imread(IMAGE_PATH)
    do_detect(dummy)


def main():
    test_image = r'C:\Users\s.hasanuddin.syukril\Downloads\OK-8-7-21\part 10005\sect 4\37.png'
    dummy = cv2.imread(test_image)
    __, image, __, __ = do_detect(dummy)
    cv2.imshow('result', image)
    print("-------------------------------------")
    print("PRESS 'ESC' TO PERFORM BENCHMARK TEST WHEN IMAGE APPEARS AND IS IN FOCUS")
    print("-------------------------------------")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    num_samples = 3
    t0 = time.time()
    for i in range(int(num_samples)):
        t2 = time.time()
        do_detect(image)
        print('%f [sec]' % (time.time() - t2))
    t1 = time.time()
    print('Average runtime: %f seconds' % (float(t1 - t0) / num_samples))


if __name__ == '__main__':
    main()
