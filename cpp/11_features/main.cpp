// 11_features: ORB / AKAZE / SIFT による特徴点検出と BFMatcher、RANSAC ホモグラフィ
// Usage: ./11_features <img1> <img2>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

static void run_detector(const std::string& name,
                         const cv::Ptr<cv::Feature2D>& det, int norm_type,
                         const cv::Mat& img1, const cv::Mat& img2,
                         std::vector<std::pair<std::string, cv::Mat>>& views) {
    std::vector<cv::KeyPoint> kp1, kp2;
    cv::Mat des1, des2;
    det->detectAndCompute(img1, cv::noArray(), kp1, des1);
    det->detectAndCompute(img2, cv::noArray(), kp2, des2);
    if (des1.empty() || des2.empty()) {
        std::cerr << "[" << name << "] no descriptors" << std::endl;
        return;
    }

    cv::BFMatcher matcher(norm_type);
    std::vector<std::vector<cv::DMatch>> knn;
    matcher.knnMatch(des1, des2, knn, 2);

    // Lowe's ratio test
    std::vector<cv::DMatch> good;
    for (const auto& m : knn) {
        if (m.size() == 2 && m[0].distance < 0.75f * m[1].distance) {
            good.push_back(m[0]);
        }
    }

    std::cout << "[" << name << "] kp1=" << kp1.size()
              << " kp2=" << kp2.size()
              << " good=" << good.size() << std::endl;

    // RANSAC でホモグラフィ推定
    cv::Mat H, inlier_mask;
    if (good.size() >= 4) {
        std::vector<cv::Point2f> p1, p2;
        for (const auto& g : good) {
            p1.push_back(kp1[g.queryIdx].pt);
            p2.push_back(kp2[g.trainIdx].pt);
        }
        H = cv::findHomography(p1, p2, cv::RANSAC, 3.0, inlier_mask);
    }

    cv::Mat vis;
    cv::drawMatches(img1, kp1, img2, kp2, good, vis,
                    cv::Scalar::all(-1), cv::Scalar::all(-1),
                    inlier_mask.empty()
                        ? std::vector<char>{}
                        : std::vector<char>(inlier_mask.begin<uchar>(),
                                            inlier_mask.end<uchar>()));
    views.push_back({name, vis});
}

int main(int argc, char** argv) {
    const std::string p1 = tutorial::arg_or(argc, argv, 1, "../data/book1.jpg");
    const std::string p2 = tutorial::arg_or(argc, argv, 2, "../data/book2.jpg");
    cv::Mat img1 = tutorial::load_image(p1, cv::IMREAD_GRAYSCALE);
    cv::Mat img2 = tutorial::load_image(p2, cv::IMREAD_GRAYSCALE);

    std::vector<std::pair<std::string, cv::Mat>> views;

    run_detector("ORB",   cv::ORB::create(2000),   cv::NORM_HAMMING, img1, img2, views);
    run_detector("AKAZE", cv::AKAZE::create(),     cv::NORM_HAMMING, img1, img2, views);

    // SIFT は OpenCV 4.4+ で features2d 内部にある (特許切れのため main に移動)。
    // 古いビルドで利用不可な場合は例外を握りつぶす。
    try {
        run_detector("SIFT", cv::SIFT::create(), cv::NORM_L2, img1, img2, views);
    } catch (const cv::Exception& e) {
        std::cerr << "[SIFT] not available: " << e.what() << std::endl;
    }

    tutorial::show_and_wait(views);
    return 0;
}
