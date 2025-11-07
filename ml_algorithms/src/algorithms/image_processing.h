#ifndef NEURALIST_IMAGE_PROCESSING_H
#define NEURALIST_IMAGE_PROCESSING_H

#include <vector>

namespace neuralist {
namespace algorithms {

/**
 * Extract color histogram features from an image
 * @param image_data Raw image data (RGB format)
 * @param width Image width in pixels
 * @param height Image height in pixels
 * @param channels Number of color channels (3 for RGB)
 * @return Feature vector containing color histogram (768 dimensions: 256 per channel)
 */
std::vector<double> extract_color_histogram(
    const unsigned char* image_data,
    int width,
    int height,
    int channels
);

/**
 * Extract features from image data
 * This is the main entry point for feature extraction
 * @param image_data Raw image data
 * @param width Image width
 * @param height Image height
 * @param feature_count Output parameter for number of features
 * @return Pointer to feature array (caller must free)
 */
double* extract_features(
    const unsigned char* image_data,
    int width,
    int height,
    int* feature_count
);

/**
 * Process image for inference
 * Performs preprocessing like resizing, normalization
 * @param image_data Raw image data
 * @param width Image width
 * @param height Image height
 * @param channels Number of channels
 * @return 0 on success, error code otherwise
 */
int process_image(
    const unsigned char* image_data,
    int width,
    int height,
    int channels
);

}  // namespace algorithms
}  // namespace neuralist

#endif  // NEURALIST_IMAGE_PROCESSING_H
