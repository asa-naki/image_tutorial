// common/utils.hpp - 各セクション共通の小さなヘルパ関数群
#pragma once

#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>

namespace tutorial {

// 画像を読み込み、失敗時は分かりやすいメッセージで終了する。
inline cv::Mat load_image(const std::string& path,
                          int flags = cv::IMREAD_COLOR) {
    cv::Mat img = cv::imread(path, flags);
    if (img.empty()) {
        std::cerr << "[error] failed to load image: " << path << "\n"
                  << "        place a sample under image_tutorial/data/ "
                     "(see data/README.md)" << std::endl;
        std::exit(1);
    }
    return img;
}

// 複数枚の画像をウィンドウに表示し、ESC または 'q' まで待機する。
// pairs: {window title, image} の vector。
inline void show_and_wait(
    const std::vector<std::pair<std::string, cv::Mat>>& pairs) {
    for (const auto& p : pairs) {
        if (!p.second.empty()) {
            cv::imshow(p.first, p.second);
        }
    }
    std::cout << "[info] press ESC or 'q' to close windows" << std::endl;
    while (true) {
        int key = cv::waitKey(0) & 0xFF;
        if (key == 27 || key == 'q') break;
    }
    cv::destroyAllWindows();
}

inline void show_and_wait(const std::string& title, const cv::Mat& img) {
    show_and_wait({{title, img}});
}

// 引数 argv から index 番目を取得し、無ければデフォルト値を返す。
inline std::string arg_or(int argc, char** argv, int index,
                          const std::string& fallback) {
    if (index < argc) return std::string(argv[index]);
    return fallback;
}

}  // namespace tutorial
