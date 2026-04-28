cmake_minimum_required(VERSION 3.16)
project(13_calibration LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()
find_package(Eigen3 REQUIRED)

add_executable(13_calibration main.cpp)
target_include_directories(13_calibration PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(13_calibration PRIVATE ${OpenCV_LIBS} Eigen3::Eigen)
