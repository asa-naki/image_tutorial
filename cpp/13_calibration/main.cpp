// 13_calibration: チェスボードを使ったカメラキャリブレーションと歪み補正
// Usage:
//   ./13_calibration <chessboard_dir> [pattern_cols pattern_rows square_size]
//   default: ../data/chessboard 9 6 1.0
#include <iostream>
#include <filesystem>
#include <opencv2/opencv.hpp>
#include <Eigen/Dense>
#include "common/utils.hpp"

namespace fs = std::filesystem;

int main(int argc, char** argv) {
    const std::string dir = tutorial::arg_or(argc, argv, 1, "../data/chessboard");
    int cols = std::stoi(tutorial::arg_or(argc, argv, 2, "9"));
    int rows = std::stoi(tutorial::arg_or(argc, argv, 3, "6"));
    float square = std::stof(tutorial::arg_or(argc, argv, 4, "1.0"));

    cv::Size pattern(cols, rows);

    // 3D 物体座標 (Z=0 平面の格子点)
    std::vector<cv::Point3f> obj_template;
    for (int i = 0; i < rows; ++i)
        for (int j = 0; j < cols; ++j)
            obj_template.emplace_back(j * square, i * square, 0.f);

    std::vector<std::vector<cv::Point3f>> obj_points;
    std::vector<std::vector<cv::Point2f>> img_points;
    cv::Size img_size;

    if (!fs::exists(dir)) {
        std::cerr << "[error] not found: " << dir << "\n"
                  << "        run image_tutorial/data/fetch_samples.sh" << std::endl;
        return 1;
    }

    int used = 0, total = 0;
    cv::Mat last_with_corners;
    for (const auto& entry : fs::directory_iterator(dir)) {
        if (!entry.is_regular_file()) continue;
        auto ext = entry.path().extension().string();
        if (ext != ".jpg" && ext != ".png" && ext != ".jpeg") continue;
        ++total;
        cv::Mat img = cv::imread(entry.path().string(), cv::IMREAD_COLOR);
        if (img.empty()) continue;
        cv::Mat gray;
        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
        std::vector<cv::Point2f> corners;
        bool found = cv::findChessboardCorners(
            gray, pattern, corners,
            cv::CALIB_CB_ADAPTIVE_THRESH | cv::CALIB_CB_NORMALIZE_IMAGE);
        if (!found) {
            std::cerr << "[skip] no corners: " << entry.path().filename() << std::endl;
            continue;
        }
        cv::cornerSubPix(gray, corners, {11, 11}, {-1, -1},
                         {cv::TermCriteria::EPS + cv::TermCriteria::COUNT, 30, 0.01});
        obj_points.push_back(obj_template);
        img_points.push_back(corners);
        img_size = gray.size();
        cv::drawChessboardCorners(img, pattern, corners, true);
        last_with_corners = img;
        ++used;
    }
    std::cout << "found chessboard in " << used << "/" << total << " images" << std::endl;
    if (used < 5) {
        std::cerr << "[error] need >= 5 valid images" << std::endl;
        return 1;
    }

    cv::Mat K, dist;
    std::vector<cv::Mat> rvecs, tvecs;
    double rms = cv::calibrateCamera(obj_points, img_points, img_size,
                                     K, dist, rvecs, tvecs);
    std::cout << "RMS reprojection error (OpenCV) = " << rms << "\n"
              << "K =\n" << K << "\n"
              << "dist = " << dist.t() << std::endl;

    // Eigen で 1 視点目の再投影誤差を手計算 (検算)
    {
        Eigen::Matrix3d Ke;
        for (int r = 0; r < 3; ++r)
            for (int c = 0; c < 3; ++c) Ke(r, c) = K.at<double>(r, c);
        std::vector<cv::Point2f> reproj;
        cv::projectPoints(obj_points[0], rvecs[0], tvecs[0], K, dist, reproj);
        double err = 0;
        for (size_t i = 0; i < reproj.size(); ++i) {
            double dx = reproj[i].x - img_points[0][i].x;
            double dy = reproj[i].y - img_points[0][i].y;
            err += dx * dx + dy * dy;
        }
        err = std::sqrt(err / reproj.size());
        std::cout << "view0 reprojection error (manual) = " << err << "\n"
                  << "Eigen K =\n" << Ke << std::endl;
    }

    // 歪み補正の例 (最後に処理した画像)
    cv::Mat undist;
    cv::undistort(last_with_corners, undist, K, dist);

    tutorial::show_and_wait({
        {"chessboard corners", last_with_corners},
        {"undistorted", undist},
    });
    return 0;
}
