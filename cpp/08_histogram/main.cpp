// 08_histogram: calcHist / equalizeHist / CLAHE
// Usage: ./08_histogram <input_image>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

// 1ch のヒストグラムを画像として描画
static cv::Mat draw_hist(const cv::Mat& gray, cv::Scalar color = {255, 255, 255}) {
    int hist_size = 256;
    float range[] = {0, 256};
    const float* hist_range = {range};
    cv::Mat hist;
    cv::calcHist(&gray, 1, 0, cv::Mat(), hist, 1, &hist_size, &hist_range);

    int w = 512, h = 300;
    int bin_w = cvRound((double)w / hist_size);
    cv::Mat canvas(h, w, CV_8UC3, cv::Scalar(0, 0, 0));
    cv::normalize(hist, hist, 0, h, cv::NORM_MINMAX);
    for (int i = 1; i < hist_size; ++i) {
        cv::line(canvas,
                 {bin_w * (i - 1), h - cvRound(hist.at<float>(i - 1))},
                 {bin_w * i,       h - cvRound(hist.at<float>(i))},
                 color, 2);
    }
    return canvas;
}

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat gray = tutorial::load_image(in_path, cv::IMREAD_GRAYSCALE);

    cv::Mat eq;
    cv::equalizeHist(gray, eq);

    auto clahe = cv::createCLAHE(2.0, cv::Size(8, 8));
    cv::Mat clahe_out;
    clahe->apply(gray, clahe_out);

    tutorial::show_and_wait({
        {"gray", gray},
        {"hist of gray", draw_hist(gray)},
        {"equalized", eq},
        {"hist of eq", draw_hist(eq)},
        {"CLAHE", clahe_out},
        {"hist of CLAHE", draw_hist(clahe_out)},
    });
    return 0;
}
