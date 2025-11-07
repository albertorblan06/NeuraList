# 🍎 Start Here - iOS Development

**📱 This folder is for APP DEVELOPMENT - ML development is in `/ml_algorithms/`**

## Quick Start (2 Commands)

### Option 1: Xcode (Recommended)
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app
open ios/Runner.xcworkspace
```
Then press **Cmd+R** in Xcode to run!

### Option 2: Terminal
```bash
cd /Users/albertorblan/Documents/NeuraList/neuralist_app
flutter run -d "iPhone 17 Pro"
```

## 📂 What to Open

### Primary: Xcode
```bash
open ios/Runner.xcworkspace
```

**Why Xcode?**
- ✅ Best for iOS development
- ✅ Built-in simulator
- ✅ C++ debugging
- ✅ iOS-specific features
- ✅ Performance profiling
- ✅ App Store publishing

### Secondary: VS Code (Optional)
```bash
code .
```

**Use VS Code for:**
- Quick Dart edits
- Better Flutter/Dart autocomplete
- Multi-file editing

## 🎯 Your Main Files

```
Edit These (App Development):
├── lib/main.dart              ← Your app starts here
├── lib/screens/               ← Create screens
├── lib/widgets/               ← Create widgets
└── native/src/inference/      ← C++ inference (load/run models)

For ML Development (algorithms, training):
└── /ml_algorithms/            ← Go here for ML work

Don't Edit:
├── ios/ (except Info.plist)
├── build/
└── .dart_tool/
```

## ⚡ Development Workflow

### 1. Open Xcode
```bash
open ios/Runner.xcworkspace
```

### 2. Select Device
- Top bar: **"iPhone 17 Pro"** (simulator)
- Or plug in your iPhone and select it

### 3. Run
- Press **Cmd+R**
- Or click ▶️ button

### 4. Edit Code
- Edit `lib/main.dart` in Xcode or VS Code
- **Save** → App updates automatically! (Hot Reload)

### 5. Edit C++ Inference Code (when needed)
- Edit `native/src/inference/` files
- Run: `cd native && ./build_ios.sh`
- **Cmd+R** in Xcode to restart app

**Note:** For ML algorithm development, work in `/ml_algorithms/` instead!

## 🔥 Hot Reload Magic

**What is Hot Reload?**
- Edit Dart code
- Press **Cmd+S**
- See changes **instantly** without restarting!

**Works for:**
- ✅ UI changes
- ✅ Adding widgets
- ✅ Text changes
- ✅ Colors, styles

**Doesn't work for:**
- ❌ C++ changes (need rebuild)
- ❌ Adding new files (use Hot Restart)
- ❌ Changing app structure (use Hot Restart)

**Hot Restart:** Press **R** in terminal (rebuilds everything fast)

## 📱 Available Simulators

You have these iPhone simulators:
- iPhone 17 Pro ✅ (Best for testing)
- iPhone 17 Pro Max (Large screen)
- iPhone Air
- iPhone 17
- iPhone 16e

**Start specific simulator:**
```bash
# From Xcode: Product → Destination → Select iPhone
# Or in terminal:
flutter run -d "iPhone 17 Pro"
```

## 🎨 First Thing to Build

### 1. Run the Default App
```bash
open ios/Runner.xcworkspace
# Press Cmd+R
```
You'll see a Flutter demo app!

### 2. Make Your First Change
Open `lib/main.dart` and change:
```dart
title: 'Flutter Demo',
```
to:
```dart
title: 'NeuralList',
```

Press **Cmd+S** → See it update instantly!

### 3. Change the Color
Find:
```dart
colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
```
Change to:
```dart
colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
```

### 4. Add Your Text
Find the `Text('0')` widget and change it to:
```dart
Text(
  '👋 Welcome to NeuralList!',
  style: TextStyle(fontSize: 24),
)
```

## 🏗️ Project Structure

```
neuralist_app/
│
├── lib/                    ← YOUR FLUTTER CODE
│   ├── main.dart          ← START HERE!
│   ├── screens/           ← Full-screen pages
│   ├── widgets/           ← Reusable UI components
│   ├── models/            ← Data structures
│   ├── services/          ← Business logic
│   └── native/            ← FFI bindings (connects to C++)
│
├── native/                 ← YOUR C++ INFERENCE CODE (not training)
│   ├── build_ios.sh       ← Build script
│   ├── include/           ← Inference API headers
│   └── src/
│       ├── inference/     ← Load/run models (NOT training)
│       └── utils/         ← Helper utilities

