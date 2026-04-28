cmake_minimum_required(VERSION 3.16)
project(07_morphology LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(07_morphology main.cpp)
target_include_directories(07_morphology PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(07_morphology PRIVATE ${OpenCV_LIBS})
