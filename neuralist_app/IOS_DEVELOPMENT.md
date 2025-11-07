# iOS Development Guide - NeuralList

**📱 This is the APP development guide - For ML development, see `/ml_algorithms/README.md`**

## 🍎 iOS-Only Development Setup

You're developing exclusively for iOS - this simplifies everything!

## ⚠️ Important Separation

This folder is for **iOS app development** only:
- ✅ Flutter UI and business logic
- ✅ Model inference (loading/running pre-trained models)
- ❌ NOT for ML training or algorithm development

For ML work: go to `/ml_algorithms/`

## 🚀 Quick Start (3 Steps)

### 1. Open in Xcode
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app
open ios/Runner.xcworkspace
```

### 2. Select Target
- In Xcode, select **"iPhone 17 Pro"** simulator (top bar)
- Or connect your iPhone and select it

### 3. Run!
- Press **Cmd+R** in Xcode
- Or click the ▶️ Play button

## 💻 Development Tools

### Option A: Xcode (Recommended for iOS)
Best for:
- iOS-specific features
- Interface Builder
- Debugging C++ code
- Performance profiling
- Publishing to App Store

### Option B: VS Code + Xcode
Best for:
- Fast Flutter/Dart editing
- Use VS Code for `lib/` folder
- Use Xcode for iOS-specific and C++ debugging

## 📁 Your iOS Project Structure

```
neuralist_app/
│
├── lib/                          ← Flutter/Dart code
│   ├── main.dart                ← Edit in VS Code or Xcode
│   ├── screens/
│   ├── widgets/
│   └── services/
│
├── ios/                          ← iOS-specific
│   ├── Runner.xcworkspace       ← OPEN THIS in Xcode
│   ├── Runner/
│   │   └── Info.plist           ← iOS permissions ✅
│   ├── Frameworks/              ← Native C++ library goes here
│   └── Podfile                  ← iOS dependencies
│
├── native/                       ← C++ INFERENCE (not training)
│   ├── build_ios.sh             ← Build for iOS
│   ├── include/
│   └── src/
│       ├── inference/           ← Load/run models
│       └── utils/               ← Helpers
│
├── assets/
│   └── models/                  ← Pre-trained .tflite models
└── (For ML development: /ml_algorithms/)
```

## 🔄 Development Workflow

### Method 1: Pure Xcode (Simplest)

1. **Open Xcode:**
   ```bash
   open ios/Runner.xcworkspace
   ```

2. **Edit Dart code:**
   - Navigate to `lib/main.dart` in Xcode sidebar
   - Edit directly in Xcode
   - Press **Cmd+R** to run

3. **Hot Reload in Xcode:**
   - After running app, save any `.dart` file
   - Press **r** in Xcode console for hot reload
   - Press **R** for hot restart

### Method 2: VS Code + Xcode (Advanced)

**Terminal 1 (VS Code):**
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app
code .
flutter run
```
- Edit Flutter code in VS Code
- Hot reload with **Cmd+S**

**Xcode (when needed):**
```bash
open ios/Runner.xcworkspace
```
- Use for iOS-specific settings
- Debug C++ code
- Profile performance

## 🛠️ Common iOS Development Tasks

### Run on iPhone Simulator
```bash
# Method 1: Flutter CLI
flutter run -d "iPhone 17 Pro"

# Method 2: Xcode
# Just press Cmd+R in Xcode
```

### Run on Real iPhone
1. **Connect iPhone via USB**
2. **Trust computer on iPhone** (first time only)
3. **In Xcode:**
   - Select your iPhone in device list
   - Update Bundle Identifier if needed
   - Press **Cmd+R**
4. **On iPhone:**
   - Settings → General → VPN & Device Management
   - Trust your developer certificate

### Build Native C++ Inference Layer for iOS
```bash
cd native
./build_ios.sh
```

**When to rebuild:**
- After changing inference code in `native/src/`
- After modifying `.cpp` or `.h` files
- Before running on device (if inference code changed)

**Note:** This builds the inference layer only. ML algorithms are developed in `/ml_algorithms/`

### View iOS Logs
```bash
# Flutter logs
flutter logs

# Xcode logs
# Window → Devices and Simulators → Select device → Open Console
```

## 📱 iOS Simulators Available

You have these simulators ready:
- iPhone 17 Pro ✅ (Recommended)
- iPhone 17 Pro Max
- iPhone Air
- iPhone 17
- iPhone 16e

