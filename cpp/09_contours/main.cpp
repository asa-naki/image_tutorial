// 09_contours: findContours / drawContours / 近似 / モーメント
// Usage: ./09_contours <input_image>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat src = tutorial::load_image(in_path);
    cv::Mat gray;
    cv::cvtColor(src, gray, cv::COLOR_BGR2GRAY);

    cv::Mat bin;
    cv::threshold(gray, bin, 0, 255, cv::THRESH_BINARY_INV | cv::THRESH_OTSU);

    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    cv::findContours(bin, contours, hierarchy,
                     cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

    cv::Mat draw = src.clone();
    cv::drawContours(draw, contours, -1, cv::Scalar(0, 255, 0), 2);

    cv::Mat draw_bbox = src.clone();
    int n = 0;
    for (const auto& c : contours) {
        double area = cv::contourArea(c);
        if (area < 200) continue;  // ノイズ除外
        // 外接矩形と重心
        cv::Rect r = cv::boundingRect(c);
        cv::rectangle(draw_bbox, r, cv::Scalar(0, 0, 255), 2);

        cv::Moments m = cv::moments(c);
        if (m.m00 > 0) {
            cv::Point2f cog(m.m10 / m.m00, m.m01 / m.m00);
            cv::circle(draw_bbox, cog, 4, cv::Scalar(255, 0, 0), -1);
        }

        // 多角形近似
        std::vector<cv::Point> approx;
        cv::approxPolyDP(c, approx, 0.01 * cv::arcLength(c, true), true);
        std::cout << "contour " << n++
                  << " area=" << area
                  << " verts(approx)=" << approx.size() << std::endl;
    }

    tutorial::show_and_wait({
        {"src", src},
        {"binary", bin},
        {"contours", draw},
        {"bbox + cog", draw_bbox},
    });
    return 0;
}
