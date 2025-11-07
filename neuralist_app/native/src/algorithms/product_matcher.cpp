#include "neuralist_native.h"
#include <math.h>
#include <float.h>

/**
 * Calculate similarity between two feature vectors
 * Using cosine similarity for now, but can be extended to other metrics
 */
double calculate_similarity(const double* features1, const double* features2, int size) {
    if (!features1 || !features2 || size <= 0) {
        return 0.0;
    }

    // Cosine similarity: dot(A, B) / (||A|| * ||B||)
    double dot_product = 0.0;
    double norm1 = 0.0;
    double norm2 = 0.0;

    for (int i = 0; i < size; i++) {
        dot_product += features1[i] * features2[i];
        norm1 += features1[i] * features1[i];
        norm2 += features2[i] * features2[i];
    }

    norm1 = sqrt(norm1);
    norm2 = sqrt(norm2);

    if (norm1 == 0.0 || norm2 == 0.0) {
        return 0.0;
    }

    return dot_product / (norm1 * norm2);
}

/**
 * Find best matching product from a database of product features
 * Returns the index of the best match
 */
int find_best_match(const double* query_features, int query_size,
                   const double** product_features, int* product_sizes,
                   int num_products) {
    if (!query_features || !product_features || !product_sizes || num_products <= 0) {
        return -1;
    }

    int best_match = -1;
    double best_similarity = -1.0;

    for (int i = 0; i < num_products; i++) {
        if (product_sizes[i] != query_size) {
            continue; // Skip if feature sizes don't match
        }

        double similarity = calculate_similarity(query_features, product_features[i], query_size);

        if (similarity > best_similarity) {
            best_similarity = similarity;
            best_match = i;
        }
    }

    return best_match;
}

/**
 * Advanced product matching with multiple features
 * This can include:
 * - Visual features (color, texture, shape)
 * - Textual features (brand, name, category)
 * - Contextual features (location in fridge, purchase history)
 */
// TODO: Implement multi-modal product matching
