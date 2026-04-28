cmake_minimum_required(VERSION 3.16)
project(12_video LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(12_video main.cpp)
target_include_directories(12_video PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(12_video PRIVATE ${OpenCV_LIBS})
