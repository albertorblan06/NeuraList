# NeuralList - iOS App

**📱 This folder is for APP DEVELOPMENT only - NOT for ML development**

AI-powered visual shopping assistant for iPhone. This app uses pre-trained ML models and runs inference via native C/C++.

## 🍎 iOS-Only Development

This is an **iOS-exclusive** app built with Flutter and native C/C++. All documentation and setup is optimized for iPhone development.

## ⚠️ Important: ML vs App Development

**This folder (`neuralist_app/`):**
- ✅ iOS app development (Flutter UI, business logic)
- ✅ Model inference (loading and running pre-trained models)
- ✅ C++ inference code (NOT training or algorithm development)

**For ML development, go to `/ml_algorithms/`:**
- Training ML models
- Developing C/C++ algorithms
- Research and experiments
- Exporting models to TFLite

**Workflow:** Train model in `/ml_algorithms/` → Export to `.tflite` → Copy to `assets/models/` → Use here

## Features

- **📸 Visual Product Recognition**: Take photos of your fridge/pantry and identify products
- **⚡ C/C++ Powered Algorithms**: High-performance native code for image processing and ML
- **🧠 Smart Shopping Suggestions**: AI-driven recommendations based on your inventory
- **🛒 Product Database**: 500+ Mercadona products with complete information
- **🚀 Native Performance**: Critical algorithms written in C++ for maximum speed
- **🍎 iOS Native Experience**: Built specifically for iPhone

## Architecture

### Flutter + Native C/C++ Inference for iOS

```
┌─────────────────────────────────────┐
│      Flutter UI Layer (iOS)         │
│   (Dart - UI, State Management)     │
└────────────┬────────────────────────┘
             │ FFI (Foreign Function Interface)
┌────────────▼────────────────────────┐
│   Native C++ Inference Layer        │
│    (Compiled for iOS arm64/x86_64)  │
│  • Load pre-trained .tflite models  │
│  • Run inference on images          │
│  • Process camera frames            │
└────────────┬────────────────────────┘
             │ Uses
┌────────────▼────────────────────────┐
│     Pre-trained ML Models           │
│   (assets/models/*.tflite)          │
│  • Trained in /ml_algorithms/       │
│  • Exported and copied here         │
└─────────────────────────────────────┘
```

## Project Structure

```
neuralist_app/
├── lib/                              # Flutter/Dart code (iOS UI)
│   ├── main.dart                     # App entry point
│   ├── native/
│   │   └── neuralist_bindings.dart   # FFI bindings to C/C++
│   ├── services/
│   │   └── image_recognition_service.dart  # High-level image processing
│   ├── models/                       # Data models
│   ├── screens/                      # iOS screens
│   └── widgets/                      # Reusable widgets
│
├── native/                           # C/C++ INFERENCE ONLY (not training)
│   ├── CMakeLists.txt               # Build configuration
│   ├── build_ios.sh                 # iOS build script
│   ├── include/
│   │   └── neuralist_inference.h    # Inference API
│   └── src/
│       ├── inference/               # Model loading & inference
│       │   ├── model_loader.cpp     # Load .tflite models
│       │   └── tflite_runner.cpp    # Run inference
│       └── utils/                   # Helper utilities

├── assets/
│   └── models/                      # Pre-trained models
│       └── *.tflite                 # Copied from /ml_algorithms/models/
│
├── ios/                              # iOS-specific code
│   ├── Runner.xcworkspace            # Xcode workspace (OPEN THIS)
│   ├── Runner/
│   │   └── Info.plist               # Camera permissions ✅
│   ├── Frameworks/
│   │   └── libneuralist_native.dylib # Native library
│   └── Podfile                      # iOS dependencies
│
├── test/                             # Unit tests
└── pubspec.yaml                      # Flutter dependencies
```

## Quick Start

### Prerequisites

- macOS (required for iOS development)
- Xcode 15+ (with iOS 17+ SDK)
- Flutter SDK 3.24.5+
- CMake 3.10+
- iPhone or iOS Simulator

