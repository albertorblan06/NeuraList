# Project Structure - NeuralList iOS

## 🍎 iOS-Focused Project Layout

This document explains the project structure for **iOS-only development**.

## 📂 Main Project Structure

```
neuralist_app/                           # Root directory
│
├── 📱 ios/                              # iOS PLATFORM (PRIMARY)
│   ├── Runner.xcworkspace              # ⭐ OPEN THIS in Xcode
│   ├── Runner/
│   │   ├── AppDelegate.swift           # iOS app lifecycle
│   │   ├── Info.plist                  # Camera permissions ✅
│   │   └── Assets.xcassets             # iOS app icons
│   ├── Frameworks/
│   │   └── libneuralist_native.dylib   # Native C++ library ✅
│   ├── Podfile                         # iOS dependencies
│   └── Runner.xcodeproj/               # Xcode project files
│
├── 📝 lib/                              # FLUTTER/DART CODE (YOUR MAIN CODE)
│   ├── main.dart                       # ⭐ App entry point - START HERE
│   │
│   ├── screens/                        # Full-screen pages
│   │   ├── home_screen.dart           # Main screen
│   │   ├── camera_screen.dart         # Camera UI
│   │   ├── products_screen.dart       # Product browser
│   │   └── shopping_list_screen.dart  # Shopping list
│   │
│   ├── widgets/                        # Reusable UI components
│   │   ├── product_card.dart          # Product display widget
│   │   ├── shopping_item.dart         # Shopping list item
│   │   └── camera_overlay.dart        # Camera UI overlay
│   │
│   ├── models/                         # Data structures
│   │   ├── product.dart               # Product data model
│   │   ├── shopping_list.dart         # Shopping list model
│   │   └── inventory.dart             # User inventory model
│   │
│   ├── services/                       # Business logic
│   │   ├── image_recognition_service.dart  # C++ FFI wrapper
│   │   ├── database_service.dart      # SQLite operations
│   │   ├── camera_service.dart        # Camera operations
│   │   └── shopping_service.dart      # Shopping list logic
│   │
│   └── native/                         # FFI Bindings
│       └── neuralist_bindings.dart    # C++ interface
│
├── ⚙️ native/                           # C/C++ ALGORITHMS
│   ├── build_ios.sh                   # ⭐ iOS build script
│   ├── build.sh                       # macOS build script (for testing)
│   ├── CMakeLists.txt                 # Build configuration
│   │
│   ├── include/                        # C++ Headers
│   │   └── neuralist_native.h         # Public C++ API
│   │
│   ├── src/                            # C++ Implementation
│   │   ├── neuralist_native.cpp       # Main implementation
│   │   └── algorithms/                # Your C++ algorithms
│   │       ├── image_processing.cpp   # Image feature extraction
│   │       └── product_matcher.cpp    # Product matching
│   │
│   └── build_ios/                      # Build output (generated)
│
├── 🧪 test/                            # Unit tests
│   └── widget_test.dart               # Example test
│
├── 📄 Configuration Files
│   ├── pubspec.yaml                   # Flutter dependencies
│   ├── analysis_options.yaml          # Dart linter config
│   └── .gitignore                     # Git ignore rules
│
├── 📖 Documentation
│   ├── README.md                      # Main project README
│   ├── START_HERE_IOS.md              # ⭐ Quick start guide
│   ├── IOS_DEVELOPMENT.md             # Complete iOS guide
│   ├── DEVELOPMENT.md                 # Development workflows
│   └── PROJECT_STRUCTURE.md           # This file
│
└── ⚠️ Other Platforms (Not Actively Used)
    ├── android/                       # Android (ignore)
    └── macos/                         # macOS (for testing C++ only)
```

## 🎯 What You Need to Know

### 📱 iOS Development (Your Focus)
```
ios/
└── Runner.xcworkspace  ← Open this in Xcode
```

### 📝 Flutter Code (Where You Write UI)
```
lib/
├── main.dart           ← Start here
├── screens/            ← Create screens
├── widgets/            ← Create widgets
└── services/           ← Business logic
```

### ⚙️ C++ Algorithms (High Performance Code)
```
native/
├── build_ios.sh        ← Build for iOS
├── include/            ← C++ headers
└── src/algorithms/     ← Your algorithms
```

## 📋 File Types Explained

### Dart Files (`.dart`)
**Location:** `lib/`
**Purpose:** Flutter UI and app logic
**Edit with:** Xcode or VS Code
**Hot Reload:** ✅ Yes (instant updates)

```dart
// lib/main.dart
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}
```

### C++ Files (`.cpp`, `.h`)
**Location:** `native/src/`, `native/include/`
**Purpose:** High-performance algorithms
**Edit with:** Xcode or VS Code
**Rebuild Required:** ✅ Yes (`cd native && ./build_ios.sh`)

```cpp
// native/src/algorithms/my_algorithm.cpp
int process_data(const double* input, int size) {
    // Your fast C++ code
}
```

### iOS Configuration (`.plist`, `.swift`)
**Location:** `ios/Runner/`
**Purpose:** iOS-specific settings
**Edit with:** Xcode
**Example:** Camera permissions in Info.plist

### Build Files (Generated)
**Don't edit these:**
- `.dart_tool/` - Dart build cache
- `build/` - Build output
- `native/build_ios/` - C++ build output
- `.flutter-plugins` - Generated plugin list

