import os
import cv2
import numpy as np
import tensorflow as tf

# ==========================
# DATA LOADING FUNCTION
# ==========================
def load_data(folder_path, label):
    data = []
    labels = []

    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)

        image = cv2.imread(image_path)

        if image is not None:
            image = cv2.resize(image, (128, 128))
            data.append(image)
            labels.append(label)

    return data, labels

# ==========================
# LOAD TRAIN DATA
# ==========================
train_batting, train_batting_labels = load_data(
    "dataset/train/batting", 0
)

train_bowling, train_bowling_labels = load_data(
    "dataset/train/bowling", 1
)

X_train = np.array(train_batting + train_bowling)
y_train = np.array(train_batting_labels + train_bowling_labels)

# ==========================
# LOAD TEST DATA
# ==========================
test_batting, test_batting_labels = load_data(
    "dataset/test/batting", 0
)

test_bowling, test_bowling_labels = load_data(
    "dataset/test/bowling", 1
)

X_test = np.array(test_batting + test_bowling)
y_test = np.array(test_batting_labels + test_bowling_labels)

# ==========================
# NORMALIZATION
# ==========================
X_train = X_train / 255.0
X_test = X_test / 255.0

print("Training Images:", len(X_train))
print("Testing Images:", len(X_test))

# ==========================
# CNN MODEL
# ==========================
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(
        32, (3, 3),
        activation='relu',
        input_shape=(128, 128, 3)
    ),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Conv2D(
        64, (3, 3),
        activation='relu'
    ),
    tf.keras.layers.MaxPooling2D((2, 2)),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(
        128,
        activation='relu'
    ),

    tf.keras.layers.Dense(
        1,
        activation='sigmoid'
    )
])

# ==========================
# COMPILE
# ==========================
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ==========================
# TRAIN
# ==========================
history = model.fit(
    X_train,
    y_train,
    epochs=10,
    validation_data=(X_test, y_test)
)

# ==========================
# SAVE MODEL
# ==========================
model.save("sports_model.h5")

print("✅ Model saved as sports_model.h5")