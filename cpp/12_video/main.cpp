// 12_video: VideoCapture (file/camera) + VideoWriter + 背景差分
// Usage:
//   ./12_video <path_to_video>     # ファイル
//   ./12_video 0                    # カメラデバイス番号
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string src = tutorial::arg_or(argc, argv, 1, "../data/video.mp4");

    cv::VideoCapture cap;
    // 数字なら整数解釈してカメラとして開く
    if (src.size() <= 2 && std::all_of(src.begin(), src.end(), ::isdigit)) {
        cap.open(std::stoi(src));
    } else {
        cap.open(src);
    }
    if (!cap.isOpened()) {
        std::cerr << "[error] failed to open: " << src << "\n"
                  << "        place a video at data/video.mp4 or specify camera id"
                  << std::endl;
        return 1;
    }

    int w = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int h = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    double fps = cap.get(cv::CAP_PROP_FPS);
    if (fps <= 0) fps = 30;
    std::cout << "input: " << w << "x" << h << " @ " << fps << "fps" << std::endl;

    // 出力 (背景差分の前景マスクを保存)
    cv::VideoWriter writer("12_video_out.mp4",
                           cv::VideoWriter::fourcc('m', 'p', '4', 'v'),
                           fps, cv::Size(w, h), false);

    auto bgsub = cv::createBackgroundSubtractorMOG2();

    cv::Mat frame, fg;
    int idx = 0;
    while (cap.read(frame)) {
        bgsub->apply(frame, fg);
        cv::imshow("frame", frame);
        cv::imshow("fg mask", fg);
        if (writer.isOpened()) writer.write(fg);
        if ((cv::waitKey(1) & 0xFF) == 27) break;
        ++idx;
    }
    std::cout << "processed frames: " << idx
              << "\nsaved: 12_video_out.mp4" << std::endl;

    cap.release();
    writer.release();
    cv::destroyAllWindows();
    return 0;
}
