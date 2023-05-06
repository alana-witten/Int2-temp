# -*- coding: utf-8 -*-
"""0.15 Four 90° Rotations.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uIWZRDqj3A030zmVl86PxHcPCBI_VLNg
"""

import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import tensorflow_datasets as tfds
import pathlib
import tensorflow_addons as tfa


from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from tensorflow_datasets.core.features.dataset_feature import Dataset
#load the dataset with tfds and split into train, validate and test
flowers, flowers_info = tfds.load('oxford_flowers102', as_supervised = True, with_info = True)
flowers_train_raw, flowers_valid_raw, flowers_test_raw = flowers['train'], flowers['validation'], flowers['test']

print(flowers_train_raw)

#Uses for manual testing, can be deleted later.
#prints out a untouched image and a augmented one
def visualize(original, augmented):
  fig = plt.figure()
  plt.subplot(1,2,1)
  plt.title('Original image')
  plt.imshow(original)

  plt.subplot(1,2,2)
  plt.title('Augmented image')
  plt.imshow(augmented)




#express the dataset in its splits
training_length = len(flowers_train_raw)
validation_length = len(flowers_valid_raw)
test_length = len(flowers_test_raw)

def rotate(image):
    angle = tf.random.uniform([], minval=-30, maxval=30, dtype=tf.float32)
    image = tfa.image.rotate(image, angle)
    
    return image

#testing out image resizing and rescaling
def imageAug(image, label):
  image = tf.cast(image, tf.float32)
  
  # image = tf.zeros(shape=(128, 128, 3), dtype=tf.float32) #make completely black image
  #resizes image
  image = tf.image.resize(image, (128, 128))
#   image = rotate(image)
  return image, label

#train and valid are now (32 * 500 * 500 * 3) tensors
#that is 32 seperate 500 * 500 images in one. (3 represents the RGB values)
flowers_train = (flowers_train_raw.map(imageAug).batch(32))
flowers_valid = flowers_valid_raw.map(imageAug).batch(32)
flowers_test = flowers_test_raw.map(imageAug)

# flowers_train_raw_augmented = flowers_train_raw.map(imageAug)
# flowers_train = flowers_train_raw.concatenate(flowers_train_raw_augmented).batch(32)
# flowers_valid_raw_augmented = flowers_valid_raw.map(imageAug)
# flowers_valid = flowers_valid_raw.concatenate(flowers_valid_raw_augmented).batch(32)

# spec = flowers_train.element_spec
# empty_data = tf.zeros((32, 128, 128, 3))
# empty_dataset = tf.data.Dataset.from_tensor_slices(empty_data)

# flowers_train = flowers_train.concatenate(empty_dataset)

# flowers_info.features['label']

image_count = training_length + validation_length + test_length

#define params for the loader
batch_size = 32
height = 500
width = 500

class_names = flowers_info.features['label']
print(class_names.names)
num_classes = len(class_names.names)

#model
model = Sequential()
#rescaling layer, can do this before

(layers.Rescaling(1./255, input_shape=(height, width, 3)))



# duplicating the training data
# flowers_train_raw_new = Dataset
# for x in range(4):
#   for img, label in flowers_train_raw:
#     rotated = tf.image.rot90(img)

# num_elements = flowers_train.reduce(0, lambda x, _: x + 1).numpy()
# print(num_elements)


# visualize(img, rotated)
    
# model.add(layers.RandomContrast(,,))
#first full layer
model.add(layers.Conv2D(16, 3, padding = 'same', activation = 'relu'))
model.add(layers.MaxPooling2D())
#second full layer
model.add(layers.Conv2D(32, 3, padding = 'same', activation = 'relu'))
model.add(layers.MaxPooling2D())
#third full layer
model.add(layers.Conv2D(64, 3, padding = 'same', activation= 'relu'))
model.add(layers.MaxPooling2D())
#flatten layer
model.add(layers.Flatten())
#first dense layer
model.add(layers.Dense(128, activation='relu'))
#output layer
model.add(layers.Dense(num_classes))

#compile the model
model.compile(optimizer = 'adam',
              loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics = ['accuracy'])

##model.summary()

#train the model
epochs = 5
history = model.fit(flowers_train, validation_data=flowers_valid, epochs=epochs)

model.summary()

#visualise training results

#accuracy
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
#loss
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1,2,2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc = 'upper right')
plt.title('Training and Validation Loss')
plt.show()