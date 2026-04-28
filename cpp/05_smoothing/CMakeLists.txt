cmake_minimum_required(VERSION 3.16)
project(05_smoothing LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(05_smoothing main.cpp)
target_include_directories(05_smoothing PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(05_smoothing PRIVATE ${OpenCV_LIBS})
