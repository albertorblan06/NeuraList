import 'dart:ffi' as ffi;
import 'dart:io';
import 'package:ffi/ffi.dart';

/// FFI bindings for NeuralList native C/C++ library
class NeuralistBindings {
  late final ffi.DynamicLibrary _dylib;

  NeuralistBindings() {
    _dylib = _loadLibrary();
  }

  /// Load the native library based on platform
  ffi.DynamicLibrary _loadLibrary() {
    if (Platform.isAndroid) {
      return ffi.DynamicLibrary.open('libneuralist_native.so');
    } else if (Platform.isIOS || Platform.isMacOS) {
      return ffi.DynamicLibrary.open('libneuralist_native.dylib');
    } else if (Platform.isWindows) {
      return ffi.DynamicLibrary.open('neuralist_native.dll');
    } else if (Platform.isLinux) {
      return ffi.DynamicLibrary.open('libneuralist_native.so');
    } else {
      throw UnsupportedError('Platform not supported');
    }
  }

  // ==================== Version ====================

  /// Get native library version
  String getVersion() {
    final getVersionFunc = _dylib.lookupFunction<
        ffi.Pointer<Utf8> Function(),
        ffi.Pointer<Utf8> Function()>('get_version');
    return getVersionFunc().toDartString();
  }

  // ==================== Image Processing ====================

  /// Process image data
  int processImage(
    ffi.Pointer<ffi.Uint8> imageData,
    int width,
    int height,
    int channels,
  ) {
    final processImageFunc = _dylib.lookupFunction<
        ffi.Int32 Function(ffi.Pointer<ffi.Uint8>, ffi.Int32, ffi.Int32, ffi.Int32),
        int Function(ffi.Pointer<ffi.Uint8>, int, int, int)>('process_image');
    return processImageFunc(imageData, width, height, channels);
  }

  /// Extract features from image
  ffi.Pointer<ffi.Double> extractFeatures(
    ffi.Pointer<ffi.Uint8> imageData,
    int width,
    int height,
    ffi.Pointer<ffi.Int32> featureCount,
  ) {
    final extractFeaturesFunc = _dylib.lookupFunction<
        ffi.Pointer<ffi.Double> Function(
            ffi.Pointer<ffi.Uint8>, ffi.Int32, ffi.Int32, ffi.Pointer<ffi.Int32>),
        ffi.Pointer<ffi.Double> Function(
            ffi.Pointer<ffi.Uint8>, int, int, ffi.Pointer<ffi.Int32>)>(
        'extract_features');
    return extractFeaturesFunc(imageData, width, height, featureCount);
  }

  /// Free features memory
  void freeFeatures(ffi.Pointer<ffi.Double> features) {
    final freeFeaturesFunc = _dylib.lookupFunction<
        ffi.Void Function(ffi.Pointer<ffi.Double>),
        void Function(ffi.Pointer<ffi.Double>)>('free_features');
    freeFeaturesFunc(features);
  }

  // ==================== Product Matching ====================

  /// Calculate similarity between two feature vectors
  double calculateSimilarity(
    ffi.Pointer<ffi.Double> features1,
    ffi.Pointer<ffi.Double> features2,
    int size,
  ) {
    final calculateSimilarityFunc = _dylib.lookupFunction<
        ffi.Double Function(ffi.Pointer<ffi.Double>, ffi.Pointer<ffi.Double>, ffi.Int32),
        double Function(ffi.Pointer<ffi.Double>, ffi.Pointer<ffi.Double>, int)>(
        'calculate_similarity');
    return calculateSimilarityFunc(features1, features2, size);
  }

  /// Find best matching product
  int findBestMatch(
    ffi.Pointer<ffi.Double> queryFeatures,
    int querySize,
    ffi.Pointer<ffi.Pointer<ffi.Double>> productFeatures,
    ffi.Pointer<ffi.Int32> productSizes,
    int numProducts,
  ) {
    final findBestMatchFunc = _dylib.lookupFunction<
        ffi.Int32 Function(
            ffi.Pointer<ffi.Double>,
            ffi.Int32,
            ffi.Pointer<ffi.Pointer<ffi.Double>>,
            ffi.Pointer<ffi.Int32>,
            ffi.Int32),
        int Function(
            ffi.Pointer<ffi.Double>,
            int,
            ffi.Pointer<ffi.Pointer<ffi.Double>>,
            ffi.Pointer<ffi.Int32>,
            int)>('find_best_match');
    return findBestMatchFunc(
        queryFeatures, querySize, productFeatures, productSizes, numProducts);
  }

  // ==================== ML Model ====================

  /// Initialize ML model
  ffi.Pointer<ffi.Void> initModel(String modelPath) {
    final modelPathPtr = modelPath.toNativeUtf8();
    final initModelFunc = _dylib.lookupFunction<
        ffi.Pointer<ffi.Void> Function(ffi.Pointer<Utf8>),
        ffi.Pointer<ffi.Void> Function(ffi.Pointer<Utf8>)>('init_model');
    final result = initModelFunc(modelPathPtr);
    malloc.free(modelPathPtr);
    return result;
  }

  /// Run inference on ML model
  int runInference(
    ffi.Pointer<ffi.Void> model,
    ffi.Pointer<ffi.Double> input,
    int inputSize,
    ffi.Pointer<ffi.Double> output,
    int outputSize,
  ) {
    final runInferenceFunc = _dylib.lookupFunction<
        ffi.Int32 Function(ffi.Pointer<ffi.Void>, ffi.Pointer<ffi.Double>,
            ffi.Int32, ffi.Pointer<ffi.Double>, ffi.Int32),
        int Function(ffi.Pointer<ffi.Void>, ffi.Pointer<ffi.Double>, int,
            ffi.Pointer<ffi.Double>, int)>('run_inference');
    return runInferenceFunc(model, input, inputSize, output, outputSize);
  }

  /// Free ML model
  void freeModel(ffi.Pointer<ffi.Void> model) {
    final freeModelFunc = _dylib.lookupFunction<
        ffi.Void Function(ffi.Pointer<ffi.Void>),
        void Function(ffi.Pointer<ffi.Void>)>('free_model');
    freeModelFunc(model);
  }
}