**Start simulator:**
```bash
# List all
xcrun simctl list devices

# Boot specific simulator
xcrun simctl boot "iPhone 17 Pro"

# Then run app
flutter run -d "iPhone 17 Pro"
```

## 🎨 iOS UI Development

### Use Cupertino Widgets (iOS Style)
```dart
import 'package:flutter/cupertino.dart';

CupertinoApp(
  home: CupertinoPageScaffold(
    navigationBar: CupertinoNavigationBar(
      middle: Text('NeuralList'),
    ),
    child: SafeArea(
      child: YourContent(),
    ),
  ),
)
```

### iOS Design Guidelines
- Use **SF Symbols** for icons
- Follow **Human Interface Guidelines**
- Use **Cupertino widgets** for native iOS feel
- Support **Dark Mode**
- Handle **Safe Area** (notch, home indicator)

### Camera Integration (iOS)
```dart
import 'package:camera/camera.dart';

// Initialize camera
final cameras = await availableCameras();
final camera = cameras.first;

// Use camera
CameraController(
  camera,
  ResolutionPreset.high,
)
```

## 🐛 Debugging

### Debug Flutter (Dart)

**In Xcode:**
1. Run app (Cmd+R)
2. Set breakpoints in Xcode
3. Use Xcode debugger

**In VS Code:**
1. Open project: `code .`
2. Press **F5** to start debugging
3. Set breakpoints in `.dart` files

### Debug C++ (Native)

**Only in Xcode:**
1. Open: `open ios/Runner.xcworkspace`
2. Navigate to C++ files in sidebar
3. Set breakpoints in `.cpp` files
4. Run (Cmd+R)
5. Xcode will break on C++ breakpoints

**Print debugging:**
```cpp
#include <iostream>
std::cout << "Debug: " << value << std::endl;
// See output in Xcode console
```

## 📦 iOS Build Process

### Debug Build (Testing)
```bash
flutter build ios --debug
```

### Release Build (App Store)
```bash
flutter build ios --release
```

### Build in Xcode
1. Open `ios/Runner.xcworkspace`
2. Product → Archive
3. Distribute to App Store or TestFlight

## ⚙️ iOS-Specific Configuration

### Update Bundle Identifier
**File:** `ios/Runner.xcodeproj/project.pbxproj`
Or in Xcode:
1. Select **Runner** project
2. Go to **Signing & Capabilities**
3. Update **Bundle Identifier**: `com.neuralist.app`

### Add iOS Capabilities
In Xcode:
1. Select **Runner** project
2. **Signing & Capabilities** tab
3. Click **+ Capability**
4. Add what you need:
   - Camera ✅ (Already configured)
   - Photo Library ✅ (Already configured)
   - Background Modes (if needed)
   - Push Notifications (if needed)

### Permissions Already Configured ✅
- **Camera Access** - For taking photos
- **Photo Library** - For selecting images
- **Photo Library Add** - For saving images

## 🔍 iOS-Specific Features

### Use iOS Native Features
```dart
import 'dart:io' show Platform;

if (Platform.isIOS) {
  // iOS-specific code
  return CupertinoButton(...);
}
```

### iOS Camera Features
- Portrait mode
- Night mode
- Live Photos
- 4K video
- HDR

### iOS System Integration
- Widgets (Home screen)
- Shortcuts
- Siri integration
- Handoff
- Universal Clipboard

## 🚀 Performance Optimization

### iOS-Specific Optimizations
1. **Use Instruments** (Xcode → Product → Profile)
2. **Enable Metal** (GPU acceleration)
3. **Optimize images** for Retina displays
4. **Use async/await** for C++ calls
5. **Profile on real device** (simulators are faster)

### Instruments Tools (in Xcode)
- **Time Profiler** - CPU usage
- **Allocations** - Memory usage
- **Leaks** - Memory leaks
- **Energy Log** - Battery usage

## 📲 Testing on Real iPhone

### Prerequisites
1. **Apple Developer Account** (free for testing)
2. **iPhone connected via USB**
3. **Xcode** installed

### First Time Setup
1. **Open Xcode:** `open ios/Runner.xcworkspace`
2. **Select iPhone** in device list
3. **Xcode → Preferences → Accounts**
   - Add Apple ID