### Installation

**1. Open the project in Xcode:**
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app
open ios/Runner.xcworkspace
```

**2. Select an iPhone simulator** (top bar in Xcode)
   - iPhone 17 Pro (recommended)
   - Or connect your real iPhone

**3. Run the app:**
   - Press **Cmd+R** in Xcode
   - Or click the ▶️ Play button

**4. Start coding!**
   - Edit `lib/main.dart`
   - Save and see instant updates (Hot Reload)

## iOS Development

### Run on iPhone Simulator
```bash
# Using Flutter CLI
flutter run -d "iPhone 17 Pro"

# Using Xcode (Recommended)
open ios/Runner.xcworkspace
# Press Cmd+R
```

### Run on Real iPhone
1. Connect iPhone via USB
2. Open Xcode: `open ios/Runner.xcworkspace`
3. Select your iPhone in device list (top bar)
4. Press **Cmd+R**
5. Trust developer certificate on iPhone (Settings → General → VPN & Device Management)

### Building Native C++ Inference Layer for iOS
```bash
cd native
./build_ios.sh
cd ..
```

**When to rebuild C++ code:**
- After changing inference code in `native/src/`
- After modifying `.cpp` or `.h` files

**Note:** Algorithm development and training happens in `/ml_algorithms/`, not here!

## C/C++ Inference Layer (NOT Training)

**⚠️ Important:** This C++ code is for **inference only** - loading and running pre-trained models.

**For ML algorithm development, go to `/ml_algorithms/`**

### What the Inference Layer Does

**Model Loading (`native/src/inference/model_loader.cpp`):**
- Load `.tflite` models from `assets/models/`
- Initialize TensorFlow Lite interpreter
- Set up GPU acceleration (Metal delegate)

**Inference Execution (`native/src/inference/tflite_runner.cpp`):**
- Run inference on camera images
- Process model outputs
- Return predictions to Dart

### Workflow: From ML to App

```
1. Train model in /ml_algorithms/
   ↓
2. Export to .tflite in /ml_algorithms/models/
   ↓
3. Copy to neuralist_app/assets/models/
   ↓
4. Load model in native/src/inference/
   ↓
5. Run inference in app
```

### Adding Inference for a New Model

**1. Copy trained model:**
```bash
cp /ml_algorithms/models/product_detector.tflite assets/models/
```

**2. Load model in C++ (`native/src/inference/model_loader.cpp`):**
```cpp
#include "tensorflow/lite/c/c_api.h"

TfLiteModel* load_model(const char* model_path) {
    return TfLiteModelCreateFromFile(model_path);
}
```

**3. Run inference:**
```cpp
float* run_inference(TfLiteModel* model, const uint8_t* image);
```

**4. Rebuild for iOS:**
```bash
cd native && ./build_ios.sh
```

**5. Use from Dart (`lib/services/inference_service.dart`):**
```dart
final result = inferenceService.runModel(imageBytes);
```

## Development Workflow

### Using Xcode (Recommended)

**Daily workflow:**
```bash
# Morning: Open Xcode
open ios/Runner.xcworkspace

# Select iPhone 17 Pro simulator
# Press Cmd+R to run

# Edit Dart code in Xcode or VS Code
# Save (Cmd+S) → Hot Reload automatically!

