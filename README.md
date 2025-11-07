# NeuralList: AI-Powered Visual Shopping Assistant

**🍎 iOS-Focused | Clear Separation: ML Development vs App Development**

## 🎯 Project Structure

This project is organized into **three independent areas**:

```
NeuraList/
│
├── 🧠 ml_algorithms/      # ML/AI Development - TRAIN MODELS HERE
├── 📱 neuralist_app/      # iOS App - USE MODELS HERE (NO ML DEV)
└── 🛒 scraper/            # Product Database
```

### 🧠 ml_algorithms/ - Where You Develop ML

- **Train** ML models
- **Develop** C/C++ algorithms
- **Research** and experiment
- **Export** trained models

### 📱 neuralist_app/ - Where You Build the App

- **Build** iOS UI
- **Implement** business logic
- **Load** pre-trained models
- **Run** inference only

### 🛒 scraper/ - Where Product Data Lives

- **Scrape** Mercadona products
- **Maintain** product database (500+ products)

---

## 1. The Problem

Standard shopping list applications act merely as "digital paper." They rely on generic text input (e.g., "milk," "tomato sauce") that lacks context, leading to friction during the actual shopping process. They don't know what the product looks like, where it is located, or exactly which specific SKU the user intends to buy among dozens of similar options.

The cognitive load of finding products in a massive, visually noisy supermarket environment remains entirely on the user.

## 2. The Solution (Project Vision)

NeuralList aims to bridge the gap between standard list management and real-world execution by applying Computer Vision (CV) and Natural Language Processing (NLP) to the shopping experience.

Instead of just sorting items alphabetically or by rough categories, the application aims to be "spatial-aware" and "visually intelligent." The ultimate goal is an assistant that can "see" the supermarket shelves through the camera feed and actively highlight the products currently on your list, effectively bringing Edge AI to a mundane daily task.

## 3. Core Pillars & Technical Expectations

### 3.1. Intelligent Intent Translation (NLP & Search)

Users rarely type full product names. The system must translate vague intent into concrete data.

- **Functionality**: When a user types "semi milk", the system won't just save that string. It will query a structured dataset (e.g., scraped from major retailers like Mercadona) using fuzzy search or vector embeddings to suggest the actual target SKU: "Hacendado Semi-Skimmed Milk, 1L Brick".

- **Value**: This ensures every item on the list is tied to a real image, price, and EAN code, essential for the subsequent visual recognition steps.

### 3.2. Real-Time Visual Recognition (Computer Vision)

Moving beyond simple barcode scanning, this module is the core R&D challenge of the project.

- **Phase 1 (Deterministic)**: High-performance native barcode scanning for quick ground-truth verification.

- **Phase 2 (Probabilistic - Edge AI)**: Implementation of lightweight Object Detection models (e.g., YOLOv8 Nano, MobileNet SSD) running on-device via TensorFlow Lite. The goal is to recognize specific product packaging in the live camera feed as the user walks down the aisle.

- **Performance Note**: To achieve real-time frame rates without destroying battery life, critical pre-processing steps are offloaded to native C++ layers accessed via Dart FFI.

### 3.3. Indoor Localization & Mapping (Visual SLAM)

A long-term research goal is to remove the need for manual aisle sorting.

- **Concept**: By leveraging smartphone visual sensors (camera + IMU), the app could potentially perform basic Visual SLAM (Simultaneous Localization and Mapping) to recognize distinct supermarket zones (e.g., "Dairy Section", "Bakery") based on visual features, automatically ordering the list based on the user's real-time path through the store.

## 4. Tech Stack

### ML Development (ml_algorithms/)
- **C++17** - Algorithm implementation
- **Python 3.13** - Training scripts
- **TensorFlow/PyTorch** - Training frameworks
- **TensorFlow Lite** - Model export for iOS
- **OpenCV** - Image processing
- **NumPy** - Data manipulation

### App Development (neuralist_app/)
- **Flutter (Dart)** - iOS UI framework
- **C++ via FFI** - Inference layer (loads and runs models)
- **TensorFlow Lite for iOS** - On-device inference
- **Swift/Objective-C** - iOS platform code
- **SQLite** - Local product database

