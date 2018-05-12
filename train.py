import cv2
import os
from PIL import Image
import numpy as np

HAARCASCADE_LIB_RALETIVE_PATH = 'extlib/haarcascades/'

def DetectFace(img):
    
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier(HAARCASCADE_LIB_RALETIVE_PATH + 'haarcascade_frontalface_default.xml')

    faces = face_cascade.detectMultiScale(grey_img, 1.2, 5)
    
    if (len(faces) == 0):
        print("Error: no face detected in this img")
        return None, None
        
    #It is expected to have only one face in trainning image
    (x, y, w, h) = faces[0]
    
    return grey_img[y:y+h, x:x+w], faces[0]
    
id_name_pair_map = {}
    
def GetTrainingData(training_img_folder_path):
    #return values
    faces  = []
    labels = []
    
    dirs = os.listdir(training_img_folder_path)
    id_counter = 0
    
    #Here dir_name will be the name of the person
    for dir_name in dirs:
        id_name_pair_map.update({id_counter: dir_name})
        label = id_counter
        id_counter += 1
        
        #This is the directory to store one person's training image
        individual_training_images_path = training_img_folder_path + "/" + dir_name
        #Get all images in the specified directory
        training_images = os.listdir(individual_training_images_path)
        
        for image_name in training_images:
            if (image_name.startswith(".")):
                continue;
                
            image_path = individual_training_images_path + "/" + image_name
            
            print("Image path: " + image_path)
            image = cv2.imread(image_path)
            
            face, rect = DetectFace(image)
            
            if (face is not None):
                resized = cv2.resize(face, (450, 450))
                faces.append(resized)
                labels.append(label)
    
    return faces, labels            
                
      
print("Retrieving training data...")
faces, labels = GetTrainingData("train_images")
print("Data retrieved")

print("Value : %s" %  id_name_pair_map.items()) 
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

recognizer = cv2.face.EigenFaceRecognizer_create()
recognizer.train(faces, np.array(labels))
recognizer.save("trained_data/EigenFaceData.yml")

def Predict(unknown_img):
    img = unknown_img.copy()
    
    face, rect = DetectFace(img)
    
    resized = cv2.resize(face, (450, 450))
    
    label, confidence = recognizer.predict(resized)
    
    print("id of this person is: " + str(label) + ". With Confidence: " + str(confidence))
    
    return img
    
test1 = cv2.imread("nationaltrasure2004.png")
predicted_img1 = Predict(test1)

    