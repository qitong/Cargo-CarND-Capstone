import tensorflow as tf
import numpy as np
import time

TRAFFIC_CLASSIFIER_MDOEL_PATH = '/Users/qitonghu/Desktop/final_project/old/Cargo-CarND-Capstone/traffic_light_detection_profiles/frozen_inference_graph.pb'

class TrafficLightDetector(object):
    def __init__(self):
        self.detection_graph = tf.Graph()

        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()

            with tf.gfile.GFile(TRAFFIC_CLASSIFIER_MDOEL_PATH, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        with self.detection_graph.as_default():
            with tf.Session(graph=self.detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

                image_np = self.__preprocess_image(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)

                time0 = time.time()

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                time1 = time.time()

                print("Time in milliseconds", (time1 - time0) * 1000)
                print(boxes, scores, classes)
        return 0 #TrafficLight.UNKNOWN

    def __preprocess_image(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def __postprocessing_detected_box(self):
        pass

if __name__ == "__main__":
    from PIL import Image

    tlc = TrafficLightDetector()
    image_path = '/Users/qitonghu/Desktop/final_project/old/Cargo-CarND-Capstone/traffic_light_detection_profiles/test_images_bosch/image3.png'
    image = Image.open(image_path)
    tlc.get_classification(image)
    image_path = '/Users/qitonghu/Desktop/final_project/old/Cargo-CarND-Capstone/traffic_light_detection_profiles/test_images_bosch/image4.png'
    image = Image.open(image_path)
    tlc.get_classification(image)