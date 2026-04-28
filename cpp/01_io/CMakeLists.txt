cmake_minimum_required(VERSION 3.16)
project(01_io LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(01_io main.cpp)
target_include_directories(01_io PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(01_io PRIVATE ${OpenCV_LIBS})
