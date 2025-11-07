#ifndef NEURALIST_NATIVE_H
#define NEURALIST_NATIVE_H

#ifdef __cplusplus
extern "C" {
#endif

// Export macro for cross-platform compatibility
#if defined(_WIN32) || defined(_WIN64)
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

// Version information
EXPORT const char* get_version();

// Image Processing functions
EXPORT int process_image(const unsigned char* image_data, int width, int height, int channels);
EXPORT void* extract_features(const unsigned char* image_data, int width, int height, int* feature_count);
EXPORT void free_features(void* features);

// Product Matching functions
EXPORT double calculate_similarity(const double* features1, const double* features2, int size);
EXPORT int find_best_match(const double* query_features, int query_size,
                           const double** product_features, int* product_sizes,
                           int num_products);

// Shopping List Intelligence
EXPORT void* generate_shopping_suggestions(const char* inventory_json, int* suggestion_count);
EXPORT void free_suggestions(void* suggestions);

// Neural Network / ML functions (placeholder for future implementation)
EXPORT void* init_model(const char* model_path);
EXPORT int run_inference(void* model, const double* input, int input_size,
                        double* output, int output_size);
EXPORT void free_model(void* model);

#ifdef __cplusplus
}
#endif

#endif // NEURALIST_NATIVE_H
