# train.py (fixed)
import os
import glob
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# -------------------------
# Configuration
# -------------------------
# If you have a fer2013.csv put it in the backend folder and set CSV_FILENAME to that name.
CSV_FILENAME = "fer2013.csv"    # filename expected in backend/
DATASET_PATH = "fer2013.csv"    # used when using image folders (fer2013.csv/train/... )
IMG_SIZE = 48
BATCH_SIZE = 64
EPOCHS = 25                    # train longer for better accuracy
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

BEST_MODEL_FILE = "best-emotion-model.h5"
FINAL_MODEL_FILE = "train-model.h5"

# -------------------------
# Model builder
# -------------------------
def build_model(input_shape=(IMG_SIZE, IMG_SIZE, 1), num_classes=len(EMOTION_LABELS)):
    model = Sequential([
        Conv2D(64, (3, 3), padding='same', input_shape=input_shape),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        Conv2D(64, (3, 3), padding='same'),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),

        Conv2D(128, (3, 3), padding='same'),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        Conv2D(128, (3, 3), padding='same'),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),

        Conv2D(256, (3, 3), padding='same'),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        Conv2D(256, (3, 3), padding='same'),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.3),

        Flatten(),
        Dense(512),
        BatchNormalization(),
        keras.layers.Activation('relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=Adam(learning_rate=1e-3),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

# -------------------------
# CSV helper
# -------------------------
def preprocess_pixels(pixels_str):
    # pixels_str example: '70 80 90 ...'
    arr = np.fromstring(pixels_str, dtype=np.float32, sep=' ')
    arr = arr.reshape((IMG_SIZE, IMG_SIZE, 1))
    arr = arr / 255.0
    return arr

# -------------------------
# Training: folders (flow_from_directory)
# -------------------------
def train_from_folders(base_path):
    print("Training from image folders (flow_from_directory).")
    # Accept either: images/<class>/*.jpg  OR images/train/<class>/*.jpg + images/test/<class>/*.jpg
    train_dir = os.path.join(base_path, "train")
    data_dir = base_path if not os.path.isdir(train_dir) else train_dir
    has_test_folder = os.path.isdir(os.path.join(base_path, "test"))

    datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255.0,
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.15,
        shear_range=0.1,
        brightness_range=(0.7, 1.3),
        horizontal_flip=True,
        validation_split=0.2
    )

    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    test_gen = None
    if has_test_folder:
        test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1.0/255.0)
        test_gen = test_datagen.flow_from_directory(
            os.path.join(base_path, "test"),
            target_size=(IMG_SIZE, IMG_SIZE),
            color_mode='grayscale',
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            shuffle=False
        )

    model = build_model(input_shape=(IMG_SIZE, IMG_SIZE, 1))
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(patience=8, restore_best_weights=True, monitor='val_loss'),
        keras.callbacks.ModelCheckpoint(BEST_MODEL_FILE, save_best_only=True, monitor='val_loss'),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6)
    ]

    steps_per_epoch = max(1, train_gen.samples // BATCH_SIZE)
    validation_steps = max(1, val_gen.samples // BATCH_SIZE)

    # Compute class weights to reduce class imbalance impact
    class_indices = train_gen.class_indices
    inv_class_indices = {v: k for k, v in class_indices.items()}
    counts = np.zeros(len(inv_class_indices), dtype=np.int64)
    for cls, idx in class_indices.items():
        counts[idx] = len(os.listdir(os.path.join(data_dir, cls)))
    total = counts.sum()
    class_weights = {i: float(total / (len(counts) * max(1, counts[i]))) for i in range(len(counts))}

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )

    if test_gen is not None:
        test_loss, test_acc = model.evaluate(test_gen, verbose=1)
        print(f"Test Loss: {test_loss:.4f}  Test Acc: {test_acc:.4f}")

    model.save(FINAL_MODEL_FILE)
    print(f"Saved: {BEST_MODEL_FILE} and {FINAL_MODEL_FILE}")
    return history

# -------------------------
# Training: CSV (fer2013-like)
# -------------------------
def train_from_csv(csv_path):
    print(f"Training from CSV: {csv_path}")
    df = pd.read_csv(csv_path)

    required = {'emotion', 'pixels', 'Usage'}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must include columns: {required}. Found columns: {df.columns.tolist()}")

    # Typical fer2013 Usage categories: Training, PublicTest, PrivateTest
    train_df = df[df['Usage'] == 'Training']
    val_df = df[df['Usage'] == 'PublicTest']
    test_df = df[df['Usage'] == 'PrivateTest']

    if len(train_df) == 0:
        raise ValueError("No training rows found in CSV with Usage=='Training'")

    print("Preparing numpy arrays from CSV (this can take time)...")
    X_train = np.stack([preprocess_pixels(p) for p in train_df['pixels'].values])
    y_train = keras.utils.to_categorical(train_df['emotion'].values, num_classes=len(EMOTION_LABELS))

    X_val = np.stack([preprocess_pixels(p) for p in val_df['pixels'].values]) if len(val_df) > 0 else None
    y_val = keras.utils.to_categorical(val_df['emotion'].values, num_classes=len(EMOTION_LABELS)) if len(val_df) > 0 else None

    X_test = np.stack([preprocess_pixels(p) for p in test_df['pixels'].values]) if len(test_df) > 0 else None
    y_test = keras.utils.to_categorical(test_df['emotion'].values, num_classes=len(EMOTION_LABELS)) if len(test_df) > 0 else None

    model = build_model(input_shape=(IMG_SIZE, IMG_SIZE, 1))
    model.summary()

    callbacks = [
        keras.callbacks.EarlyStopping(patience=12, restore_best_weights=True),
        keras.callbacks.ModelCheckpoint(BEST_MODEL_FILE, save_best_only=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, min_lr=1e-6)
    ]

    history = model.fit(
        X_train, y_train,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val) if X_val is not None else None,
        callbacks=callbacks,
        verbose=1
    )

    if X_test is not None:
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=1)
        print(f"Test Loss: {test_loss:.4f}  Test Acc: {test_acc:.4f}")

    model.save(FINAL_MODEL_FILE)
    print(f"Saved: {BEST_MODEL_FILE} and {FINAL_MODEL_FILE}")
    return history

# -------------------------
# Main dispatcher
# -------------------------
def main():
    cwd = os.getcwd()
    print("Current working dir:", cwd)

    # 1) Look for CSV in current folder first (backend/fer2013.csv)
    csv_full = os.path.join(cwd, CSV_FILENAME)
    if os.path.isfile(csv_full):
        print("Found CSV file:", csv_full)
        return train_from_csv(csv_full)

    # 2) Otherwise look for image folders
    images_full = os.path.join(cwd, DATASET_PATH)
    if os.path.isdir(images_full):
        # check for class subfolders
        subfolders = [p for p in glob.glob(os.path.join(images_full, "*")) if os.path.isdir(p)]
        if len(subfolders) == 0:
            print(f"No class subfolders found under {images_full}. Expected images/<class>/*.jpg")
        else:
            print("Found image subfolders (example):", [os.path.basename(s) for s in subfolders[:8]])
            return train_from_folders(images_full)

    # nothing found
    print("ERROR: No dataset found. Place fer2013.csv in the backend folder OR create images/<class> subfolders.")
    return

if __name__ == "__main__":
    main()
