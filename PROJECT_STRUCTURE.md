# NeuralList - Complete Project Structure

**🍎 iOS-Focused | Clear Separation of Concerns**

## 🎯 Three Main Areas

```
NeuraList/
│
├── 🧠 ml_algorithms/          # ML/AI Development (YOU CODE ALGORITHMS HERE)
├── 📱 neuralist_app/          # iOS App (YOU CODE APP HERE - NO ML)
└── 🛒 scraper/                # Product Database
```

## 📂 Complete Structure

```
NeuraList/
│
├── 🧠 ml_algorithms/                    # ML/AI DEVELOPMENT
│   ├── training/                        # Training scripts
│   │   ├── train_product_recognition.py
│   │   ├── train_feature_extractor.py
│   │   ├── datasets/                    # Training data
│   │   └── notebooks/                   # Jupyter notebooks
│   │
│   ├── models/                          # EXPORTED MODELS
│   │   ├── product_detector.tflite     # Ready for app
│   │   ├── feature_extractor.tflite
│   │   └── checkpoints/                 # Training checkpoints
│   │
│   ├── src/                             # C++ ALGORITHM CODE
│   │   ├── feature_extraction/
│   │   ├── product_matching/
│   │   ├── preprocessing/
│   │   └── algorithms/                  # Your algorithms
│   │
│   ├── export/                          # Model export tools
│   │   ├── export_to_tflite.py
│   │   └── optimize_model.py
│   │
│   └── docs/                            # Algorithm docs
│       ├── architecture.md
│       └── training_guide.md
│
├── 📱 neuralist_app/                    # iOS APP (NO ML DEVELOPMENT)
│   │
│   ├── ios/                             # iOS PLATFORM
│   │   └── Runner.xcworkspace           # ⭐ OPEN IN XCODE
│   │
│   ├── lib/                             # FLUTTER UI CODE
│   │   ├── main.dart                    # App entry
│   │   ├── screens/                     # UI screens
│   │   ├── widgets/                     # UI components
│   │   ├── services/                    # Business logic
│   │   └── native/                      # FFI bindings
│   │
│   ├── native/                          # C++ INFERENCE ONLY
│   │   ├── build_ios.sh                 # Build for iOS
│   │   ├── include/
│   │   │   └── neuralist_inference.h   # Inference API
│   │   └── src/
│   │       ├── inference/               # Load & run models
│   │       └── utils/                   # Utilities
│   │
│   ├── assets/                          # APP ASSETS
│   │   └── models/                      # Pre-trained models
│   │       ├── product_detector.tflite # Copied from ml_algorithms
│   │       └── feature_extractor.tflite
│   │
│   ├── test/                            # Tests
│   │
│   └── Documentation
│       ├── README.md                    # App overview
│       ├── START_HERE_IOS.md            # Quick start
│       └── IOS_DEVELOPMENT.md           # Complete guide
│
└── 🛒 scraper/                          # PRODUCT DATABASE
    ├── scraper.py                       # Mercadona scraper
    ├── data/
    │   └── products.db                  # 500 products
    └── README.md
```

## 🎓 What Goes Where

### 🧠 ml_algorithms/ - ML Development

**YOU CODE HERE:**
- ✅ Training ML models
- ✅ Developing C/C++ algorithms
- ✅ Research and experiments
- ✅ Exporting models to TFLite

**OUTPUTS:**
- Trained models (`.tflite` files)
- Algorithm implementations
- Performance benchmarks

**WORKFLOW:**
```bash
cd ml_algorithms
# 1. Develop algorithm in src/
# 2. Train model in training/
# 3. Export to models/
# 4. Copy to neuralist_app/assets/models/
```

### 📱 neuralist_app/ - iOS App

**YOU CODE HERE:**
- ✅ Flutter UI (screens, widgets)
- ✅ Business logic (services)
- ✅ C++ inference code (load & run models)
- ✅ App configuration

**DO NOT CODE HERE:**
- ❌ ML training
- ❌ Algorithm development
- ❌ Model export

**WORKFLOW:**
```bash
cd neuralist_app
# 1. Code UI in lib/
# 2. Code inference in native/src/
# 3. Load models from assets/models/
# 4. Build and run in Xcode
```

### 🛒 scraper/ - Product Data

**PURPOSE:**
- Scrape product information
- Maintain product database
- Export data for app

**WORKFLOW:**
```bash
cd scraper
# 1. Run scraper.py
# 2. Get products.db
# 3. Copy to app if needed
```

## 🔄 Complete Workflow