### Data (scraper/)
- **Python 3.13** - Web scraping
- **Requests** - HTTP library
- **SQLAlchemy** - Database ORM
- **SQLite** - Product storage

## 5. Complete Project Structure

```
NeuraList/
│
├── 🧠 ml_algorithms/                    # ML/AI DEVELOPMENT
│   ├── training/                        # Training scripts
│   │   ├── train_product_recognition.py
│   │   ├── train_feature_extractor.py
│   │   ├── datasets/                    # Training data
│   │   └── notebooks/                   # Jupyter experiments
│   │
│   ├── models/                          # EXPORTED MODELS
│   │   ├── product_detector.tflite     # ← Deploy this to app
│   │   ├── feature_extractor.tflite
│   │   └── checkpoints/                 # Training checkpoints
│   │
│   ├── src/                             # C++ ALGORITHMS
│   │   ├── feature_extraction/
│   │   ├── product_matching/
│   │   ├── preprocessing/
│   │   └── algorithms/                  # Your algorithms
│   │
│   ├── export/                          # Model export
│   │   ├── export_to_tflite.py
│   │   └── optimize_model.py
│   │
│   └── README.md                        # ML dev guide
│
├── 📱 neuralist_app/                    # iOS APP
│   ├── ios/
│   │   └── Runner.xcworkspace           # ⭐ OPEN IN XCODE
│   │
│   ├── lib/                             # Flutter UI
│   │   ├── main.dart
│   │   ├── screens/
│   │   ├── widgets/
│   │   └── services/
│   │
│   ├── native/                          # C++ INFERENCE ONLY
│   │   ├── build_ios.sh
│   │   ├── include/
│   │   │   └── neuralist_inference.h
│   │   └── src/
│   │       ├── inference/               # Load & run models
│   │       └── utils/
│   │
│   ├── assets/
│   │   └── models/                      # Pre-trained models here
│   │       └── product_detector.tflite # ← Copy from ml_algorithms
│   │
│   └── README.md                        # App guide
│
└── 🛒 scraper/                          # PRODUCT DATA
    ├── scraper.py
    ├── data/products.db                 # 500 products
    └── README.md
```

## 6. Development Workflow

### Complete ML → App Pipeline

```
1. Develop Algorithm (ml_algorithms/src/)
   ↓
2. Train Model (ml_algorithms/training/)
   ↓
3. Export to TFLite (ml_algorithms/export/)
   ↓ creates: ml_algorithms/models/product_detector.tflite
   ↓
4. Copy to App (neuralist_app/assets/models/)
   ↓
5. Code Inference (neuralist_app/native/src/)
   ↓
6. Build iOS App (neuralist_app/ios/)
   ↓
7. Test on iPhone
```

### Commands

```bash
# ML Development
cd ml_algorithms
python training/train_model.py        # Train
python export/export_to_tflite.py     # Export
cp models/product_detector.tflite ../neuralist_app/assets/models/

# App Development
cd neuralist_app
cd native && ./build_ios.sh           # Build C++
open ios/Runner.xcworkspace            # Open Xcode
# Press Cmd+R in Xcode

# Data
cd scraper
source venv/bin/activate
python3 scraper.py
```

## 7. Getting Started

### For ML Development:
```bash
cd ml_algorithms
cat README.md                # Read ML guide
# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install tensorflow numpy opencv-python
```

### For App Development:
```bash
cd neuralist_app
cat START_HERE_IOS.md        # Read quick start
open ios/Runner.xcworkspace  # Open Xcode
# Press Cmd+R
```

### For Product Data:
```bash
cd scraper
cat README.md                # Read scraper guide
```

## 8. Development Status

### ✅ Completed
- [x] Project structure (ML separate from app)
- [x] iOS app setup with C++ FFI
- [x] Product database scraper (500 products)
- [x] iOS camera permissions configured
- [x] Build system (CMake for C++)
- [x] Documentation structure

### 🔄 In Progress
- [ ] ML algorithm development
- [ ] Model training pipeline
- [ ] TensorFlow Lite integration
- [ ] Camera screen implementation
- [ ] Product database integration with app

