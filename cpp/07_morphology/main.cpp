// 07_morphology: erode / dilate / open / close / gradient / tophat / blackhat
// Usage: ./07_morphology <input_image>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat gray = tutorial::load_image(in_path, cv::IMREAD_GRAYSCALE);

    // 二値画像 (Otsu) を入力に使う
    cv::Mat bin;
    cv::threshold(gray, bin, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));

    cv::Mat erode, dilate, open, close, grad, tophat, blackhat;
    cv::erode(bin, erode, kernel);
    cv::dilate(bin, dilate, kernel);
    cv::morphologyEx(bin, open,    cv::MORPH_OPEN,     kernel);
    cv::morphologyEx(bin, close,   cv::MORPH_CLOSE,    kernel);
    cv::morphologyEx(gray, grad,    cv::MORPH_GRADIENT, kernel);
    cv::morphologyEx(gray, tophat,  cv::MORPH_TOPHAT,   kernel);
    cv::morphologyEx(gray, blackhat, cv::MORPH_BLACKHAT, kernel);

    tutorial::show_and_wait({
        {"binary", bin},
        {"erode", erode},
        {"dilate", dilate},
        {"open", open},
        {"close", close},
        {"gradient", grad},
        {"tophat", tophat},
        {"blackhat", blackhat},
    });
    return 0;
}