4. **Project Settings:**
   - Select **Runner** project
   - **Signing & Capabilities**
   - Team: Select your Apple ID
   - Bundle Identifier: `com.yourname.neuralist`
5. **Press Cmd+R**
6. **On iPhone:**
   - Settings → General → VPN & Device Management
   - Trust developer certificate

### Wireless Debugging (iOS 17+)
1. Connect iPhone via USB (first time)
2. Xcode → Window → Devices and Simulators
3. Select iPhone → Check "Connect via network"
4. Disconnect USB - still debugs wirelessly!

## 🎯 iOS Development Shortcuts

### Xcode Keyboard Shortcuts
- **Cmd+R** - Run
- **Cmd+.** - Stop
- **Cmd+B** - Build
- **Cmd+Shift+K** - Clean Build Folder
- **Cmd+/** - Comment/Uncomment
- **Cmd+Control+↑** - Switch between .h/.m/.swift files
- **Cmd+0** - Show/Hide Navigator
- **Cmd+Shift+Y** - Show/Hide Console

### Flutter Commands (Terminal)
```bash
# Run on iPhone
flutter run

# Hot reload
# Just save file or press 'r' in terminal

# Hot restart
# Press 'R' in terminal

# Clear cache
flutter clean

# Update dependencies
flutter pub get

# Check for issues
flutter doctor -v
```

## 📋 Daily iOS Development Routine

### Morning Setup:
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app

# Open in Xcode
open ios/Runner.xcworkspace
```

### During Development:

**UI Work (Dart):**
1. Edit `lib/` files in Xcode or VS Code
2. Save (Cmd+S)
3. Hot reload automatically (or press 'r')

**Inference Code Work (C++):**
1. Edit `native/src/inference/` files (model loading/running only)
2. Run: `cd native && ./build_ios.sh`
3. Restart app (Cmd+R in Xcode)

**ML Algorithm Development:**
1. Work in `/ml_algorithms/` folder
2. Train models there
3. Export to `.tflite`
4. Copy to `assets/models/`

### Testing:
1. Test on simulator first
2. Test on real iPhone before publishing
3. Test camera features on real device (required)

## 🆘 Common iOS Issues

### "Code signing required"
**Fix:**
1. Open `ios/Runner.xcworkspace` in Xcode
2. Select **Runner** project
3. **Signing & Capabilities**
4. Select **Team** (your Apple ID)

### "Library not found"
**Fix:**
```bash
cd native
./build_ios.sh
```

### Camera not working
**Fix:**
- Camera only works on **real iPhone**, not simulator
- Check Info.plist has camera permission ✅

### Build errors after Flutter update
**Fix:**
```bash
flutter clean
cd ios
pod install
cd ..
flutter pub get
```

### "Unable to boot simulator"
**Fix:**
```bash
# Quit Xcode
killall Simulator
xcrun simctl shutdown all
xcrun simctl erase all
# Reopen Xcode
```

## 📚 iOS Resources

### Apple Documentation
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [iOS Developer Documentation](https://developer.apple.com/documentation/)
- [SF Symbols](https://developer.apple.com/sf-symbols/)

### Flutter iOS
- [Flutter iOS Setup](https://docs.flutter.dev/get-started/install/macos#ios-setup)
- [Platform-Specific Code](https://docs.flutter.dev/platform-integration/platform-channels)
- [iOS Deployment](https://docs.flutter.dev/deployment/ios)

## 🎯 Recommended Development Setup

**For best iOS development experience:**

1. **Primary Tool:** Xcode
   - Open: `open ios/Runner.xcworkspace`
   - Use for everything iOS-related

2. **Secondary Tool:** VS Code (optional)
   - For quick Dart edits
   - Better code completion for Flutter

3. **Terminal Window:**
   - Keep one terminal open for `flutter run`
   - Quick commands and logs

4. **Real iPhone:**
   - Essential for camera testing
   - Better performance evaluation
   - Actual user experience

## 🏁 Next Steps

1. **Run the app:**
   ```bash
   open ios/Runner.xcworkspace
   # Press Cmd+R in Xcode
   ```

2. **Test camera permissions** (on real iPhone)

3. **Start building UI** in `lib/main.dart`

4. **Add product database** from scraper

5. **Implement camera screen**

6. **Integrate C++ algorithms**

---

**You're all set for iOS development! 🍎**

Start with Xcode: `open ios/Runner.xcworkspace`
