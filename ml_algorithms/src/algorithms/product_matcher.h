#ifndef NEURALIST_PRODUCT_MATCHER_H
#define NEURALIST_PRODUCT_MATCHER_H

#include <vector>

namespace neuralist {
namespace algorithms {

/**
 * Calculate cosine similarity between two feature vectors
 * @param features1 First feature vector
 * @param features2 Second feature vector
 * @param size Length of feature vectors (must be same for both)
 * @return Cosine similarity score between -1 and 1 (higher is more similar)
 */
double calculate_similarity(
    const double* features1,
    const double* features2,
    int size
);

/**
 * Find best matching product from a database of features
 * @param query_features Features extracted from query image
 * @param query_size Size of query feature vector
 * @param database_features Array of feature vectors from product database
 * @param num_products Number of products in database
 * @param feature_size Size of each feature vector
 * @return Index of best matching product (-1 if none found)
 */
int find_best_match(
    const double* query_features,
    int query_size,
    const double** database_features,
    int num_products,
    int feature_size
);

/**
 * Find top-K matching products
 * @param query_features Features extracted from query image
 * @param query_size Size of query feature vector
 * @param database_features Array of feature vectors from product database
 * @param num_products Number of products in database
 * @param feature_size Size of each feature vector
 * @param k Number of top matches to return
 * @param scores Output array for similarity scores (must have space for k elements)
 * @return Vector of product indices (top-k matches)
 */
std::vector<int> find_top_k_matches(
    const double* query_features,
    int query_size,
    const double** database_features,
    int num_products,
    int feature_size,
    int k,
    double* scores
);

}  // namespace algorithms
}  // namespace neuralist

#endif  // NEURALIST_PRODUCT_MATCHER_H
