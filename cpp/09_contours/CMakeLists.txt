cmake_minimum_required(VERSION 3.16)
project(09_contours LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(09_contours main.cpp)
target_include_directories(09_contours PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(09_contours PRIVATE ${OpenCV_LIBS})
