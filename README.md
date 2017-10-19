This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

### Cargo team and team members
* Team name
#### Cargo
*Cargo* means car drives autonomously.
* Team members
* Our Lead Submission is https://github.com/xfqbuaa/Cargo-CarND-Capstone 

|                  | Name            |  Email                  |
| --------         | -----           |  ----                   |
| Team Lead        | Fuqiang Xu      |  qiyuwang@163.com       |
| Team Member 1    | Sridhar Sampath |  sridhar912@gmail.com   |
| Team Member 2    | Takashi Ikegami |  tks.ikegami@gmail.com  |
| Team Member 3    | Andras Hejj     |  andreas.hejj@gmail.com |
| Team Member 4    | Qitong Hu       |  huqitong@aiztone.com   |


### Traffic Detection Model


In our team, I'm mainly taking charge of training the traffic light classifier and integrate the model into the whole system. The model we use to traffic light detection is transferred from ssd-inception model using Tensorflow objecct detection API.

There are two separately classifier model, one for simulator and one for Carla. All these parameters are integrated in tl_detector.launch and tl_detector_site.launch.

The original pre-trained model is downloaded from tensorflow/models. One data are from Bosch and the other from our classmate Shyam Jagannathan shared in slack, which is taken from simulator and rosbag.

We use the Tensorflow Object-Detection API to train the model with some hyperparameters tuned in the config file and a project-specific label-map file (number of classes to 4, proposal region to 10 and second stage batch size to 8, max detection to 4 and max per class to 4). we get the models after training around 20K step with final loss under 0.5.

At first, we train the model with Bosch data (rgb version and additional set) but traffic light detection perform poor and takes a lot of time. Then we train with task-specific data only.

We tried with ssd-mobile, ssd-inception, faster-rcnn and rcfn as pre-trained model separately. The later-two are good at accuracy but the model size is around 200M and need additional 0.03s (about 60% more) time to detect. We compare these four models from the processing time, accuracy and model size, finally we decide to use ssd-Inception model.

The traffic light classifier loads the model during initiating, then processes the image and outputs the classification and probability of detected box. We set 0.5 as the accepting threshold, and all the accepted ones will have a majority vote, the vote result will be our final judgment. The whole process takes around 0.05s for ssd-Inception and 0.08s for Faster-RCNN model (both testing on Qitong Ubuntu16.04 system with GTX1080Ti), both satisfactory with designed requirement time to response -- 0.1s (10Hz).
