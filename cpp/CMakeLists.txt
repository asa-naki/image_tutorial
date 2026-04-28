cmake_minimum_required(VERSION 3.16)
project(image_tutorial_cpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# 共通依存
find_package(OpenCV REQUIRED)
find_package(Eigen3 QUIET)
if(NOT Eigen3_FOUND)
    message(STATUS "Eigen3 not found via find_package; using pkg-config fallback if available")
endif()

# 共通インクルードパス (common/utils.hpp 用)
set(IMAGE_TUTORIAL_COMMON_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# 全セクション
set(ALL_SECTIONS
    01_io
    02_color
    03_geometry
    04_threshold
    05_smoothing
    06_edge
    07_morphology
    08_histogram
    09_contours
    10_template_matching
    11_features
    12_video
    13_calibration
    14_dnn
)

# 部分ビルドオプション (例: -DBUILD_SECTIONS="01_io;05_smoothing")
set(BUILD_SECTIONS "" CACHE STRING "Subset of sections to build (empty = all)")

if(BUILD_SECTIONS STREQUAL "")
    set(SECTIONS_TO_BUILD ${ALL_SECTIONS})
else()
    set(SECTIONS_TO_BUILD ${BUILD_SECTIONS})
endif()

foreach(sec ${SECTIONS_TO_BUILD})
    if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${sec}/CMakeLists.txt")
        message(STATUS "Adding section: ${sec}")
        add_subdirectory(${sec})
    else()
        message(WARNING "Section directory not found: ${sec}")
    endif()
endforeach()
