cmake_minimum_required(VERSION 3.10)
project(neuralist_native)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set C standard
set(CMAKE_C_STANDARD 11)

# Platform-specific configurations
if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15" CACHE STRING "Minimum OS X deployment version")
endif()

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Source files
set(SOURCES
    src/algorithms/image_processing.cpp
    src/algorithms/product_matcher.cpp
    src/neuralist_native.cpp
)

# Create shared library
add_library(neuralist_native SHARED ${SOURCES})

# Platform-specific library output
if(APPLE)
    set_target_properties(neuralist_native PROPERTIES
        FRAMEWORK FALSE
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../macos/Frameworks"
    )
elseif(ANDROID)
    set_target_properties(neuralist_native PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../android/app/src/main/jniLibs/${ANDROID_ABI}"
    )
elseif(IOS)
    set_target_properties(neuralist_native PROPERTIES
        FRAMEWORK FALSE
        LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../ios/Frameworks"
    )
endif()

# Installation rules
install(TARGETS neuralist_native
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
)
