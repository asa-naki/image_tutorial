// 05_smoothing: 平滑化フィルタ (Box / Gaussian / Median / Bilateral)
// Usage: ./05_smoothing <input_image>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat src = tutorial::load_image(in_path);

    // ノイズ付加 (比較用)
    cv::Mat noisy = src.clone();
    cv::Mat noise(src.size(), src.type());
    cv::randn(noise, 0, 25);
    noisy += noise;

    cv::Mat box, gauss, median, bilat;
    cv::blur(noisy, box, cv::Size(5, 5));                   // ボックス平均
    cv::GaussianBlur(noisy, gauss, cv::Size(5, 5), 1.5);    // ガウシアン
    cv::medianBlur(noisy, median, 5);                       // メディアン
    cv::bilateralFilter(noisy, bilat, 9, 75, 75);           // バイラテラル

    tutorial::show_and_wait({
        {"src", src},
        {"noisy", noisy},
        {"box 5x5", box},
        {"gaussian 5x5 sigma=1.5", gauss},
        {"median 5", median},
        {"bilateral", bilat},
    });
    return 0;
}
