# Native iOS Inference Layer

**⚡ This is for MODEL INFERENCE only - NOT for ML development**

## Purpose

This folder contains C++ code that RUNS in the iOS app to:
- ✅ Load pre-trained models
- ✅ Run inference on images
- ✅ Process camera frames
- ✅ Call TensorFlow Lite

**NOT for:**
- ❌ Training models (go to `/ml_algorithms`)
- ❌ Developing algorithms (go to `/ml_algorithms`)
- ❌ Experimenting (go to `/ml_algorithms`)

## Structure

```
native/
│
├── build_ios.sh                # Build for iOS
├── CMakeLists.txt              # Build config
│
├── include/                    # C++ headers
│   └── neuralist_inference.h  # Inference API
│
└── src/                        # C++ implementation
    ├── inference/              # TFLite inference
    │   ├── model_loader.cpp
    │   ├── image_preprocessor.cpp
    │   └── tflite_runner.cpp
    │
    └── utils/                  # Utilities
        └── image_utils.cpp
```

## What Goes Here

### ✅ Inference Code
```cpp
// Load pre-trained model
TFLiteModel* load_model(const char* model_path);

// Run inference
float* run_inference(TFLiteModel* model, const uint8_t* image);

// Preprocess image for model
void preprocess_image(const uint8_t* input, float* output);
```

### ✅ Image Processing for Inference
```cpp
// Resize image to model input size
void resize_for_model(const uint8_t* image, int width, int height,
                     uint8_t* output, int target_width, int target_height);

// Normalize pixel values
void normalize_pixels(const uint8_t* image, float* output, int size);
```

### ❌ What DOESN'T Go Here

- Training code (→ `/ml_algorithms/training/`)
- Algorithm development (→ `/ml_algorithms/src/`)
- Model export (→ `/ml_algorithms/export/`)
- Research code (→ `/ml_algorithms/`)

## Workflow

### 1. Get Model from ML Team
```bash
# Models are developed in /ml_algorithms
# Copy trained model to app
cp ../../ml_algorithms/models/product_detector.tflite \
   ../assets/models/
```

### 2. Write Inference Code
```cpp
// native/src/inference/model_loader.cpp
#include "tensorflow/lite/c/c_api.h"

TfLiteModel* load_model(const char* path) {
    return TfLiteModelCreateFromFile(path);
}
```

### 3. Build for iOS
```bash
./build_ios.sh
```

### 4. Use from Dart
```dart
// lib/services/inference_service.dart
final result = inferenceService.runModel(imageBytes);
```

## Building

### Build for iOS
```bash
cd native
./build_ios.sh
```

This creates: `../ios/Frameworks/libneuralist_native.dylib`

### Build Requirements
- Xcode 15+
- CMake 4.1+
- TensorFlow Lite iOS framework

## Integration with TensorFlow Lite

### Add TFLite to iOS
```ruby
# ios/Podfile
pod 'TensorFlowLiteSwift'
pod 'TensorFlowLiteC'
```

### Use in C++
```cpp
#include "tensorflow/lite/c/c_api.h"

TfLiteModel* model = TfLiteModelCreateFromFile(model_path);
TfLiteInterpreter* interpreter = TfLiteInterpreterCreate(model, options);
TfLiteInterpreterAllocateTensors(interpreter);

// Set input
TfLiteTensor* input = TfLiteInterpreterGetInputTensor(interpreter, 0);
TfLiteTensorCopyFromBuffer(input, image_data, image_size);

// Run inference
TfLiteInterpreterInvoke(interpreter);

// Get output
const TfLiteTensor* output = TfLiteInterpreterGetOutputTensor(interpreter, 0);
```

## API Design

### Simple Inference API
```cpp
// include/neuralist_inference.h
#ifdef __cplusplus
extern "C" {
#endif

// Initialize model
void* init_model(const char* model_path);

// Run inference on image
float* run_inference(void* model, const uint8_t* image,
                    int width, int height, int* output_size);

// Cleanup
void free_model(void* model);
void free_output(float* output);

#ifdef __cplusplus
}
#endif
```

## Performance Considerations

### iOS Optimization
- Use Metal GPU delegate for TFLite
- Quantize models to int8
- Batch process when possible
- Cache models in memory

### Example: GPU Acceleration
```cpp
#include "tensorflow/lite/delegates/gpu/metal_delegate.h"

TfLiteDelegate* delegate = TFLGpuDelegateCreate(nullptr);
TfLiteInterpreterModifyGraph(interpreter, delegate);
```

## File Organization

```
src/
├── inference/              # Model inference
│   ├── model_loader.cpp   # Load .tflite models
│   ├── preprocessor.cpp   # Prepare images
│   └── runner.cpp         # Run inference
│
└── utils/                  # Helpers
    ├── image_utils.cpp    # Image manipulation
    └── memory.cpp         # Memory management
```

## Current Implementation

### ✅ Completed
- [x] Build system (CMake)
- [x] iOS build script
- [x] Basic FFI structure
- [ ] TFLite integration
- [ ] GPU delegate
- [ ] Model loading
- [ ] Inference pipeline

### 🔄 Next Steps
1. Add TensorFlow Lite dependency
2. Implement model loader
3. Create inference runner
4. Add GPU acceleration
5. Optimize for battery life

## Testing

### Test Inference Speed
```cpp
auto start = std::chrono::high_resolution_clock::now();
float* result = run_inference(model, image, width, height, &size);
auto end = std::chrono::high_resolution_clock::now();
auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
std::cout << "Inference time: " << duration.count() << "ms" << std::endl;
```

### Test on Device
- Always test on real iPhone
- Profile with Xcode Instruments
- Check battery usage
- Monitor memory

## Common Issues

### Model Not Found
```
Error: Could not load model from path
Solution: Check model is in assets/models/
```

### Slow Inference
```
Problem: >200ms per frame
Solution: Enable GPU delegate, quantize model
```

### Memory Leak
```
Problem: Memory keeps growing
Solution: Call free_model() and free_output()
```

## Resources

- [TFLite iOS Guide](https://www.tensorflow.org/lite/guide/ios)
- [GPU Delegate](https://www.tensorflow.org/lite/performance/gpu)
- [Metal Framework](https://developer.apple.com/metal/)

## Key Principle

> **This folder loads and runs models.**
> **Models are created in `/ml_algorithms/`.**

---

**⚡ Focus: Fast, efficient inference on iOS**

**For ML development: go to `/ml_algorithms/`**
