import pandas as pd
import numpy as np
from scipy import misc
import math
from matplotlib import pyplot as plt



def read_data(version):
    DATASET_PATH = 'data/{}/'.format(version)

    mushroom_classes = pd.read_json(DATASET_PATH + 'mushroom_classes.json', lines=True)
    mushroom_imgs = pd.read_json(DATASET_PATH + 'mushroom_imgs.json', lines=True)
    mushroom_info = mushroom_imgs.merge(mushroom_classes, how = "right", on = "name_latin")


    def load_mushroom_images(folder_path, img_df):
        img_dict = {}
        for index, path in enumerate(img_df['file_path']):
            img_dict[index] = misc.imread(folder_path + path)
        return img_dict
    
    
    img_dict =  load_mushroom_images(DATASET_PATH, mushroom_imgs)
    img_dict = format_images(img_dict)
    X = np.stack(dict2list(img_dict))
    y = mushroom_info.edibility.isin(("edible", "edible and good", "edible and excellent"))
    y = pd.Series(y)
    return X, y, mushroom_info



def format_images(img_dict):
    
    #Format the pictures to (480,480,3) by padding them with the edge values
    for img in img_dict:
        height = 480 - img_dict[img].shape[0]
        width = 480 - img_dict[img].shape[1]

        if(height % 2 == 1 & width % 2 == 1):
            height1,height2 = math.floor(height/2), math.floor(height/2) + 1
            width1,width2 = math.floor(width/2), math.floor(width/2) +1
        elif(width % 2 == 1):
            width1,width2 = math.floor(width/2), math.floor(height/2) + 1
            height1,height2 = int(height/2), int(height/2)
        elif(height % 2 == 1):
            height1,height2 = math.floor(height/2), math.floor(height/2) + 1
            width1,width2 = int(width/2), int(width/2) 
        else:
            height1,height2 = int(height/2), int(height/2)
            width1,width2 = int(width/2), int(width/2)

        if(height == 0):
            img_dict[img] = np.lib.pad(img_dict[img], ((0,0),(width1, width2),(0,0)), 'edge')
        elif (width == 0):
            img_dict[img] = np.lib.pad(img_dict[img], ((height1, height2),(0,0),(0,0)), 'edge')
        else:
            img_dict[img] = np.lib.pad(img_dict[img], ((height1, height2),(width1, width2),(0,0)), 'edge')
            
    return img_dict


def dict2list(dict):
    X = []
    for i in range(len(dict)):
        X.append(dict[i])
    return X


def draw_shroom(i, X, y):
    plt.imshow(X[i])
    plt.title("edible: " + str(y[i]))
    plt.show()


def get_model(path = "models"):
    from keras.models import model_from_json
    import pickle
    
    json_file = open(path + '/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(path + "/weights.h5")
    
    with open(path + "/history", "rb") as f:
        train_history = pickle.load(f)
        
    return loaded_model, train_history


def precision_recall(decision_tresholds, probs, labels):
    
    def recall(predictions, labels):
        n = sum(labels)
        k =  sum(labels[predictions])
        return k / n


    def precision(predictions, labels):
        n = sum(predictions)
        k = sum(labels[predictions])
        return k / n

    recalls = [recall(probs > treshold, labels) for treshold in decision_tresholds]
    precisions = [precision(probs > treshold, labels) for treshold in decision_tresholds]
    
    return precisions, recalls
