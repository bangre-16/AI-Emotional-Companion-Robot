#!/usr/bin/env python3
"""
Test all model files to find which one works properly
"""
import tensorflow as tf
import numpy as np
import os

def test_model(model_path):
    """Test a single model file"""
    print(f"\n🔍 Testing {model_path}:")
    
    if not os.path.exists(model_path):
        print(f"  ❌ File not found")
        return False
    
    try:
        # Load model
        model = tf.keras.models.load_model(model_path)
        print(f"  ✅ Model loaded successfully")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
        
        # Test with different inputs
        test1 = np.random.random((1, 48, 48, 1))
        test2 = np.random.random((1, 48, 48, 1)) * 0.5
        test3 = np.ones((1, 48, 48, 1)) * 0.8
        
        pred1 = model.predict(test1, verbose=0)
        pred2 = model.predict(test2, verbose=0)
        pred3 = model.predict(test3, verbose=0)
        
        # Check if predictions are identical (bad sign)
        identical_12 = np.allclose(pred1, pred2, atol=1e-6)
        identical_13 = np.allclose(pred1, pred3, atol=1e-6)
        identical_23 = np.allclose(pred2, pred3, atol=1e-6)
        
        print(f"  Predictions identical (1&2): {identical_12}")
        print(f"  Predictions identical (1&3): {identical_13}")
        print(f"  Predictions identical (2&3): {identical_23}")
        
        if identical_12 and identical_13 and identical_23:
            print(f"  ❌ Model returns identical predictions for all inputs!")
            print(f"  Sample prediction: {pred1[0]}")
            return False
        else:
            print(f"  ✅ Model responds to different inputs")
            print(f"  Test 1: {pred1[0]}")
            print(f"  Test 2: {pred2[0]}")
            print(f"  Test 3: {pred3[0]}")
            return True
            
    except Exception as e:
        print(f"  ❌ Error loading model: {e}")
        return False

def main():
    print("🧪 Testing All Model Files")
    print("=" * 50)
    
    model_files = [
        'best-emotion-model.h5',
        'best_emotion_model.h5', 
        'emotion_detection.h5',
        'train-model.h5'
    ]
    
    working_models = []
    
    for model_path in model_files:
        if test_model(model_path):
            working_models.append(model_path)
    
    print("\n" + "=" * 50)
    print("📊 Results:")
    print(f"Total models tested: {len(model_files)}")
    print(f"Working models: {len(working_models)}")
    
    if working_models:
        print(f"✅ Working models: {working_models}")
        print(f"💡 Recommendation: Use '{working_models[0]}' in app.py")
    else:
        print("❌ No working models found!")
        print("💡 Recommendation: Retrain the model using train.py")

if __name__ == "__main__":
    main()
