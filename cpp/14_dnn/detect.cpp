// 14_dnn / detect.cpp: ONNX 物体検出モデル (例: YOLOv5s/YOLOv8n)
// Usage: ./14_dnn_detect <onnx_model> <labels.txt> <image> [conf_thr] [nms_thr]
//
// 入力: 640x640 RGB, scale=1/255, out shape は (1, 25200, 85) (yolov5)
//       または (1, 84, 8400) (yolov8)。両方を簡易ハンドリング。
#include <fstream>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "usage: " << argv[0]
                  << " <onnx_model> <labels.txt> <image> [conf=0.25] [nms=0.45]\n"
                  << "       see 14_dnn/README.md for model download instructions"
                  << std::endl;
        return 1;
    }
    const std::string model_path = argv[1];
    const std::string labels_path = argv[2];
    const std::string image_path  = argv[3];
    float conf_thr = (argc > 4) ? std::stof(argv[4]) : 0.25f;
    float nms_thr  = (argc > 5) ? std::stof(argv[5]) : 0.45f;

    std::vector<std::string> labels;
    {
        std::ifstream ifs(labels_path);
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
    const int IN = 640;
    cv::Mat blob = cv::dnn::blobFromImage(img, 1.0 / 255.0, cv::Size(IN, IN),
                                          cv::Scalar(), true, false);
    net.setInput(blob);
    cv::Mat out = net.forward();

    // shape を判定して (N, attrs) 形式に正規化
    cv::Mat det;
    if (out.dims == 3) {
        if (out.size[1] < out.size[2]) {
            // YOLOv8: (1, attrs=84, N)
            det = cv::Mat(out.size[2], out.size[1], CV_32F);
            for (int n = 0; n < out.size[2]; ++n)
                for (int a = 0; a < out.size[1]; ++a)
                    det.at<float>(n, a) = out.ptr<float>(0, a)[n];
        } else {
            // YOLOv5: (1, N, 85)
            det = cv::Mat(out.size[1], out.size[2], CV_32F,
                          (void*)out.ptr<float>(0));
            det = det.clone();
        }
    } else {
        std::cerr << "[error] unexpected output shape" << std::endl;
        return 1;
    }

    const int N = det.rows;
    const int A = det.cols;
    const int num_classes = A - 5;  // YOLOv5: x,y,w,h,obj + classes
    const bool yolov8 = (num_classes < 0);  // yolov8 は obj 抜き → A = 4 + classes

    std::vector<cv::Rect> boxes;
    std::vector<float> scores;
    std::vector<int> class_ids;

    float sx = (float)img.cols / IN;
    float sy = (float)img.rows / IN;

    for (int i = 0; i < N; ++i) {
        const float* row = det.ptr<float>(i);
        float cx = row[0], cy = row[1], w = row[2], h = row[3];
        float obj = yolov8 ? 1.0f : row[4];
        int cls_off = yolov8 ? 4 : 5;
        int cls_count = yolov8 ? (A - 4) : (A - 5);

        // クラス最大スコア
        int best_c = 0;
        float best_s = 0;
        for (int c = 0; c < cls_count; ++c) {
            float s = row[cls_off + c];
            if (s > best_s) { best_s = s; best_c = c; }
        }
        float conf = obj * best_s;
        if (conf < conf_thr) continue;

        int x = static_cast<int>((cx - w / 2) * sx);
        int y = static_cast<int>((cy - h / 2) * sy);
        int bw = static_cast<int>(w * sx);
        int bh = static_cast<int>(h * sy);
        boxes.emplace_back(x, y, bw, bh);
        scores.push_back(conf);
        class_ids.push_back(best_c);
    }

    std::vector<int> keep;
    cv::dnn::NMSBoxes(boxes, scores, conf_thr, nms_thr, keep);

    cv::Mat draw = img.clone();
    for (int i : keep) {
        cv::rectangle(draw, boxes[i], cv::Scalar(0, 255, 0), 2);
        std::string lbl = (class_ids[i] < (int)labels.size())
            ? labels[class_ids[i]]
            : std::to_string(class_ids[i]);
        lbl += cv::format(" %.2f", scores[i]);
        cv::putText(draw, lbl, boxes[i].tl() + cv::Point(0, -5),
                    cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 1);
    }
    std::cout << "kept " << keep.size() << "/" << boxes.size() << " boxes" << std::endl;
    tutorial::show_and_wait("detection", draw);
    return 0;
}
