cmake_minimum_required(VERSION 3.16)
project(06_edge LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(06_edge main.cpp)
target_include_directories(06_edge PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(06_edge PRIVATE ${OpenCV_LIBS})
