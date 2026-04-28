cmake_minimum_required(VERSION 3.16)
project(10_template_matching LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(10_template_matching main.cpp)
target_include_directories(10_template_matching PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(10_template_matching PRIVATE ${OpenCV_LIBS})
