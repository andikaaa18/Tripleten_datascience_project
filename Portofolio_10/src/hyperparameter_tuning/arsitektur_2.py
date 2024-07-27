import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Conv2D
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.regularizers import l1_l2
from tensorflow.keras.optimizers import Adam
import os
import tempfile
import optuna
import gc

# function untuk membuat image generator pada training set
def load_train(df, path):
    augmented_datagen = ImageDataGenerator(rescale=1/255, horizontal_flip=True, vertical_flip=True)
    
    train_data_flow = augmented_datagen.flow_from_dataframe(dataframe=df,
                                                            directory=path,
                                                            x_col='file_name',
                                                            y_col='real_age',
                                                            target_size=(150, 150),
                                                            class_mode='raw',
                                                            batch_size=32,
                                                            seed=101010)
    
    return train_data_flow

# function untuk membuat image generator pada validation dan test set
def load_test(df, path, shuffle=True):
    if shuffle:
        seed = 101010
    else:
        seed=None

    datagen = ImageDataGenerator(rescale=1/255)
    test_data_flow = datagen.flow_from_dataframe(dataframe=df,
                                                 directory=path,
                                                 x_col='file_name',
                                                 y_col='real_age',
                                                 target_size=(150, 150),
                                                 class_mode='raw',
                                                 batch_size=32,
                                                 shuffle=shuffle,
                                                 seed=seed)
    return test_data_flow

def feature_engineering():
    # memuat data
    data = pd.read_csv("./datasets/faces/labels.csv")

    # mengeluarkan outliers
    q3 = data['real_age'].quantile(0.75)
    q1 = data['real_age'].quantile(0.25)
    iqr = q3 - q1
    lower_bound = np.ceil(np.max([0, q1-1.5*iqr]))
    upper_bound = np.ceil(q3+1.5*iqr)
    filter_data = data.query("@lower_bound<=real_age<=@upper_bound")

    # data split
    train_data, val_data = train_test_split(filter_data, test_size=0.3, random_state=101010)
    val_data, test_data = train_test_split(val_data, test_size=0.5, random_state=101010)

    return train_data, val_data, test_data

def create_model(input_shape, neuron_1, neuron_2, neuron_3, neuron_4, l1_constant, l2_constant):
    def add_regularization(model, regularizer):
        # menambahkan informasi regularizer pada layer Dense atau Conv2D pada config file
        for layer in model.layers:
            if isinstance(layer, (Conv2D, Dense)):
                layer.kernel_regularizer = regularizer
        
        # Saat kita mengubah atribut layer, perubahan hanya terjadi pada file konfigurasi model
        model_config = model.to_json()

        # Simpan bobot sebelum memuat ulang model.
        tmp_weights_path = os.path.join(tempfile.gettempdir(), 'tmp_weights.h5')
        model.save_weights(tmp_weights_path)

        # memuat model dari config file
        model = tf.keras.models.model_from_json(model_config)

        # memuat nilai bobot yang sudah disimpan
        model.load_weights(tmp_weights_path, by_name=True)

        return model
    
    # ResNet50V2 backbone
    backbone = ResNet50V2(include_top=False,
                          weights='imagenet',
                          input_shape=input_shape)

    # mengatur regularisasi pada backbone
    backbone = add_regularization(backbone, l1_l2(l1=l1_constant, l2=l2_constant))

    # add new top layers
    model = Sequential()
    model.add(backbone)
    model.add(GlobalAveragePooling2D())
    model.add(Dense(units=neuron_1, activation='relu', kernel_regularizer=l1_l2(l1=l1_constant, l2=l2_constant)))
    model.add(Dense(units=neuron_2, activation='relu', kernel_regularizer=l1_l2(l1=l1_constant, l2=l2_constant)))
    model.add(Dense(units=neuron_3, activation='relu', kernel_regularizer=l1_l2(l1=l1_constant, l2=l2_constant)))
    model.add(Dense(units=neuron_4, activation='relu', kernel_regularizer=l1_l2(l1=l1_constant, l2=l2_constant)))
    model.add(Dense(1, activation='relu', kernel_regularizer=l1_l2(l1=l1_constant, l2=l2_constant)))

    model.compile(optimizer=Adam(learning_rate=0.0001), loss='mse', metrics=['mae'])

    return model

def train_model(model, train_data, test_data, batch_size=None, epochs=50, steps_per_epoch=None, validation_steps=None):
    history = model.fit(train_data,
                        validation_data=test_data,
                        batch_size=batch_size,
                        epochs=epochs,
                        steps_per_epoch=steps_per_epoch,
                        validation_steps=validation_steps,
                        verbose=2)
    return history

def logging_callback(study, frozen_trial):
    previous_best_value = study.user_attrs.get('previous_best_value', None)
    if previous_best_value != study.best_value:
        previous_best_value = study.set_user_attr('previous_best_value', study.best_value)
        print("Trial {} finished with best value: {} and parameters: {}. ".format(
            frozen_trial.number,
            frozen_trial.value,
            frozen_trial.params,
            )
        )
    
    # membuang sampah process untuk mencegah running out memory
    gc.collect()

def hyperparameter_tuning(n_trials=10):
    def objective(trial):
        # hyperparameter
        exp_1 = trial.suggest_int('exp_1', 3, 10)
        exp_2 = trial.suggest_int('exp_2', 3, exp_1)
        exp_3 = trial.suggest_int('exp_3', 3, exp_2)
        exp_4 = trial.suggest_int('exp_4', 3, exp_3)
        l1_constant = trial.suggest_float('l1_constant', 0.001, 0.1)
        l2_constant = trial.suggest_float('l2_constant', 0.001, 0.1)
        
        # load data & feature engineering
        train_data, val_data, test_data = feature_engineering()

        # mengatur randomness model keras
        tf.keras.utils.set_random_seed(101010)
        tf.config.experimental.enable_op_determinism()

        # training
        train_gen = load_train(train_data, './datasets/faces/final_files/')
        val_gen = load_test(val_data, './datasets/faces/final_files/')

        model = create_model(input_shape=(150,150,3), neuron_1=2**exp_1, neuron_2=2**exp_2, neuron_3=2**exp_3, 
                             neuron_4=2**exp_4, l1_constant=l1_constant, l2_constant=l2_constant)
        
        history = train_model(model, train_gen, val_gen, epochs=10)

        return np.min(history.history['val_mae'])

    # atur logger agar tidak menampilkan log DEBUG dan INFO, tetapi hanya menampilkan log WARNING, ERROR dan CRITICAL
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    study = optuna.create_study(direction='minimize', sampler=optuna.samplers.TPESampler(seed=101010))
    study.optimize(objective, n_trials=n_trials, callbacks=[logging_callback])


if __name__=='__main__':
    hyperparameter_tuning(n_trials=5)