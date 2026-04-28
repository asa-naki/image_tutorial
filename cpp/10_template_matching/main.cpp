// 10_template_matching: matchTemplate + マルチスケール
// Usage: ./10_template_matching <scene> <template>
#include <iostream>
#include <opencv2/opencv.hpp>
#include "common/utils.hpp"

int main(int argc, char** argv) {
    const std::string scene_path = tutorial::arg_or(argc, argv, 1, "../data/scene.png");
    const std::string tmpl_path  = tutorial::arg_or(argc, argv, 2, "../data/template.png");

    cv::Mat scene = tutorial::load_image(scene_path);
    cv::Mat tmpl  = tutorial::load_image(tmpl_path);

    // 1) シングルスケール (NCC)
    cv::Mat result;
    cv::matchTemplate(scene, tmpl, result, cv::TM_CCOEFF_NORMED);
    double min_v, max_v;
    cv::Point min_p, max_p;
    cv::minMaxLoc(result, &min_v, &max_v, &min_p, &max_p);

    cv::Mat draw = scene.clone();
    cv::Rect best_box(max_p, tmpl.size());
    cv::rectangle(draw, best_box, cv::Scalar(0, 255, 0), 2);
    cv::putText(draw, cv::format("NCC=%.3f", max_v),
                max_p + cv::Point(0, -5), cv::FONT_HERSHEY_SIMPLEX,
                0.6, cv::Scalar(0, 255, 0), 2);

    // スコアマップを正規化して可視化
    cv::Mat score_vis;
    cv::normalize(result, score_vis, 0, 255, cv::NORM_MINMAX);
    score_vis.convertTo(score_vis, CV_8U);

    // 2) マルチスケール (テンプレートをスケール変えて最良)
    double best = -1;
    cv::Rect best_ms;
    double best_scale = 1.0;
    for (double s = 0.5; s <= 1.5; s += 0.1) {
        cv::Mat tmpl_s;
        cv::resize(tmpl, tmpl_s, cv::Size(), s, s);
        if (tmpl_s.cols >= scene.cols || tmpl_s.rows >= scene.rows) continue;
        cv::Mat r;
        cv::matchTemplate(scene, tmpl_s, r, cv::TM_CCOEFF_NORMED);
        double mn, mx;
        cv::Point pmn, pmx;
        cv::minMaxLoc(r, &mn, &mx, &pmn, &pmx);
        if (mx > best) {
            best = mx;
            best_ms = cv::Rect(pmx, tmpl_s.size());
            best_scale = s;
        }
    }
    cv::Mat draw_ms = scene.clone();
    cv::rectangle(draw_ms, best_ms, cv::Scalar(0, 255, 255), 2);
    cv::putText(draw_ms, cv::format("scale=%.1f score=%.3f", best_scale, best),
                best_ms.tl() + cv::Point(0, -5), cv::FONT_HERSHEY_SIMPLEX,
                0.6, cv::Scalar(0, 255, 255), 2);

    std::cout << "single-scale NCC = " << max_v << " at " << max_p << "\n"
              << "multi-scale best score = " << best
              << " at scale " << best_scale << std::endl;

    tutorial::show_and_wait({
        {"scene", scene},
        {"template", tmpl},
        {"score map", score_vis},
        {"single-scale", draw},
        {"multi-scale", draw_ms},
    });
    return 0;
}
