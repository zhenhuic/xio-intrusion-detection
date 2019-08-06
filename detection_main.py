import time
import torch
import cv2

from models import Darknet
from visualize import Visualize
from opc_client import OpcClient
from video_stream import initialize_video_streams, capture_one_frame
from utils.utils import non_max_suppression, load_classes, calc_fps
from utils.transform import transform, stack_tensors, preds_postprocess
from intrusion_handling import IntrusionHandling
from config.config import opc_url, nodes_dict, video_stream_paths_dict, switch_mask, \
    vis_name, frame_shape, masks_paths_dict


def get_model(config_path, img_size, weights_path, device):
    model = Darknet(config_path, img_size=img_size)
    model.load_weights(weights_path)

    model = model.to(device)
    model.eval()  # Set in evaluation mode
    return model


def inference(model, input_tensor, device, num_classes, conf_thres, nms_thres):
    input_tensor = input_tensor.to(device)
    output = model(input_tensor)
    preds = non_max_suppression(output, num_classes, conf_thres, nms_thres)
    return preds


@torch.no_grad()
def main(args):
    device = torch.device(args.device)
    model = get_model(args.config_path, args.img_size, args.weights_path, device)

    if args.open_opc:
        opc_client = OpcClient(opc_url, nodes_dict)
    else:
        opc_client = None

    video_streams_dict = initialize_video_streams(list(video_stream_paths_dict.values()),
                                                  list(video_stream_paths_dict.keys()),
                                                  switch_mask=switch_mask)
    visualize = Visualize(masks_paths_dict)
    handling = IntrusionHandling(masks_paths_dict, opc_client)

    # for calculating inference fps
    since = time.time()
    accum_time, curr_fps = 0, 0
    show_fps = 'FPS: ??'

    exception_flag = False
    while not exception_flag:
        # prepare frame tensors before inference
        frames_dict = capture_one_frame(video_streams_dict)
        input_tensor = []
        for name in frames_dict.keys():
            tensor = transform(frames_dict[name], args.img_size)
            input_tensor.append(tensor)
        input_tensor = stack_tensors(input_tensor)

        # model inference and postprocess
        preds = inference(model, input_tensor, device, 80, args.conf_thres, args.nms_thres)
        classes = load_classes(args.class_path)  # Extracts class labels from file
        preds_dict = preds_postprocess(preds, list(video_stream_paths_dict.keys()),
                                       frame_shape, args.img_size, classes)

        # judge whether someone breaks into
        judgements_dict = handling.judge_intrusion(preds_dict)

        # calculate inference fps
        since, accum_time, curr_fps, show_fps = calc_fps(since, accum_time, curr_fps, show_fps)
        print(show_fps)

        # visualize detection results
        vis_imgs_dict = visualize.draw(frames_dict, preds_dict, judgements_dict, show_fps)

        # handle judgement results
        handling.handle_judgement(judgements_dict, vis_imgs_dict)

        img = vis_imgs_dict[vis_name]
        cv2.namedWindow(vis_name, cv2.WINDOW_NORMAL)
        cv2.imshow(vis_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--open-opc', type=bool, default=False, help='whether to connect to opc server')

    # model config
    parser.add_argument('--img-size', type=int, default=416, help='size of each image dimension')
    parser.add_argument('--config-path', type=str, default='config/yolov3.cfg', help='path to model config file')
    parser.add_argument('--weights-path', type=str, default='weights/yolov3.weights', help='path to weights file')
    parser.add_argument('--class-path', type=str, default='config/coco.names', help='path to class label file')
    parser.add_argument('--conf-thres', type=float, default=0.8, help='object confidence threshold')
    parser.add_argument('--nms-thres', type=float, default=0.4, help='iou threshold for non-maximum suppression')
    parser.add_argument('--device', type=str, default='cuda:0', help='whether to use cuda if available')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    main(args)
