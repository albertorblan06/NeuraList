# NeuralList ML Algorithms - CMake Configuration
cmake_minimum_required(VERSION 3.20)
project(neuralist_algorithms VERSION 1.0.0 LANGUAGES CXX)

# C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -Wall -Wextra")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/src)

# Source files for algorithms
set(ALGORITHM_SOURCES
    src/algorithms/image_processing.cpp
    src/algorithms/product_matcher.cpp
)

# Create algorithms library
add_library(neuralist_algorithms STATIC ${ALGORITHM_SOURCES})

# Optional: Find OpenCV (uncomment when needed)
# find_package(OpenCV REQUIRED)
# if(OpenCV_FOUND)
#     include_directories(${OpenCV_INCLUDE_DIRS})
#     target_link_libraries(neuralist_algorithms ${OpenCV_LIBS})
# endif()

# Optional: Add feature extraction sources when created
# set(FEATURE_EXTRACTION_SOURCES
#     src/feature_extraction/color_histogram.cpp
#     src/feature_extraction/edge_detection.cpp
# )
# add_library(feature_extraction STATIC ${FEATURE_EXTRACTION_SOURCES})

# Optional: Add preprocessing sources when created
# set(PREPROCESSING_SOURCES
#     src/preprocessing/image_resize.cpp
#     src/preprocessing/normalization.cpp
# )
# add_library(preprocessing STATIC ${PREPROCESSING_SOURCES})

# Install targets
install(TARGETS neuralist_algorithms
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)

# Install headers
install(DIRECTORY src/
    DESTINATION include/neuralist
    FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

# Testing (optional - uncomment when you add tests)
# enable_testing()
# add_subdirectory(tests)

# Print configuration
message(STATUS "")
message(STATUS "NeuralList ML Algorithms Configuration:")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ Standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "")