├── assets/
│   └── models/            ← Pre-trained .tflite models
│                          ← (copied from /ml_algorithms/models/)
│
├── ios/                    ← iOS-SPECIFIC
│   ├── Runner.xcworkspace ← OPEN THIS in Xcode
│   ├── Runner/Info.plist  ← Camera permissions ✅
│   └── Frameworks/        ← Native library ✅
│
├── test/                   ← Tests
└── pubspec.yaml           ← Dependencies
```

## 🛠️ Common Commands

### Run App
```bash
# Xcode: Press Cmd+R
# Or terminal:
flutter run
```

### Hot Reload
```bash
# Press 'r' in terminal
# Or just save file (Cmd+S)
```

### Hot Restart
```bash
# Press 'R' in terminal
```

### Clean Build
```bash
flutter clean
flutter pub get
```

### Build for Testing on iPhone
```bash
flutter build ios --debug
```

### View Logs
```bash
flutter logs
```

## 📸 Camera Feature

**Important:** Camera only works on **real iPhone**, not simulator!

**To test camera:**
1. Connect iPhone via USB
2. In Xcode: Select your iPhone (top bar)
3. Press Cmd+R
4. On iPhone: Trust computer
5. App launches on your iPhone!

Camera permissions are already configured ✅

## 🐛 Debugging

### Print Debugging (Easiest)
```dart
print('Debug: $myVariable');
debugPrint('This is a debug message');
```

See output in Xcode console or terminal.

### Breakpoint Debugging
1. Click left of line number to add breakpoint (red dot)
2. Run in debug mode
3. App pauses at breakpoint
4. Inspect variables

### C++ Debugging (Xcode Only)
1. Open: `open ios/Runner.xcworkspace`
2. Open C++ file in Xcode sidebar
3. Set breakpoint in C++ code
4. Run (Cmd+R)
5. Debugger breaks on C++ breakpoints

## 🚀 Next Steps

### Step 1: Run the App (Now!)
```bash
open ios/Runner.xcworkspace
# Press Cmd+R
```

### Step 2: Make Changes
- Edit `lib/main.dart`
- Change some text
- Save and see it update!

### Step 3: Create Your First Screen
Create `lib/screens/home_screen.dart`:
```dart
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('NeuralList')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.camera_alt, size: 100, color: Colors.blue),
            SizedBox(height: 20),
            Text('Take a photo of your fridge!',
                style: TextStyle(fontSize: 24)),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Camera action here
              },
              child: Text('Open Camera'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Step 4: Use Your Screen
In `lib/main.dart`, change:
```dart
home: MyHomePage(title: 'Flutter Demo Home Page'),
```
to:
```dart
home: HomeScreen(),
```

## 💡 Tips for iOS Development

1. **Always use Xcode** for iOS development
2. **Test on real iPhone** for camera features
3. **Save often** - Hot Reload is magic!
4. **Check Xcode console** for errors
5. **Use Cupertino widgets** for iOS look
6. **Read errors carefully** - they're helpful!

## 📚 Documentation

- **iOS Guide:** `IOS_DEVELOPMENT.md`
- **Full Dev Guide:** `DEVELOPMENT.md`
- **Architecture:** `README.md`

## 🆘 Problems?

### App won't build?
```bash
flutter clean
flutter pub get
cd ios
pod install
cd ..
flutter run
```

### Native library error?
```bash
cd native
./build_ios.sh
cd ..
```

### Xcode issues?
```bash
# Clean Xcode
# Xcode → Product → Clean Build Folder
# Or: Cmd+Shift+K
```

## ✅ You're Ready!

Everything is set up for iOS development:
- ✅ Flutter project created
- ✅ C++ algorithms ready
- ✅ iOS permissions configured
- ✅ Native library built
- ✅ Xcode workspace ready

**Now run this:**
```bash
open ios/Runner.xcworkspace
```

**Then press Cmd+R and start coding!** 🚀

---

**Have fun building NeuralList! 🍎📱**
