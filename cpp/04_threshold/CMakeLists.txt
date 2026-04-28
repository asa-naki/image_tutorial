cmake_minimum_required(VERSION 3.16)
project(04_threshold LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(04_threshold main.cpp)
target_include_directories(04_threshold PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(04_threshold PRIVATE ${OpenCV_LIBS})
