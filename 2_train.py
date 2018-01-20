
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense
from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.optimizers import SGD

from src.net import mobilenet_binary_classifier

def build_generator(train_directory="dataset",
                    valid_directory="..//dataset//weakly-digit-detector//val"):

    # prepare data augmentation configuration
    train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input,
                                       rotation_range=20.0,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.4,
                                       zoom_range=0.2)
    valid_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_generator = train_datagen.flow_from_directory(directory=train_directory,
                                                        target_size=(224, 224),
                                                        batch_size=8)
    valid_generator = valid_datagen.flow_from_directory(directory=valid_directory,
                                                        target_size=(224, 224),
                                                        batch_size=8)
    return train_generator, valid_generator

def create_callbacks(weight_file="mobilenet_cls2.h5"):
    from keras.callbacks import ModelCheckpoint
    checkpoint = ModelCheckpoint("weights.{epoch:02d}.h5", 
                                 monitor='loss', 
                                 verbose=1, 
                                 save_best_only=False,
                                 mode='min', 
                                 period=1)
    return [checkpoint]

mobilenet = mobilenet_binary_classifier()
train_generator, valid_generator = build_generator()
mobilenet.fit_generator(train_generator,
                        steps_per_epoch = len(train_generator),
#                         validation_data = valid_generator,
#                         validation_steps = len(valid_generator),
                        callbacks        = create_callbacks(),
                        epochs=20)


