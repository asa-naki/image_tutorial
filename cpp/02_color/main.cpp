// 02_color: 色空間変換とチャネル分離・HSV による色抽出
// Usage: ./02_color <input_image>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat bgr = tutorial::load_image(in_path);

    // 1) BGR -> Gray
    cv::Mat gray;
    cv::cvtColor(bgr, gray, cv::COLOR_BGR2GRAY);

    // 2) BGR -> HSV
    cv::Mat hsv;
    cv::cvtColor(bgr, hsv, cv::COLOR_BGR2HSV);

    // 3) チャネル分離 (BGR)
    std::vector<cv::Mat> bgr_ch;
    cv::split(bgr, bgr_ch);  // bgr_ch[0]=B, [1]=G, [2]=R

    // 4) HSV 閾値による赤色抽出
    //    赤は H=0 付近と H=180 付近の二箇所
    cv::Mat mask1, mask2, red_mask;
    cv::inRange(hsv, cv::Scalar(0, 80, 80), cv::Scalar(10, 255, 255), mask1);
    cv::inRange(hsv, cv::Scalar(170, 80, 80), cv::Scalar(180, 255, 255), mask2);
    red_mask = mask1 | mask2;

    cv::Mat red_only;
    bgr.copyTo(red_only, red_mask);

    std::cout << "BGR mean : " << cv::mean(bgr) << "\n"
              << "Gray mean: " << cv::mean(gray) << std::endl;

    tutorial::show_and_wait({
        {"bgr", bgr},
        {"gray", gray},
        {"hsv (visualized)", hsv},
        {"B", bgr_ch[0]},
        {"G", bgr_ch[1]},
        {"R", bgr_ch[2]},
        {"red mask", red_mask},
        {"red only", red_only},
    });
    return 0;
}
