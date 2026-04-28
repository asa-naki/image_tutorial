cmake_minimum_required(VERSION 3.16)
project(11_features LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(11_features main.cpp)
target_include_directories(11_features PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(11_features PRIVATE ${OpenCV_LIBS})