## 🚀 Development Workflows

### UI Development (Daily)
```
1. Open: open ios/Runner.xcworkspace
2. Edit: lib/main.dart or lib/screens/*.dart
3. Save: Cmd+S
4. Result: Instant Hot Reload! ⚡
```

### C++ Algorithm Development
```
1. Edit: native/src/algorithms/*.cpp
2. Build: cd native && ./build_ios.sh
3. Restart: Cmd+R in Xcode
4. Test: Run app on simulator or device
```

### Adding New Features
```
1. Create screen: lib/screens/my_screen.dart
2. Create widget: lib/widgets/my_widget.dart
3. Add to navigation: Update main.dart
4. Hot Reload: Cmd+S
```

## 📁 Directory Purposes

### `/ios` - iOS Platform Code
- Xcode workspace and project
- iOS app configuration
- Native frameworks
- Platform-specific code

**Open in Xcode:**
```bash
open ios/Runner.xcworkspace
```

### `/lib` - Flutter Application Code
- All Dart code
- UI components
- Business logic
- FFI bindings

**Primary development area for UI**

### `/native` - C++ Native Code
- High-performance algorithms
- Image processing
- Product matching
- ML inference (future)

**Build with:**
```bash
cd native && ./build_ios.sh
```

### `/test` - Unit Tests
- Widget tests
- Integration tests
- C++ tests (future)

**Run with:**
```bash
flutter test
```

## 🔗 How Components Connect

```
┌─────────────────────────────────────┐
│  iOS App (Runner.xcworkspace)       │
│  ┌───────────────────────────────┐  │
│  │ Flutter UI (lib/)             │  │
│  │  ├─ Screens                   │  │
│  │  ├─ Widgets                   │  │
│  │  └─ Services                  │  │
│  │      │                        │  │
│  │      ├─ FFI Bindings          │  │
│  │      │  (neuralist_bindings)  │  │
│  │      ▼                        │  │
│  │  ┌──────────────────────┐    │  │
│  │  │ Native C++ Library   │    │  │
│  │  │ (libneuralist_native)│    │  │
│  │  │  • Image Processing  │    │  │
│  │  │  • Product Matching  │    │  │
│  │  └──────────────────────┘    │  │
│  └───────────────────────────────┘  │
│                                     │
│  iOS Frameworks & Camera            │
└─────────────────────────────────────┘
```

## 📊 File Count Overview

```
lib/          ~20-50 files   (Your Dart code)
native/src/   ~5-10 files    (Your C++ code)
ios/          ~50+ files     (iOS platform, mostly auto-generated)
test/         ~5-20 files    (Your tests)
```

## 🎨 Typical Project Evolution

### Phase 1: Basic Structure (Current)
```
lib/
└── main.dart (demo app)
```

### Phase 2: Add Screens
```
lib/
├── main.dart
└── screens/
    ├── home_screen.dart
    ├── camera_screen.dart
    └── products_screen.dart
```

### Phase 3: Add Services
```
lib/
├── main.dart
├── screens/
└── services/
    ├── camera_service.dart
    ├── database_service.dart
    └── image_recognition_service.dart
```

### Phase 4: Add C++ Integration
```
lib/
├── screens/
├── services/
└── native/
    └── neuralist_bindings.dart ←→ native/src/algorithms/
```

## 🗂️ Where to Put New Files

### New UI Screen?
```
lib/screens/my_new_screen.dart
```

### New Widget?
```
lib/widgets/my_widget.dart
```

### New Data Model?
```
lib/models/my_model.dart
```

### New Service/Logic?
```
lib/services/my_service.dart
```

### New C++ Algorithm?
```
native/src/algorithms/my_algorithm.cpp
native/include/neuralist_native.h (add declaration)
```

### New Test?
```
test/my_test.dart
```

## 🚫 What NOT to Edit

**Generated/Build Files:**
- `.dart_tool/`
- `build/`
- `ios/Flutter/` (auto-generated)
- `ios/Pods/` (CocoaPods dependencies)
- `.flutter-plugins`
- `.flutter-plugins-dependencies`

**Platform Boilerplate (usually):**
- `ios/Runner/AppDelegate.swift` (unless adding native features)
- `ios/Runner.xcodeproj/` (use Xcode UI instead)

## 💡 Quick Navigation

### I want to...

**Change the app UI:**
→ Edit `lib/screens/*.dart`

**Add a new screen:**
→ Create `lib/screens/new_screen.dart`

**Improve performance with C++:**
→ Edit `native/src/algorithms/*.cpp`

**Configure iOS permissions:**
→ Edit `ios/Runner/Info.plist`

**Add Flutter package:**
→ Edit `pubspec.yaml`, run `flutter pub get`

**Run the app:**
→ `open ios/Runner.xcworkspace`, press Cmd+R

**Build native code:**
→ `cd native && ./build_ios.sh`

**Run tests:**
→ `flutter test`

## 📚 Related Documentation

- **Quick Start:** `START_HERE_IOS.md`
- **iOS Development:** `IOS_DEVELOPMENT.md`
- **Main README:** `README.md`
- **Development Guide:** `DEVELOPMENT.md`

---

**🍎 Focused on iOS development**

Your main areas:
1. `ios/Runner.xcworkspace` - Open in Xcode
2. `lib/` - Write your Flutter code here
3. `native/` - Write your C++ algorithms here
