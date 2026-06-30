#!/usr/bin/env python3
"""
Analyze the emotion detection dataset
"""
import os

def analyze_dataset():
    """Analyze the dataset distribution"""
    train_dir = "fer2013.csv/train"
    test_dir = "fer2013.csv/test"
    
    print("=== Dataset Analysis ===")
    print(f"Train directory: {train_dir}")
    print(f"Test directory: {test_dir}")
    
    if os.path.exists(train_dir):
        classes = os.listdir(train_dir)
        print(f"\nClasses found: {classes}")
        
        print("\nTraining set distribution:")
        total_train = 0
        for cls in classes:
            count = len(os.listdir(os.path.join(train_dir, cls)))
            total_train += count
            print(f"  {cls}: {count:,} samples")
        
        print(f"\nTotal training samples: {total_train:,}")
        
        print("\nClass percentages:")
        for cls in classes:
            count = len(os.listdir(os.path.join(train_dir, cls)))
            percentage = (count / total_train) * 100
            print(f"  {cls}: {percentage:.1f}%")
    
    if os.path.exists(test_dir):
        print(f"\nTest set distribution:")
        total_test = 0
        for cls in classes:
            count = len(os.listdir(os.path.join(test_dir, cls)))
            total_test += count
            print(f"  {cls}: {count:,} samples")
        
        print(f"\nTotal test samples: {total_test:,}")

if __name__ == "__main__":
    analyze_dataset()
