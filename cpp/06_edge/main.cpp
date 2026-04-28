// 06_edge: Sobel / Laplacian / Canny によるエッジ検出
// Usage: ./06_edge <input_image>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/building.jpg");
    cv::Mat gray = tutorial::load_image(in_path, cv::IMREAD_GRAYSCALE);

    // ノイズ低減
    cv::Mat blur;
    cv::GaussianBlur(gray, blur, cv::Size(3, 3), 0);

    // 1) Sobel (x, y)
    cv::Mat gx, gy, abs_gx, abs_gy, sobel_mag;
    cv::Sobel(blur, gx, CV_16S, 1, 0, 3);
    cv::Sobel(blur, gy, CV_16S, 0, 1, 3);
    cv::convertScaleAbs(gx, abs_gx);
    cv::convertScaleAbs(gy, abs_gy);
    cv::addWeighted(abs_gx, 0.5, abs_gy, 0.5, 0, sobel_mag);

    // 2) Laplacian
    cv::Mat lap, abs_lap;
    cv::Laplacian(blur, lap, CV_16S, 3);
    cv::convertScaleAbs(lap, abs_lap);

    // 3) Canny
    cv::Mat canny;
    cv::Canny(blur, canny, 80, 160);

    tutorial::show_and_wait({
        {"gray", gray},
        {"sobel x", abs_gx},
        {"sobel y", abs_gy},
        {"sobel mag", sobel_mag},
        {"laplacian", abs_lap},
        {"canny 80/160", canny},
    });
    return 0;
}
