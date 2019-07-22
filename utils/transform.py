import cv2
import torch
from PIL import Image
import torchvision.transforms.functional as TF


def transform(img_array, input_size):
    """

    :param img_array:
    :param input_size:
    :return:
    """
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img_array)

    width, height = img.size
    img = TF.resize(img, int(height / width * input_size))  # the smaller edge will be matched to input_size
    img = TF.pad(img, (0, int((img.size[0] - img.size[1]) / 2)))

    tensor = TF.to_tensor(img)
    tensor = TF.normalize(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    return tensor


def stack_tensors(tensors):
    stacked = torch.stack(tensors)
    return stacked


def preds_postprocess(preds, stream_names, frame_shape, img_size, classes):
    # The amount of padding that was added
    pad_x = max(frame_shape[0] - frame_shape[1], 0) * \
            (img_size / max(frame_shape))
    pad_y = max(frame_shape[1] - frame_shape[0], 0) * \
            (img_size / max(frame_shape))
    # Image height and width after padding is removed
    unpad_h = img_size - pad_y
    unpad_w = img_size - pad_x

    preds_dict = {}
    person_bboxes = []
    for i, pred in enumerate(preds):
        if pred is None:
            preds_dict[stream_names[i]] = None
        else:
            for *xyxy, conf, cls_conf, cls_pred in pred:
                if classes[int(cls_pred)] == 'person':  # 只检测人
                    # Rescale coordinates to original dimensions
                    box_h = ((xyxy[3] - xyxy[1]) / unpad_h) * frame_shape[0]
                    box_w = ((xyxy[2] - xyxy[0]) / unpad_w) * frame_shape[1]
                    y1 = ((xyxy[1] - pad_y // 2) / unpad_h) * frame_shape[0]
                    x1 = ((xyxy[0] - pad_x // 2) / unpad_w) * frame_shape[1]

                    person_bbox = (x1, y1, x1 + box_w, y1 + box_h)
                    person_bboxes.append(person_bbox)
            preds_dict[stream_names[i]] = person_bboxes

    return preds_dict
