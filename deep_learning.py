from PIL import Image
import tensorflow as tf
from keras_preprocessing.image import ImageDataGenerator
from keras.models import Model
import numpy as np
from keras.layers import Input, Conv2D, Dense, Flatten, MaxPooling2D,Dropout,BatchNormalization

def model_func(path):

    tf.keras.backend.clear_session()
    InceptionResNetV2 = tf.keras.applications.InceptionResNetV2(input_shape=(75, 75, 3), include_top=False)
    for layer in InceptionResNetV2.layers[:-10]:
        layer.trainable = False

    flatten = Flatten()(InceptionResNetV2.output)

    drop = Dropout(0.5)(flatten)
    dense1 = Dense(512, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal(seed=32),
                   kernel_regularizer='l2')(drop)
    BN1 = tf.keras.layers.BatchNormalization()(dense1)
    dense2 = Dense(128, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal(seed=32),
                   kernel_regularizer='l2')(BN1)
    BN2 = tf.keras.layers.BatchNormalization()(dense2)
    dense3 = Dense(64, activation='relu', kernel_initializer=tf.keras.initializers.HeNormal(seed=32),
                   kernel_regularizer='l2')(BN2)
    BN3 = tf.keras.layers.BatchNormalization()(dense3)
    Output_layer = Dense(units=5, activation='softmax', kernel_initializer=tf.keras.initializers.glorot_uniform(),
                         name='Output')(BN3)

    model4 = Model(inputs=InceptionResNetV2.input, outputs=Output_layer)
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, decay=1e-2 / 15)
    model4.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy", "AUC"], run_eagerly=True)

    model4.load_weights(path)

    return model4


def predict(image,model):
    lst = ["basophil","eosinophil","lymphocyte","monocyte","neutrophil",]
    image=image.resize((75,75))
    test_datagen = ImageDataGenerator(rescale=1./255)
    image = tf.keras.preprocessing.image.img_to_array(image)
    test_generator = test_datagen.flow(image.reshape(1,75,75, 3))
    output_data = model.predict(test_generator)
    return lst[np.argmax(output_data, axis=1)[0]]