```
┌─────────────────────────────────────┐
│  1. Develop ML Algorithm            │
│     ml_algorithms/src/              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Train Model                     │
│     ml_algorithms/training/         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Export to TFLite                │
│     ml_algorithms/export/           │
│     → models/product_detector.tflite│
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. Copy to App                     │
│     cp to neuralist_app/assets/     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  5. Code Inference Layer            │
│     neuralist_app/native/src/       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  6. Build iOS App                   │
│     neuralist_app/ios/              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  7. Test on iPhone                  │
│     Xcode → Cmd+R                   │
└─────────────────────────────────────┘
```

## 📋 Quick Reference

### I want to...

**Train a ML model:**
→ `cd ml_algorithms/training`

**Develop algorithm:**
→ `cd ml_algorithms/src`

**Export model:**
→ `cd ml_algorithms/export`

**Code app UI:**
→ `cd neuralist_app/lib`

**Code inference:**
→ `cd neuralist_app/native/src`

**Run app:**
→ `open neuralist_app/ios/Runner.xcworkspace`

**Scrape products:**
→ `cd scraper && python3 scraper.py`

## 🎯 Key Principles

### Separation of Concerns

1. **ML Development** (ml_algorithms/)
   - Research
   - Training
   - Algorithm development
   - Model export

2. **App Development** (neuralist_app/)
   - UI/UX
   - Business logic
   - Model inference (using pre-trained models)
   - iOS integration

3. **Data** (scraper/)
   - Product information
   - Database maintenance

### Clear Boundaries

```
ml_algorithms/        →  Creates models
neuralist_app/        →  Uses models
scraper/              →  Provides data
```

### One-Way Dependencies

```
ml_algorithms/  (independent)
      ↓
neuralist_app/  (depends on ml_algorithms outputs)
      ↓
User's iPhone
```

## 🚀 Getting Started

### Day 1: ML Development
```bash
cd ml_algorithms
# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install tensorflow numpy opencv-python

# Start developing
```

### Day 1: App Development
```bash
cd neuralist_app
# Open Xcode
open ios/Runner.xcworkspace
# Press Cmd+R
```

## 📚 Documentation Map

### For ML Development:
- `/ml_algorithms/README.md` - ML development guide
- `/ml_algorithms/docs/` - Algorithm documentation

### For App Development:
- `/neuralist_app/START_HERE_IOS.md` - Quick start
- `/neuralist_app/IOS_DEVELOPMENT.md` - Complete guide
- `/neuralist_app/README.md` - App overview
- `/neuralist_app/native/README.md` - Inference guide

### For Data:
- `/scraper/README.md` - Scraper documentation

### Project Overview:
- `/README.md` - Project vision
- `/PROJECT_STRUCTURE.md` - This file

## 🔑 Key Concepts

### Models Flow
```
Develop → Train → Export → Deploy → Inference
(ML)      (ML)    (ML)     (Copy)   (App)
```

### Code Organization
```
ml_algorithms/
  ├── Algorithm research & development
  ├── Model training
  └── Model export

neuralist_app/
  ├── UI development
  ├── Business logic
  └── Model inference (use only)
```

## ⚠️ Common Mistakes to Avoid

❌ **Don't** train models in the app folder
✅ **Do** train in ml_algorithms/

❌ **Don't** develop algorithms in app/native
✅ **Do** develop in ml_algorithms/src/

❌ **Don't** put training code in the app
✅ **Do** keep it in ml_algorithms/training/

❌ **Don't** mix ML development with app development
✅ **Do** keep them separate and clean

## 📊 Folder Sizes (Expected)

```
ml_algorithms/     ~500MB-5GB (datasets, models)
neuralist_app/     ~50-100MB (app code only)
scraper/           ~10-50MB (database)
```

## 🎯 Focus Areas

### As ML Engineer:
→ Work in `ml_algorithms/`

### As App Developer:
→ Work in `neuralist_app/`

### As Both:
1. Morning: Train model in `ml_algorithms/`
2. Export model
3. Afternoon: Use model in `neuralist_app/`

## 💡 Pro Tips

1. **Keep them separate** - Don't mix ML and app code
2. **Version models** - Tag model versions in ml_algorithms/models/
3. **Test before deploy** - Validate models before copying to app
4. **Document everything** - Keep docs updated
5. **Use git tags** - Tag stable model versions

## 🔧 Build Commands

### ML Development
```bash
cd ml_algorithms
source venv/bin/activate
python training/train_model.py
python export/export_to_tflite.py
```

### App Development
```bash
cd neuralist_app
cd native && ./build_ios.sh  # Build C++
open ios/Runner.xcworkspace   # Open Xcode
```

---

**🎯 Clear structure. Clear purpose. No confusion.**

**ML Development: `/ml_algorithms/`**
**App Development: `/neuralist_app/`**
**Data: `/scraper/`**
