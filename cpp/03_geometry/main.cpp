// 03_geometry: 幾何変換 (resize / rotate / affine / perspective)
// Eigen で 3x3 のホモグラフィ行列を組み立て cv::Mat に流し込む例も含む。
// Usage: ./03_geometry <input_image>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <Eigen/Dense>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string in_path = tutorial::arg_or(argc, argv, 1, "../data/lena.png");
    cv::Mat src = tutorial::load_image(in_path);
    const cv::Size sz = src.size();

    // 1) リサイズ (半分)
    cv::Mat half;
    cv::resize(src, half, cv::Size(), 0.5, 0.5, cv::INTER_AREA);

    // 2) 回転 (中心 30deg) - getRotationMatrix2D は 2x3 アフィン行列
    cv::Point2f center(sz.width / 2.f, sz.height / 2.f);
    cv::Mat M_rot = cv::getRotationMatrix2D(center, 30.0, 1.0);
    cv::Mat rotated;
    cv::warpAffine(src, rotated, M_rot, sz);

    // 3) アフィン (3 点対応)
    cv::Point2f src_pts[3] = {{0, 0}, {sz.width - 1.f, 0}, {0, sz.height - 1.f}};
    cv::Point2f dst_pts[3] = {{sz.width * 0.1f, sz.height * 0.2f},
                              {sz.width * 0.9f, sz.height * 0.1f},
                              {sz.width * 0.2f, sz.height * 0.9f}};
    cv::Mat M_aff = cv::getAffineTransform(src_pts, dst_pts);
    cv::Mat affined;
    cv::warpAffine(src, affined, M_aff, sz);

    // 4) Eigen で 3x3 ホモグラフィ行列を組み、cv::warpPerspective に渡す
    //    例: 単純なせん断 + スケール
    Eigen::Matrix3d H_eig;
    H_eig << 1.0, 0.2, 0.0,
             0.1, 1.0, 0.0,
             0.0, 0.0, 1.0;
    cv::Mat H(3, 3, CV_64F);
    for (int r = 0; r < 3; ++r)
        for (int c = 0; c < 3; ++c) H.at<double>(r, c) = H_eig(r, c);

    cv::Mat warped;
    cv::warpPerspective(src, warped, H, sz);

    std::cout << "Eigen H =\n" << H_eig << std::endl;

    tutorial::show_and_wait({
        {"src", src},
        {"resize x0.5", half},
        {"rotate 30deg", rotated},
        {"affine 3pt", affined},
        {"perspective (Eigen H)", warped},
    });
    return 0;
}
