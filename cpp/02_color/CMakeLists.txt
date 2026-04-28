cmake_minimum_required(VERSION 3.16)
project(02_color LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(02_color main.cpp)
target_include_directories(02_color PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(02_color PRIVATE ${OpenCV_LIBS})
