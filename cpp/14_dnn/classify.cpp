// 14_dnn / classify.cpp: ONNX 画像分類モデル (例: MobileNetV2)
// Usage: ./14_dnn_classify <onnx_model> <labels.txt> <image>
#include <fstream>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "usage: " << argv[0] << " <onnx_model> <labels.txt> <image>\n"
                  << "       see 14_dnn/README.md for model download instructions"
                  << std::endl;
        return 1;
    }
    const std::string model_path = argv[1];
    const std::string labels_path = argv[2];
    const std::string image_path = argv[3];

    // ラベル読み込み
    std::vector<std::string> labels;
    {
        std::ifstream ifs(labels_path);
        if (!ifs) {
            std::cerr << "[error] failed to open labels: " << labels_path << std::endl;
            return 1;
        }
        std::string line;
        while (std::getline(ifs, line)) labels.push_back(line);
    }

    cv::dnn::Net net;
    try {
        net = cv::dnn::readNetFromONNX(model_path);
    } catch (const cv::Exception& e) {
        std::cerr << "[error] failed to load ONNX model: " << e.what() << std::endl;
        return 1;
    }
    net.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
    net.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);

    cv::Mat img = tutorial::load_image(image_path);

    // ImageNet 系の前処理: 224x224, mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225]
    cv::Mat blob = cv::dnn::blobFromImage(
        img, 1.0 / 255.0, cv::Size(224, 224),
        cv::Scalar(0.485 * 255, 0.456 * 255, 0.406 * 255),
        true, false);
    // チャンネルごとの std で割る (blob は CHW)
    static const float stds[3] = {0.229f, 0.224f, 0.225f};
    for (int c = 0; c < 3; ++c) {
        cv::Mat ch(blob.size[2], blob.size[3], CV_32F,
                   blob.ptr<float>(0, c));
        ch /= stds[c];
    }

    net.setInput(blob);
    cv::Mat out = net.forward();  // 1 x N

    // softmax + top-5
    cv::Mat probs;
    cv::exp(out - *std::max_element(out.begin<float>(), out.end<float>()), probs);
    probs /= cv::sum(probs)[0];

    std::vector<std::pair<float, int>> ranked;
    for (int i = 0; i < probs.cols; ++i) ranked.push_back({probs.at<float>(0, i), i});
    std::partial_sort(ranked.begin(), ranked.begin() + 5, ranked.end(),
                      [](auto& a, auto& b) { return a.first > b.first; });

    std::cout << "Top-5:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        int idx = ranked[i].second;
        const std::string lbl = (idx < (int)labels.size()) ? labels[idx] : std::to_string(idx);
        std::cout << "  " << ranked[i].first << "\t" << lbl << std::endl;
    }

    cv::Mat draw = img.clone();
    cv::putText(draw, labels[ranked[0].second], {10, 30},
                cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(0, 255, 0), 2);
    tutorial::show_and_wait("classification", draw);
    return 0;
}
