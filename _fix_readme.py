# -*- coding: utf-8 -*-
import io
p = "README.md"
s = io.open(p, encoding="utf-8").read()

s = s.replace(
"用一组环绕拍摄的多视角照片（手机拍摄 130 余张，选用连续环绕的一圈共 40 张），\n走通「稀疏重建 -> 位姿求解 -> 3DGS 训练 -> 新视角合成」的完整链路。",
"用一组环绕拍摄的多视角照片（手机拍摄 130 余张，上传其中 120 张），\n走通「稀疏重建 -> 位姿求解 -> 3DGS 训练 -> 新视角合成」的链路。")

s = s.replace("| 输入影像 | 40 张（从 130 余张中选连续环绕的一圈） |",
              "| 输入影像 | 120 张（手机环绕拍摄，共 130 余张） |")
s = s.replace("| SfM 影像注册 | 40 / 40 全部注册成功 |",
              "| SfM 相机注册 | 输出 10 个相机（日志共 38 次影像注册；匹配阶段 423 对有效匹配） |")

s = s.replace("COLMAP  feature_extractor  (SIFT nfeatures=2000, 强制 SIMPLE_PINHOLE 模型)",
              "COLMAP  feature_extractor  (SIFT, 强制 SIMPLE_PINHOLE 模型)")
s = s.replace("        sequential_matcher (环绕拍摄有天然顺序)",
              "        sequential_matcher (环绕拍摄有天然顺序, 实测 423 对有效匹配)")

s = s.replace("- 拍摄是环绕一圈，基线短、视角变化有限，重建质量受限于此；",
              "- 相机注册率低：120 张输入最终只输出 10 个训练相机。日志显示匹配阶段只有 423 对\n  有效匹配，匹配对不足限制了增量重建的扩展范围，后段出现 “No good initial image pair\n  found” 后停止扩张。\n- 拍摄是环绕一圈，基线短、视角变化有限，重建质量受限于此；")

io.open(p, "w", encoding="utf-8").write(s)
print("done")
