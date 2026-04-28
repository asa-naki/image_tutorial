cmake_minimum_required(VERSION 3.16)
project(14_dnn LANGUAGES CXX)

if(NOT TARGET opencv_core)
    find_package(OpenCV REQUIRED)
endif()

add_executable(14_dnn_classify classify.cpp)
target_include_directories(14_dnn_classify PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(14_dnn_classify PRIVATE ${OpenCV_LIBS})

add_executable(14_dnn_detect detect.cpp)
target_include_directories(14_dnn_detect PRIVATE ${IMAGE_TUTORIAL_COMMON_INCLUDE_DIR})
target_link_libraries(14_dnn_detect PRIVATE ${OpenCV_LIBS})
