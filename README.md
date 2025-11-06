# NeuralList: AI-Powered Visual Shopping Assistant

## 1. The Problem

Standard shopping list applications act merely as "digital paper." They rely on generic text input (e.g., "milk," "tomato sauce") that lacks context, leading to friction during the actual shopping process. They don't know what the product looks like, where it is located, or exactly which specific SKU the user intends to buy among dozens of similar options.

The cognitive load of finding products in a massive, visually noisy supermarket environment remains entirely on the user.

## 2. The Solution (Project Vision)

NeuralList aims to bridge the gap between standard list management and real-world execution by applying Computer Vision (CV) and Natural Language Processing (NLP) to the shopping experience.

Instead of just sorting items alphabetically or by rough categories, the application aims to be "spatial-aware" and "visually intelligent." The ultimate goal is an assistant that can "see" the supermarket shelves through the camera feed and actively highlight the products currently on your list, effectively bringing Edge AI to a mundane daily task.

## 3. Core Pillars & Technical Expectations

### 3.1. Intelligent Intent Translation (NLP & Search)

Users rarely type full product names. The system must translate vague intent into concrete data.

- **Functionality**: When a user types "semi milk", the system won't just save that string. It will query a structured dataset (e.g., scraped from major retailers like Mercadona) using fuzzy search or vector embeddings to suggest the actual target SKU: "Hacendado Semi-Skimmed Milk, 1L Brick".

- **Value**: This ensures every item on the list is tied to a real image, price, and EAN code, essential for the subsequent visual recognition steps.

### 3.2. Real-Time Visual Recognition (Computer Vision)

Moving beyond simple barcode scanning, this module is the core R&D challenge of the project.

- **Phase 1 (Deterministic)**: High-performance native barcode scanning for quick ground-truth verification.

- **Phase 2 (Probabilistic - Edge AI)**: Implementation of lightweight Object Detection models (e.g., YOLOv8 Nano, MobileNet SSD) running on-device via TensorFlow Lite. The goal is to recognize specific product packaging in the live camera feed as the user walks down the aisle.

- **Performance Note**: To achieve real-time frame rates without destroying battery life, critical pre-processing steps may be offloaded to native C++ layers accessed via Dart FFI.

### 3.3. Indoor Localization & Mapping (Visual SLAM)

A long-term research goal is to remove the need for manual aisle sorting.

- **Concept**: By leveraging smartphone visual sensors (camera + IMU), the app could potentially perform basic Visual SLAM (Simultaneous Localization and Mapping) to recognize distinct supermarket zones (e.g., "Dairy Section", "Bakery") based on visual features, automatically ordering the list based on the user's real-time path through the store.

## 4. Proposed Tech Stack

This project chooses a hybrid approach to balance UI development speed with raw performance for native tasks.

- **Mobile Framework**: Flutter (Dart). Chosen for its rapid UI capabilities and mature ecosystem for managing varied state (shopping lists vs. camera streams).

- **Native Performance Layer**: C++ accessed via Dart FFI. Reserved for computationally intensive image processing tasks that exceed Dart's capabilities in real-time scenarios.

- **AI/ML Engine**: TensorFlow Lite for on-device inference, ensuring the app works even with poor supermarket connectivity.

- **Backend & Data**: Firebase/Supabase for real-time list synchronization between household members and hosting the product master catalog.