### 📋 Planned
- [ ] Train product detection model
- [ ] Export to TFLite
- [ ] Implement inference layer
- [ ] Real-time product recognition
- [ ] Shopping list management
- [ ] Smart suggestions
- [ ] App Store submission

## 9. Key Principles

### Clear Separation

```
ml_algorithms/   →  Develops and trains models
                    Exports .tflite files

neuralist_app/   →  Loads pre-trained models
                    Runs inference only
                    Builds iOS UI

scraper/         →  Provides product data
```

### One-Way Dependencies

```
ml_algorithms/  (independent)
      ↓ exports models
neuralist_app/  (uses models)
      ↓ uses data
scraper/        (provides data)
```

### Focus Areas

**As ML Engineer:** Work in `ml_algorithms/`
**As App Developer:** Work in `neuralist_app/`
**As Both:** Train in `ml_algorithms/`, deploy to `neuralist_app/`

## 10. Documentation

### Project-Wide:
- **README.md** (this file) - Project vision
- **PROJECT_STRUCTURE.md** - Detailed structure guide

### ML Development:
- **ml_algorithms/README.md** - ML development guide
- **ml_algorithms/docs/** - Algorithm documentation

### App Development:
- **neuralist_app/START_HERE_IOS.md** - Quick start
- **neuralist_app/IOS_DEVELOPMENT.md** - Complete iOS guide
- **neuralist_app/README.md** - App overview
- **neuralist_app/native/README.md** - Inference guide

### Data:
- **scraper/README.md** - Scraper documentation

## 11. Performance Goals

- **Training**: <2 hours for full model
- **Model Size**: <5MB (TFLite, quantized)
- **Inference**: <50ms on iPhone
- **Frame Processing**: <30ms (30+ FPS)
- **Accuracy**: >90% top-5 recognition
- **Battery**: <10% per hour active use
- **Memory**: <200MB peak usage

## 12. Architecture Overview

```
┌─────────────────────────────────────┐
│     Flutter iOS App UI              │
│  (neuralist_app/lib/)               │
└───────────────┬─────────────────────┘
                │ Dart FFI
┌───────────────▼─────────────────────┐
│   C++ Inference Layer               │
│  (neuralist_app/native/)            │
│  • Load .tflite models              │
│  • Run TensorFlow Lite              │
│  • Preprocess images                │
└───────────────┬─────────────────────┘
                │ Uses
┌───────────────▼─────────────────────┐
│   Pre-trained Models                │
│  (neuralist_app/assets/models/)     │
│  • product_detector.tflite          │
│  • feature_extractor.tflite         │
└───────────────┬─────────────────────┘
                │ Trained in
┌───────────────▼─────────────────────┐
│   ML Development                    │
│  (ml_algorithms/)                   │
│  • Algorithm research               │
│  • Model training                   │
│  • Model export                     │
└─────────────────────────────────────┘
```

## 13. Resources

### ML Development
- [TensorFlow](https://www.tensorflow.org/)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
- [YOLOv8](https://github.com/ultralytics/ultralytics)

### iOS Development
- [Flutter Documentation](https://docs.flutter.dev/)
- [TensorFlow Lite for iOS](https://www.tensorflow.org/lite/guide/ios)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Tools
- [Xcode](https://developer.apple.com/xcode/)
- [CMake](https://cmake.org/)

## 14. Contributing

This is currently a single-developer project.

**Development environment:**
- macOS (required for iOS)
- Xcode 15+
- Flutter SDK 3.24.5+
- Python 3.13
- CMake 4.1+

## 15. License

This project is part of the NeuralList application.

---

**🎯 Clear Structure. Clear Purpose.**

**ML Development: `/ml_algorithms/`**
**App Development: `/neuralist_app/`**
**Product Data: `/scraper/`**

**Quick commands:**
```bash
# ML
cd ml_algorithms && python training/train_model.py

# App
cd neuralist_app && open ios/Runner.xcworkspace

# Data
cd scraper && python3 scraper.py
```
