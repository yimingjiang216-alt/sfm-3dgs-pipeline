# Image -> COLMAP SfM -> 3D Gaussian Splatting

用一组自己拍的多视角照片，走通「稀疏重建 -> 位姿求解 -> 3DGS 训练 -> 新视角合成」的完整链路。

COLMAP 和 3D Gaussian Splatting 都是上游开源项目，本仓库不包含它们的源码。
本仓库做的是：把两者衔接起来跑通，并解决衔接过程中出现的环境和格式问题。

---

## 一、链路

```
手机环绕拍摄多视角照片
      |
      v
COLMAP  feature_extractor  (SIFT, 强制 SIMPLE_PINHOLE 模型)
        exhaustive_matcher (40 张，穷举匹配)
        mapper             (增量式 SfM: 稀疏点云 + 相机位姿)
      |
      v
3D Gaussian Splatting  train.py  (7000 步)
      |
      v
后处理  render_custom.py  自写轨道相机轨迹，渲染新视角
        trajectory.py     轨迹生成 (orbit / push / zoom)
        eval_metrics.py   与真值帧比对 PSNR / SSIM / LPIPS
      |
      v
ffmpeg 合成环绕视频
```

数据规模：拍摄 130 余张，选用连续 40 张，全部影像注册成功。

---

## 二、本仓库的文件

| 文件 | 作用 |
|---|---|
| `notebooks/kaggle_pipeline.ipynb` | 完整的 Kaggle 端流程（COLMAP -> 训练 -> 渲染 -> 视频） |
| `scripts/trajectory.py` | 相机轨迹生成器，输出 orbit / push / zoom 等路径，本地可跑，不需要 GPU |
| `scripts/render_custom.py` | 训练完成后按自定义轨迹渲染新视角。需要放在 `gaussian-splatting/` 目录内运行 |
| `scripts/eval_metrics.py` | 渲染帧与真值帧的 PSNR / SSIM / LPIPS，本地可跑 |

需要注意 `render_custom.py` 必须放进上游 `gaussian-splatting` 仓库目录里执行
（这样 `from gaussian_renderer import render` 才能解析），它不是独立脚本。

---

## 三、环境与分工

| 环节 | 在哪跑 | 原因 |
|---|---|---|
| 轨迹生成、指标评估 | 本地 CPU | 这部分不需要 GPU |
| COLMAP SfM | Kaggle（CPU 模式） | 无本地 GPU 环境 |
| 3DGS 训练 | Kaggle 免费 T4 | 训练需要 CUDA |

所以「训练在 Kaggle、轨迹与评估在本地」是这个项目的实际分工，不是刻意拆分。

---

## 四、衔接过程中定位并解决的问题

这一部分是本项目的主要实际工作。跑通这条链路的难点几乎全在两个工具的衔接处。

| 现象 | 原因 | 处理 |
|---|---|---|
| COLMAP 正常跑完，但 3DGS 读不了它的输出 | COLMAP 默认相机模型含畸变参数，3DGS 只接受针孔模型 | `feature_extractor` 强制 `--ImageReader.camera_model SIMPLE_PINHOLE` |
| COLMAP 在无显示环境直接崩溃 | Qt 找不到显示后端 | `QT_QPA_PLATFORM=offscreen` |
| CUDA 扩展编译失败 | 安装的 torch 版本与 Kaggle 系统 CUDA 不匹配 | 固定 `torch cu121` + `TORCH_CUDA_ARCH_LIST=7.5` |
| 子模块扩展报缺 `libc10` 符号 | 编译顺序问题 | 先 `import torch` 再编译子模块 |
| COLMAP 内存爆掉 | 原图分辨率过高 | 缩放到 1600 px + 限制线程数 |
| 全量穷举匹配太慢 | 有序环绕拍摄用不上穷举 | 改 `sequential_matcher`（40 张规模下穷举亦可接受，两种都验证过） |

---

## 五、复现

```
1. 把 gaussian-splatting 克隆到工作目录（本仓库不含它）
2. 上传照片，跑 notebooks/kaggle_pipeline.ipynb
3. 下载训练输出与渲染帧
4. 本地跑 scripts/eval_metrics.py 算指标
```

---

## 六、已知不足

- 拍摄是手机环绕一圈，基线短、视角变化有限，重建质量受限于此；
  更好的做法是分层多角度拍摄（俯视 / 平视 / 仰视各一组）。
- 3DGS 训练只到 7000 步，未做完整收敛验证。
- 场景是桌面小物体，不涉及大规模场景或分块重建。
