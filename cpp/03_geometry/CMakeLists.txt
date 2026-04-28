cmake_minimum_required(VERSION 3.16)
project(03_geometry LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()
find_package(Eigen3 REQUIRED)

add_executable(03_geometry main.cpp)
target_include_directories(03_geometry PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(03_geometry PRIVATE ${OpenCV_LIBS} Eigen3::Eigen)
