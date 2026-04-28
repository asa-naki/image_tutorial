cmake_minimum_required(VERSION 3.16)
project(08_histogram LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(08_histogram main.cpp)
target_include_directories(08_histogram PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(08_histogram PRIVATE ${OpenCV_LIBS})
