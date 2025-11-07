#!/bin/bash
# Build script for iOS native library

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Building NeuralList native library for iOS...${NC}"

# Create build directory for iOS
mkdir -p build_ios
cd build_ios

# Configure for iOS (arm64 for device, x86_64 for simulator)
echo -e "${YELLOW}Configuring for iOS...${NC}"
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_SYSTEM_NAME=iOS \
    -DCMAKE_OSX_DEPLOYMENT_TARGET=14.0 \
    -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" \
    -DCMAKE_XCODE_ATTRIBUTE_ONLY_ACTIVE_ARCH=NO

# Build
echo -e "${YELLOW}Building...${NC}"
cmake --build . --config Release

# Copy to iOS Frameworks
echo -e "${YELLOW}Installing to iOS Frameworks...${NC}"
mkdir -p ../../ios/Frameworks
cp libneuralist_native.dylib ../../ios/Frameworks/

echo -e "${GREEN}✅ iOS build complete!${NC}"
echo -e "${GREEN}Library: ios/Frameworks/libneuralist_native.dylib${NC}"
