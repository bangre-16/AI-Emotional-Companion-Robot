#!/usr/bin/env python3
"""
Evaluate all model files on the test set to find the best performing model
"""
import os
import glob
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Configuration
IMG_SIZE = 48
BATCH_SIZE = 32
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
TEST_DIR = "backend/fer2013.csv/test"

def get_test_generator():
    """Create test data generator"""
    test_datagen = ImageDataGenerator(rescale=1.0/255.0)

    test_gen = test_datagen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode='grayscale',
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    return test_gen

def evaluate_model(model_path, test_gen):
    """Evaluate a single model on the test set"""
    print(f"\n🔍 Evaluating {model_path}:")

    if not os.path.exists(model_path):
        print(f"  ❌ File not found")
        return None, None

    try:
        # Load model
        model = keras.models.load_model(model_path)
        print(f"  ✅ Model loaded successfully")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")

        # Evaluate on test set
        test_steps = max(1, test_gen.samples // BATCH_SIZE)
        loss, accuracy = model.evaluate(test_gen, steps=test_steps, verbose=1)

        print(f"  Test Loss: {loss:.4f}")
        print(f"  Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

        return loss, accuracy

    except Exception as e:
        print(f"  ❌ Error evaluating model: {e}")
        return None, None

def main():
    print("🧪 Evaluating All Model Files on Test Set")
    print("=" * 60)

    # Find all .h5 model files
    model_files = glob.glob("backend/*.h5")
    model_files = list(set(model_files))  # Remove duplicates

    if not model_files:
        print("❌ No .h5 model files found!")
        return

    print(f"Found {len(model_files)} model files:")
    for mf in model_files:
        print(f"  - {mf}")

    # Check if test directory exists
    if not os.path.exists(TEST_DIR):
        print(f"❌ Test directory not found: {TEST_DIR}")
        return

    # Create test generator
    test_gen = get_test_generator()
    print(f"Test samples: {test_gen.samples}")

    # Evaluate each model
    results = []
    for model_path in model_files:
        loss, acc = evaluate_model(model_path, test_gen)
        if acc is not None:
            results.append((model_path, loss, acc))

    # Sort by accuracy descending
    results.sort(key=lambda x: x[2], reverse=True)

    print("\n" + "=" * 60)
    print("📊 Evaluation Results (sorted by accuracy):")
    print(f"{'Model':<30} {'Loss':<10} {'Accuracy':<10}")
    print("-" * 50)
    for model_path, loss, acc in results:
        print(f"{model_path:<30} {loss:<10.4f} {acc:<10.4f}")

    if results:
        best_model, best_loss, best_acc = results[0]
        print(f"\n🏆 Best Model: {best_model}")
        print(f"   Accuracy: {best_acc:.4f} ({best_acc*100:.2f}%)")
        print(f"   Loss: {best_loss:.4f}")

        print("\n💡 Recommendation: Update app.py to use this model by changing MODEL_PATH to")
        print(f"   '{best_model}'")
    else:
        print("❌ No models could be evaluated successfully!")

if __name__ == "__main__":
    main()
