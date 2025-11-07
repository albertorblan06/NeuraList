#include "product_matcher.h"
#include <cmath>
#include <cfloat>
#include <vector>
#include <algorithm>

namespace neuralist {
namespace algorithms {

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
int find_best_match(
    const double* query_features,
    int query_size,
    const double** database_features,
    int num_products,
    int feature_size
) {
    if (!query_features || !database_features || num_products <= 0) {
        return -1;
    }

    if (query_size != feature_size) {
        return -1;  // Feature size mismatch
    }

    int best_match = -1;
    double best_similarity = -1.0;

    for (int i = 0; i < num_products; i++) {
        double similarity = calculate_similarity(
            query_features,
            database_features[i],
            query_size
        );

        if (similarity > best_similarity) {
            best_similarity = similarity;
            best_match = i;
        }
    }

    return best_match;
}

/**
 * Find top-K matching products
 */
std::vector<int> find_top_k_matches(
    const double* query_features,
    int query_size,
    const double** database_features,
    int num_products,
    int feature_size,
    int k,
    double* scores
) {
    std::vector<int> result;

    if (!query_features || !database_features || num_products <= 0 || k <= 0) {
        return result;
    }

    if (query_size != feature_size) {
        return result;  // Feature size mismatch
    }

    // Calculate all similarities
    std::vector<std::pair<double, int>> similarities;
    similarities.reserve(num_products);

    for (int i = 0; i < num_products; i++) {
        double similarity = calculate_similarity(
            query_features,
            database_features[i],
            query_size
        );
        similarities.push_back({similarity, i});
    }

    // Sort by similarity (descending)
    std::sort(
        similarities.begin(),
        similarities.end(),
        [](const std::pair<double, int>& a, const std::pair<double, int>& b) {
            return a.first > b.first;
        }
    );

    // Get top-k
    int count = std::min(k, static_cast<int>(similarities.size()));
    for (int i = 0; i < count; i++) {
        result.push_back(similarities[i].second);
        if (scores) {
            scores[i] = similarities[i].first;
        }
    }

    return result;
}

}  // namespace algorithms
}  // namespace neuralist
