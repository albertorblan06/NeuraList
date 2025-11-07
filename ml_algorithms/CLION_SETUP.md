# CLion Setup Guide for NeuralList ML Algorithms

## 🚀 Quick Start

### 1. Open Project in CLion

```bash
# Launch CLion
# File → Open...
# Navigate to: ~/Documents/NeuraList/ml_algorithms
# Click "Open"
```

CLion will automatically detect the `CMakeLists.txt` file.

### 2. Configure CMake

CLion should auto-configure, but if needed:

1. **File → Settings** (or **CLion → Preferences** on macOS)
2. **Build, Execution, Deployment → CMake**
3. You should see:
   - **Build type:** Release (or Debug for development)
   - **CMake options:** (leave empty for now)
   - **Build directory:** `cmake-build-release` or `cmake-build-debug`

### 3. Build the Project

**Method A: Menu**
- **Build → Build Project** (or press **Cmd+F9** on macOS)

**Method B: Bottom panel**
- Click **Build** button in bottom panel
- Click **CMake** tab to see build output

### 4. Start Coding!

Navigate to:
- `src/algorithms/image_processing.cpp`
- `src/algorithms/product_matcher.cpp`

Start implementing your algorithms!

---

## 📂 Project Structure

```
ml_algorithms/
├── CMakeLists.txt           ← CMake configuration
├── .clang-format           ← Code formatting rules
├── .gitignore              ← Git ignore rules
│
├── src/                     ← YOUR C++ CODE
│   ├── algorithms/          ← Main algorithms
│   │   ├── image_processing.cpp
│   │   ├── image_processing.h
│   │   ├── product_matcher.cpp
│   │   └── product_matcher.h
│   ├── feature_extraction/  ← Feature extraction
│   ├── product_matching/    ← Advanced matching
│   └── preprocessing/       ← Image preprocessing
│
├── training/                ← Python training scripts
│   ├── train_product_recognition.py
│   ├── datasets/            ← Training data
│   └── notebooks/           ← Jupyter notebooks
│
├── models/                  ← Trained models
│   ├── *.tflite            ← Exported models
│   └── checkpoints/         ← Training checkpoints
│
├── export/                  ← Model export scripts
│   ├── export_to_tflite.py
│   └── optimize_model.py
│
└── docs/                    ← Documentation
    ├── architecture.md
    └── training_guide.md
```

---

## 🔧 CLion Features You'll Use

### 1. **Code Navigation**
- **Cmd+Click** (or **Ctrl+Click**) on function → Go to definition
- **Cmd+B** → Go to declaration
- **Cmd+Alt+B** → Go to implementation
- **Cmd+Shift+F** → Search in project

### 2. **Code Completion**
- Start typing → CLion suggests completions
- **Ctrl+Space** → Force show completions

### 3. **Refactoring**
- **Right-click** → **Refactor** → Rename/Extract/etc.
- **Cmd+Alt+Shift+T** → Refactoring menu

### 4. **Debugging** (Not for this project yet)
- C++ debugging works great
- Set breakpoints (click left of line number)
- Run in debug mode

### 5. **Code Formatting**
- **Cmd+Alt+L** → Format current file (uses .clang-format)
- **Code → Reformat Code**

---

## 🛠️ Common Tasks

### Build Project
```
Menu: Build → Build Project
Shortcut: Cmd+F9
```

### Clean Build
```
Menu: Build → Clean
```

### Rebuild All
```
Menu: Build → Rebuild All
```

### View CMake Output
```
Bottom panel → CMake tab
```

---

## 📝 Adding New C++ Files

### Method 1: Via CLion

1. **Right-click** on `src/algorithms/` (or other folder)
2. **New → C++ Class** (or **C++ Header File** / **C++ Source File**)
3. Enter name: e.g., `edge_detection`
4. CLion creates `.h` and `.cpp` files

### Method 2: Manual

1. Create files manually:
   ```bash
   touch src/feature_extraction/color_histogram.cpp
   touch src/feature_extraction/color_histogram.h
   ```

2. Update `CMakeLists.txt`:
   ```cmake
   set(FEATURE_EXTRACTION_SOURCES
       src/feature_extraction/color_histogram.cpp
   )
   add_library(feature_extraction STATIC ${FEATURE_EXTRACTION_SOURCES})
   ```

3. **Tools → CMake → Reload CMake Project**

---

## 🐍 Python Development (Not in CLion)

For Python training scripts, use:
- **VS Code** (recommended)
- **PyCharm**
- **Jupyter Lab**

CLion can open Python files but isn't ideal for Python development.

---

## ⚙️ Advanced Configuration

### Enable More Warnings

Edit `CMakeLists.txt`:
```cmake
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra -Wpedantic")
```

### Add OpenCV (when needed)

Uncomment in `CMakeLists.txt`:
```cmake
find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
    include_directories(${OpenCV_INCLUDE_DIRS})
    target_link_libraries(neuralist_algorithms ${OpenCV_LIBS})
endif()
```

### Enable C++20

Edit `CMakeLists.txt`:
```cmake
set(CMAKE_CXX_STANDARD 20)
```

---

## 🎯 What to Code Here

### ✅ DO Code Here:
- C++ algorithms (feature extraction, matching, etc.)
- Algorithm research and prototypes
- Image processing functions
- Mathematical computations

### ❌ DON'T Code Here:
- Model training (use Python in `training/`)
- iOS app code (use Xcode for `neuralist_app/`)
- Inference code for app (that's in `neuralist_app/native/`)

---

## 🚨 Important Notes

### This is for Algorithm Development Only

**Purpose:** Develop and test C++ algorithms

**NOT for:**
- Running the iOS app (use Xcode)
- Training models (use Python/PyCharm/VS Code)
- Inference in app (that's in `neuralist_app/`)

### Workflow

```
1. Develop algorithm here (CLion)
   ↓
2. Train model with it (Python)
   ↓
3. Export to TFLite
   ↓
4. Use in app (Xcode)
```

---

## 🔍 Troubleshooting

### CMake Not Found

If CLion says "CMake not found":

```bash
# Install CMake
brew install cmake

# Restart CLion
# File → Settings → Build → CMake
# Set CMake executable to: /opt/homebrew/bin/cmake
```

### Cannot Find Header Files

If CLion shows red underlines for `#include`:

1. **Tools → CMake → Reset Cache and Reload Project**
2. **File → Invalidate Caches / Restart**

### Build Errors

```bash
# Clean build
rm -rf cmake-build-*

# In CLion: Build → Clean
# Then: Build → Rebuild All
```

---

## 📚 Resources

### CLion Documentation
- [CLion Quick Start](https://www.jetbrains.com/help/clion/clion-quick-start-guide.html)
- [CMake in CLion](https://www.jetbrains.com/help/clion/cmake-support.html)

### Project Documentation
- `README.md` - ML development guide
- `/PROJECT_STRUCTURE.md` - Complete project structure
- `/neuralist_app/START_HERE_IOS.md` - iOS app guide

---

## ✅ You're Ready!

1. **Open CLion**
2. **File → Open** → Select `ml_algorithms` folder
3. **Wait for CMake to configure**
4. **Navigate to `src/algorithms/image_processing.cpp`**
5. **Start coding!**

---

**Happy coding! 🚀**
