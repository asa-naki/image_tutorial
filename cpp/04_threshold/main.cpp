// 04_threshold: 固定閾値 / Otsu / Adaptive
// Usage: ./04_threshold <input_image>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat gray = tutorial::load_image(in_path, cv::IMREAD_GRAYSCALE);

    // 1) 固定閾値 (127)
    cv::Mat fixed_bin;
    cv::threshold(gray, fixed_bin, 127, 255, cv::THRESH_BINARY);

    // 2) Otsu (自動閾値)
    cv::Mat otsu_bin;
    double otsu_thr = cv::threshold(gray, otsu_bin, 0, 255,
                                    cv::THRESH_BINARY | cv::THRESH_OTSU);

    // 3) Adaptive (Mean / Gaussian)
    cv::Mat adapt_mean, adapt_gauss;
    cv::adaptiveThreshold(gray, adapt_mean, 255,
                          cv::ADAPTIVE_THRESH_MEAN_C, cv::THRESH_BINARY, 31, 5);
    cv::adaptiveThreshold(gray, adapt_gauss, 255,
                          cv::ADAPTIVE_THRESH_GAUSSIAN_C, cv::THRESH_BINARY, 31, 5);

    std::cout << "Otsu threshold = " << otsu_thr << std::endl;

    tutorial::show_and_wait({
        {"gray", gray},
        {"fixed (127)", fixed_bin},
        {"otsu", otsu_bin},
        {"adaptive mean", adapt_mean},
        {"adaptive gauss", adapt_gauss},
    });
    return 0;
}
