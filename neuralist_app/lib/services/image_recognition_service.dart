import 'dart:ffi' as ffi;
import 'dart:typed_data';
import '../native/neuralist_bindings.dart';
import 'package:ffi/ffi.dart';

/// High-level service for image recognition and product matching
/// This wraps the native C/C++ FFI bindings for easier use in Flutter
class ImageRecognitionService {
  final NeuralistBindings _bindings = NeuralistBindings();

  /// Get the native library version
  String getVersion() {
    return _bindings.getVersion();
  }

  /// Process an image and extract features for product recognition
  Future<List<double>> extractImageFeatures(Uint8List imageData, int width, int height) async {
    // Allocate native memory for image data
    final imagePtr = malloc.allocate<ffi.Uint8>(imageData.length);
    final asBytes = imagePtr.asTypedList(imageData.length);
    asBytes.setAll(0, imageData);

    // Allocate memory for feature count
    final featureCountPtr = malloc.allocate<ffi.Int32>(ffi.sizeOf<ffi.Int32>());

    try {
      // Extract features from native code
      final featuresPtr = _bindings.extractFeatures(
        imagePtr,
        width,
        height,
        featureCountPtr,
      );

      final featureCount = featureCountPtr.value;

      if (featuresPtr == ffi.nullptr || featureCount <= 0) {
        return [];
      }

      // Convert native features to Dart list
      final features = featuresPtr.asTypedList(featureCount);
      final result = List<double>.from(features);

      // Free native memory
      _bindings.freeFeatures(featuresPtr);

      return result;
    } finally {
      malloc.free(imagePtr);
      malloc.free(featureCountPtr);
    }
  }

  /// Calculate similarity between two feature vectors
  double calculateSimilarity(List<double> features1, List<double> features2) {
    if (features1.length != features2.length) {
      throw ArgumentError('Feature vectors must have the same length');
    }

    // Allocate native memory for features
    final features1Ptr = malloc.allocate<ffi.Double>(features1.length * ffi.sizeOf<ffi.Double>());
    final features2Ptr = malloc.allocate<ffi.Double>(features2.length * ffi.sizeOf<ffi.Double>());

    try {
      // Copy features to native memory
      final features1List = features1Ptr.asTypedList(features1.length);
      final features2List = features2Ptr.asTypedList(features2.length);
      features1List.setAll(0, features1);
      features2List.setAll(0, features2);

      // Calculate similarity
      return _bindings.calculateSimilarity(features1Ptr, features2Ptr, features1.length);
    } finally {
      malloc.free(features1Ptr);
      malloc.free(features2Ptr);
    }
  }

  /// Find the best matching product from a database
  /// Returns the index of the best match, or -1 if no match found
  Future<int> findBestMatch(
    List<double> queryFeatures,
    List<List<double>> productFeatures,
  ) async {
    if (productFeatures.isEmpty) {
      return -1;
    }

    // Allocate memory for query features
    final queryPtr = malloc.allocate<ffi.Double>(queryFeatures.length * ffi.sizeOf<ffi.Double>());
    final queryList = queryPtr.asTypedList(queryFeatures.length);
    queryList.setAll(0, queryFeatures);

    // Allocate memory for product features array
    final numProducts = productFeatures.length;
    final productPtrsPtr = malloc.allocate<ffi.Pointer<ffi.Double>>(
      numProducts * ffi.sizeOf<ffi.Pointer<ffi.Double>>(),
    );
    final productSizesPtr = malloc.allocate<ffi.Int32>(numProducts * ffi.sizeOf<ffi.Int32>());

    try {
      // Set up product features
      final productPtrsList = productPtrsPtr.asTypedList(numProducts);
      final productSizesList = productSizesPtr.asTypedList(numProducts);

      for (int i = 0; i < numProducts; i++) {
        final features = productFeatures[i];
        final featurePtr = malloc.allocate<ffi.Double>(features.length * ffi.sizeOf<ffi.Double>());
        final featureList = featurePtr.asTypedList(features.length);
        featureList.setAll(0, features);

        productPtrsList[i] = featurePtr.address;
        productSizesList[i] = features.length;
      }

      // Find best match
      final result = _bindings.findBestMatch(
        queryPtr,
        queryFeatures.length,
        productPtrsPtr,
        productSizesPtr,
        numProducts,
      );

      // Free product feature memory
      for (int i = 0; i < numProducts; i++) {
        malloc.free(ffi.Pointer<ffi.Double>.fromAddress(productPtrsList[i]));
      }

      return result;
    } finally {
      malloc.free(queryPtr);
      malloc.free(productPtrsPtr);
      malloc.free(productSizesPtr);
    }
  }
}
