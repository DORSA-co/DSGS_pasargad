import numpy as np
import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import warnings
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import cv2
import draw_xml
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings



IMAGE_PATHS = './images/dataset/test/'
#IMAGE_PATHS = './images/oxin/'
#IMAGE_PATHS = './images/test/'

MODEL_PATH = './exported-models/model/saved_model'
LABEL_MAP_PATH = './annotations/label_map.pbtxt'




detect_fn = tf.saved_model.load(MODEL_PATH)
category_index = label_map_util.create_category_index_from_labelmap(LABEL_MAP_PATH,
                                                                    use_display_name=True)

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))


for image_name in os.listdir(IMAGE_PATHS):
    
    dot_idx = image_name.find('.')
    if image_name[dot_idx:] not in ['.png', '.jpg' , '.jpeg', '.bmp']:
        continue        
    
    print('Running inference for {}... '.format(os.path.join(IMAGE_PATHS,image_name)), end='')

    image_np = load_image_into_numpy_array(os.path.join(IMAGE_PATHS,image_name))

    if len(image_np.shape)==2:
        image_np = np.expand_dims(image_np, axis=-1)
        image_np = np.concatenate((image_np,image_np,image_np), axis=-1)
    
    xml_name = image_name[:dot_idx] + '.xml'
    true_boxes = draw_xml.get_bndboxes( IMAGE_PATHS, xml_name)

    
    

    # Things to try:
    # Flip horizontally
    # image_np = np.fliplr(image_np).copy()

    # Convert image to grayscale
    # image_np = np.tile(
    #     np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)
    
    
    
    
    
    
    
    

    boxes_tensor = tf.convert_to_tensor(detections['detection_boxes'], np.float32)[0]
    scores_tensor = tf.convert_to_tensor(detections['detection_scores'], np.float32)[0]
    classes_tensor = tf.convert_to_tensor(detections['detection_classes'], np.float32)[0]
    
    selected_indices = tf.image.non_max_suppression(boxes=boxes_tensor, max_output_size=50, iou_threshold=0.2,scores=scores_tensor)
    
    boxes = tf.gather(boxes_tensor, selected_indices)
    scores = tf.gather(scores_tensor, selected_indices)
    classes = tf.gather(classes_tensor, selected_indices)
        
    
    #boxes = tf.expand_dims(boxes, 0)
    #scores = tf.expand_dims(scores, 0)
    #classes = tf.expand_dims(classes, 0)
        
    boxes = boxes.numpy()
    scores = scores.numpy()
    classes = classes.numpy().astype(np.int64)
    
    
    
    
    
    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}

    # detection_classes should be ints.
    #detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    

    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
          image_np_with_detections,
          boxes,# detections['detection_boxes'],
          classes,#detections['detection_classes'],
          scores,#detections['detection_scores'],
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=10,
          min_score_thresh=.3,
          agnostic_mode=False)

    #plt.figure()
    #plt.imshow(image_np_with_detections)
    #print('Done')
    #plt.show()

    image_np_with_detections = draw_xml.draw_boxes( image_np_with_detections, true_boxes)
    #cv2.imshow('image', cv2.resize(image_np_with_detections,None,fx=0.5,fy=0.5))
    cv2.imshow('image', image_np_with_detections)
    key=cv2.waitKey(0)
    if key==27:
        cv2.destroyAllWindows()
        break

# sphinx_gallery_thumbnail_number = 2
