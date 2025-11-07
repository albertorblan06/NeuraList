# ML Algorithms Development

**🧠 This is where you develop and train ML/AI algorithms**

## Purpose

This folder is for:
- ✅ Training ML models
- ✅ Developing C/C++ algorithms
- ✅ Researching and experimenting
- ✅ Exporting trained models
- ✅ Testing algorithm performance

**NOT for app code** - see `neuralist_app/` for that!

## Structure

```
ml_algorithms/
│
├── training/                    # Training scripts and data
│   ├── train_product_recognition.py
│   ├── train_feature_extractor.py
│   ├── datasets/                # Training datasets
│   └── notebooks/               # Jupyter notebooks for experiments
│
├── models/                      # Exported trained models
│   ├── product_detector.tflite # Ready to use in app
│   ├── feature_extractor.tflite
│   └── checkpoints/             # Training checkpoints
│
├── src/                         # C/C++ ML algorithm implementations
│   ├── feature_extraction/      # Feature extraction algorithms
│   ├── product_matching/        # Matching algorithms
│   ├── preprocessing/           # Image preprocessing
│   └── utils/                   # Utilities
│
├── export/                      # Model export utilities
│   ├── export_to_tflite.py
│   ├── optimize_model.py
│   └── validate_export.py
│
├── docs/                        # Algorithm documentation
│   ├── architecture.md
│   ├── training_guide.md
│   └── performance_benchmarks.md
│
└── README.md                    # This file
```

## Workflow

### 1. Develop Algorithm (C++)
```bash
cd src/feature_extraction
# Write your C++ algorithm
# Test it standalone
```

### 2. Train Model (Python)
```bash
cd training
python train_product_recognition.py
```

### 3. Export Model
```bash
cd export
python export_to_tflite.py --model ../models/checkpoints/best.h5
# Creates: models/product_detector.tflite
```

### 4. Copy to App
```bash
cp models/product_detector.tflite ../neuralist_app/assets/models/
```

## Technologies

- **C++17** - Algorithm implementation
- **Python 3.13** - Training scripts
- **TensorFlow/PyTorch** - Training framework
- **TensorFlow Lite** - Model export for iOS
- **OpenCV** - Image processing (optional)
- **NumPy** - Data manipulation

## Getting Started

### 1. Set up Python environment
```bash
cd ml_algorithms
python3 -m venv venv
source venv/bin/activate
pip install tensorflow opencv-python numpy jupyter
```

### 2. Start developing
- Write algorithm in `src/`
- Train model in `training/`
- Export to `models/`
- Copy to app

## Examples

### Feature Extraction Algorithm (C++)
```cpp
// src/feature_extraction/color_histogram.cpp
#include <vector>

std::vector<double> extract_color_histogram(
    const unsigned char* image,
    int width,
    int height
) {
    // Your algorithm here
    std::vector<double> features(768); // RGB histogram
    // ... compute features
    return features;
}
```

### Training Script (Python)
```python
# training/train_product_recognition.py
import tensorflow as tf

model = tf.keras.Sequential([
    # Your model architecture
])

model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(train_data, epochs=10)
model.save('models/checkpoints/product_detector.h5')
```

### Export to TFLite
```python
# export/export_to_tflite.py
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open('models/product_detector.tflite', 'wb') as f:
    f.write(tflite_model)
```

## Current Status

### ✅ Completed
- [x] Folder structure created
- [x] Basic C++ algorithm framework
- [ ] Training pipeline
- [ ] Model export pipeline
- [ ] Benchmarking tools

### 🔄 In Development
- Color histogram feature extraction
- Product similarity matching
- Image preprocessing algorithms

### 📋 Planned
- YOLOv8 Nano for product detection
- MobileNet for feature extraction
- Custom lightweight models
- Performance optimization
- Quantization for mobile

## Development Cycle

```
┌─────────────────────────────────────┐
│   1. Research & Experiment          │
│      (notebooks/, src/)             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   2. Implement Algorithm (C++)      │
│      (src/feature_extraction/)      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   3. Train Model (Python)           │
│      (training/)                    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   4. Export for iOS (TFLite)        │
│      (export/ → models/)            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   5. Deploy to App                  │
│      (cp to neuralist_app/)         │
└─────────────────────────────────────┘
```

## Performance Goals

- **Training Speed**: <2 hours for full model
- **Model Size**: <5MB (TFLite)
- **Inference Time**: <50ms on iPhone
- **Accuracy**: >90% top-5 recognition

## Best Practices

1. **Version Control** - Tag model versions
2. **Documentation** - Document algorithm choices
3. **Testing** - Benchmark before deploying
4. **Optimization** - Profile and optimize
5. **Validation** - Validate accuracy on test set

## Resources

- [TensorFlow Lite Guide](https://www.tensorflow.org/lite)
- [TensorFlow Lite for iOS](https://www.tensorflow.org/lite/guide/ios)
- [Model Optimization](https://www.tensorflow.org/lite/performance/model_optimization)
- [YOLOv8](https://github.com/ultralytics/ultralytics)

## Notes

- This folder is for **development only**
- Final models go to `neuralist_app/assets/models/`
- Keep training data separate (large files)
- Use `.gitignore` for large files

---

**🧠 Focus: ML algorithm development and training**

**Output: Trained models ready for the app**
