from shroom import read_data, draw_shroom, get_model, precision_recall
from matplotlib import pyplot as plt

DATASET_VERSION = 'mushroom_world_2017_16_10'
X, y, mushroom_info = read_data(DATASET_VERSION)

model, train_history = get_model()
probs = model.predict(X/255.0)
probs.shape = probs.shape[0]

decision_tresholds = np.arange(0,1,step = 0.01)
precisions, recalls = precision_recall(decision_tresholds, probs, labels = y)

plt.plot(recalls, label = "Recall (pick all edibles)")
plt.plot(precisions, label = "Precision (no death to poison)")
plt.legend()
plt.title("Precision and recall by classification treshold")
plt.savefig("docs/precision_recall.png")
plt.show()






