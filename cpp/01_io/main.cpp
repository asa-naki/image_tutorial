// 01_io: 画像の入出力と表示
// Usage: ./01_io <input_image> [output_path]
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    const std::string out_path = tutorial::arg_or(argc, argv, 2, "01_io_out.png");

    // カラー (BGR) として読み込み
    cv::Mat color = tutorial::load_image(in_path, cv::IMREAD_COLOR);
    // グレースケールとして読み込み
    cv::Mat gray = tutorial::load_image(in_path, cv::IMREAD_GRAYSCALE);

    std::cout << "size  : " << color.cols << " x " << color.rows << "\n"
              << "chans : " << color.channels() << "\n"
              << "dtype : " << color.type() << " (CV_8UC3=" << CV_8UC3 << ")"
              << std::endl;

    // PNG として保存
    if (!cv::imwrite(out_path, color)) {
        std::cerr << "failed to write: " << out_path << std::endl;
        return 1;
    }
    std::cout << "saved : " << out_path << std::endl;

    tutorial::show_and_wait({{"color", color}, {"gray", gray}});
    return 0;
}