# For C++ changes:
cd native && ./build_ios.sh
# Then restart app (Cmd+R in Xcode)
```

### Hot Reload
- Edit any `.dart` file
- Save (**Cmd+S**)
- Changes appear **instantly** (no rebuild!)
- Works for UI, logic, styling

### Hot Restart
- Press **R** in terminal
- Rebuilds entire app quickly
- Use when adding new files or changing app structure

## iOS Features

### Camera Integration ✅
- Camera access configured in Info.plist
- Photo library access enabled
- Save photos permission granted

**Note:** Camera features only work on **real iPhone**, not simulator!

### iOS Permissions (Already Configured)
- ✅ Camera Usage
- ✅ Photo Library Usage
- ✅ Photo Library Add Usage

### iOS Design
- Uses Cupertino widgets for native iOS look
- Supports Dark Mode
- Safe Area handling (notch, home indicator)
- iOS-style navigation

## Testing

### Run Tests
```bash
flutter test
```

### Test on Real Device
Camera and performance features should be tested on a real iPhone for best results.

## Building for Production

### Debug Build
```bash
flutter build ios --debug
```

### Release Build
```bash
flutter build ios --release
```

### Archive for App Store
1. Open Xcode: `open ios/Runner.xcworkspace`
2. Product → Archive
3. Distribute to App Store or TestFlight

## Performance

### Why C/C++ for Algorithms?

1. **Speed**: 10-100x faster than pure Dart for intensive tasks
2. **Memory Control**: Direct memory management for large image data
3. **Native Libraries**: Easy integration with iOS frameworks
4. **Optimization**: SIMD instructions, Metal GPU acceleration

### iOS-Specific Optimizations
- Universal binary (arm64 + x86_64)
- Metal framework support (GPU)
- iOS memory management
- Battery optimization

## Dependencies

### Flutter Packages
- **ffi**: Foreign Function Interface for C/C++
- **camera**: iOS camera access
- **image_picker**: Photo selection from library
- **image**: Image manipulation
- **sqflite**: Local SQLite database
- **provider**: State management
- **http**: API requests
- **json_serializable**: JSON handling

### Native (C/C++)
- Standard C++ Library (17)
- iOS SDK frameworks
- Future: TensorFlow Lite for iOS
- Future: Accelerate framework (Apple's optimized math)

## Documentation

- **📱 START_HERE_IOS.md** - Quick start guide (read this first!)
- **🍎 IOS_DEVELOPMENT.md** - Complete iOS development guide
- **🛠️ DEVELOPMENT.md** - General development guide
- **📖 README.md** - This file

## Roadmap

### Phase 1: Core iOS Features ✅
- [x] iOS project setup
- [x] FFI integration with C/C++
- [x] Camera permissions configured
- [x] Basic algorithms (image processing, matching)
- [ ] Camera screen implementation
- [ ] Product database integration

### Phase 2: Product Recognition
- [ ] Camera capture workflow
- [ ] Image preprocessing in C++
- [ ] Feature extraction
- [ ] Product matching against database
- [ ] Results display

### Phase 3: Shopping Features
- [ ] Shopping list management
- [ ] Smart suggestions
- [ ] Inventory tracking
- [ ] Price tracking

### Phase 4: Polish & Publish
- [ ] iOS UI polish (Cupertino design)
- [ ] Performance optimization
- [ ] Battery optimization
- [ ] App Store submission

## Troubleshooting

### Build Errors
```bash
flutter clean
flutter pub get
cd ios
pod install
cd ..
flutter run
```

### Native Library Errors
```bash
cd native
./build_ios.sh
cd ..
```

### Xcode Issues
```bash
# Clean in Xcode
# Xcode → Product → Clean Build Folder
# Or press: Cmd+Shift+K
```

### Camera Not Working
- Camera only works on real iPhone (not simulator)
- Check Info.plist has camera permissions ✅
- Test on physical device

## Resources

### Apple Documentation
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [iOS Developer Documentation](https://developer.apple.com/documentation/)

### Flutter for iOS
- [Flutter iOS Setup](https://docs.flutter.dev/get-started/install/macos#ios-setup)
- [Platform-Specific Code](https://docs.flutter.dev/platform-integration/platform-channels)
- [iOS Deployment](https://docs.flutter.dev/deployment/ios)

### Project Resources
- [Flutter FFI Documentation](https://dart.dev/guides/libraries/c-interop)
- [CMake Documentation](https://cmake.org/documentation/)

## License

This project is part of the NeuralList application.

---

**🍎 Built exclusively for iOS**

Get started: `open ios/Runner.xcworkspace` then press **Cmd+R**
