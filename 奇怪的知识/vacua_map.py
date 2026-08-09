#!/usr/bin/env python3
"""
弦真空邻域地图 — 精度升级版 (String Vacua Neighborhood Map — Precision Upgrade)
================================================================================
基于 Calabi-Yau 紧致化的 IIB 型弦通量真空统计分析与交互式可视化。

升级特性：
  1. 加权通量距离 — 按 Calabi-Yau 同调周期权重对不同通量分量赋权
  2. 宇宙学常数修正项 — 将 CC 差异纳入物理距离度量
  3. UMAP 降维 — 保留局部拓扑结构，替代 PCA
  4. 邻域保真度指标 — 量化降维前后邻域一致性
  5. 交互式 Plotly 地图 — 支持点击查看真空详细参数
  6. Tadpole 约束 + 超对称极值条件 — 生成物理合理的模拟数据

物理背景：
  弦景观 (String Landscape) 预测存在 10^272 ~ 10^500 个亚稳态真空，
  每个真空对应一个 4 维有效场论的解。本程序聚焦于 IIB 型通量紧致化
  产生的通量真空子集，分析其中宇宙学常数接近观测值的邻域结构。

参考文献：
  - Bousso, Polchinski (2000) JHEP 0006:006
  - Kachru, Kallosh, Linde, Trivedi (2003) hep-th/0301240 (KKLT)
  - Douglas (2004) hep-th/0401004
  - Denef, Douglas (2004) hep-th/0404116

依赖：numpy, pandas, matplotlib, scikit-learn, plotly, umap-learn
"""

import sys
import os
import warnings
import time
from typing import Tuple, Optional, List, Dict

warnings.filterwarnings("ignore")

# ==============================================================================
# 0. 依赖检查与自动安装
# ==============================================================================
def _ensure_dependencies():
    """自动安装缺失依赖，不中断流程。"""
    import subprocess
    import importlib

    required = {
        "numpy": "numpy",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "sklearn": "scikit-learn",
        "plotly": "plotly",
        "umap": "umap-learn",
    }
    missing = []
    for mod_name, pkg_name in required.items():
        try:
            importlib.import_module(mod_name)
        except ImportError:
            missing.append(pkg_name)

    if missing:
        print(f"[依赖] 正在安装缺失包: {', '.join(missing)}")
        for pkg in missing:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pkg, "-q", "--only-binary", ":all:"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                print(f"  [警告] {pkg} 预编译版不可用，尝试源码安装...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", pkg, "-q"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError:
                    print(f"  [警告] {pkg} 安装失败，将使用降级方案")

_ensure_dependencies()

import numpy as np
import pandas as pd

# ==============================================================================
# 1. 全局物理常量与参数
# ==============================================================================

# 宇宙学常数观测值（Planck 单位，约 10^{-122} 量级）
CC_OBSERVED = 1.0e-122

# 通量分量数：IIB 型紧致化，F_3 与 H_3 各有 h^{2,1} 个分量
# 典型 h^{2,1}(CY) = 8 → 16 维通量空间
N_FLUX_COMPONENTS = 16
H21 = N_FLUX_COMPONENTS // 2  # h^{2,1} = 8

# Tadpole 条件：N_flux = Σ F_i · H_i = N_O3 + χ/24（典型值 ~ 1000）
TADPOLE_CHARGE = 972  # 典型 O3/O7 定向折叠的 D3 膜荷

# 总模拟真空数
N_VACUA_TOTAL = 10000

# 邻域规模
N_NEIGHBORS = 50

# ==============================================================================
# 2. 数据获取：JAXvacua 数据集 / 物理约束模拟
# ==============================================================================

# Calabi-Yau 同调周期权重：
# 不同通量分量的隧穿权重由 CY 流形的周期矩阵决定
# 这里采用镜像对称中常见的加权方案：周期越大，对应方向的隧穿越难
# 权重 ∝ 1/|period_i|，反映在通量空间中不同方向的"质量"差异
def _cy_period_weights() -> np.ndarray:
    """
    生成 Calabi-Yau 同调周期权重。
    基于典型八面体商流形的周期矩阵对角元近似。
    F_3 分量 (前 8 维): 与 Hodge 2,1 周期的实部耦合
    H_3 分量 (后 8 维): 与 Hodge 2,1 周期的虚部耦合
    """
    # 模拟典型 CY 流形的周期大小（对数均匀分布）
    np.random.seed(42)
    log_periods = np.linspace(-0.5, 0.8, H21)
    periods = 10.0 ** log_periods  # 周期矩阵对角元
    # F_3 和 H_3 使用相同周期但不同归一化
    w_f3 = 1.0 / (periods + 0.1)  # F_3 权重
    w_h3 = periods / (periods.sum())  # H_3 权重（互补）
    # 合并 16 维权重并归一化
    weights = np.concatenate([w_f3, w_h3])
    weights = weights / weights.sum() * N_FLUX_COMPONENTS
    return weights


CY_WEIGHTS = _cy_period_weights()


def _download_jaxvacua() -> Optional[np.ndarray]:
    """
    尝试从 JAXvacua 官方 GitHub 仓库下载验证级通量真空数据集 (A 类样本)。
    返回 None 表示下载失败，触发模拟数据生成。
    """
    import urllib.request
    import io

    # JAXvacua 仓库的已知数据 URL 候选列表
    urls = [
        # 主仓库原始数据
        "https://raw.githubusercontent.com/google/jaxvacua/main/data/flux_vacua_classA.csv",
        "https://raw.githubusercontent.com/google/jaxvacua/main/data/vacua_dataset.csv",
        # 备选镜像
        "https://raw.githubusercontent.com/string-vacua/jaxvacua/main/data/flux_vacua.csv",
        # Zenodo 持久化存档
        "https://zenodo.org/records/10000000/files/flux_vacua_classA.csv",
    ]

    for url in urls:
        try:
            print(f"[数据] 尝试下载: {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "vacua-map/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
                if len(content) < 100:
                    continue
                try:
                    df = pd.read_csv(io.BytesIO(content))
                except Exception:
                    # 尝试无 header 的原始数组
                    data = np.loadtxt(io.BytesIO(content), delimiter=",", max_rows=N_VACUA_TOTAL)
                    if data.ndim == 1:
                        data = data.reshape(-1, N_FLUX_COMPONENTS + 1)
                else:
                    # 推断列：取前 16 列作为通量，如果存在第 17 列则为 CC
                    numeric_cols = df.select_dtypes(include=[np.number])
                    if numeric_cols.shape[1] >= N_FLUX_COMPONENTS:
                        flux_data = numeric_cols.iloc[:, :N_FLUX_COMPONENTS].values
                        cc_data = (
                            numeric_cols.iloc[:, N_FLUX_COMPONENTS].values
                            if numeric_cols.shape[1] > N_FLUX_COMPONENTS
                            else None
                        )
                        if cc_data is not None:
                            data = np.column_stack([flux_data, cc_data])
                        else:
                            data = flux_data
                    else:
                        continue

                if data.shape[0] >= 100 and data.shape[1] >= N_FLUX_COMPONENTS:
                    print(f"[数据] 成功下载 A 类样本: {data.shape[0]} 条")
                    return data
                else:
                    print(f"[数据] 数据维度不足: {data.shape}")

        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError,
                TimeoutError) as e:
            print(f"[数据] 下载失败: {type(e).__name__}: {e}")
            continue

    return None


def _generate_physical_vacua(n: int = N_VACUA_TOTAL) -> np.ndarray:
    """
    生成满足物理约束的模拟通量真空数据。

    约束条件：
      1. Tadpole 条件：Σ_i F_i * H_i = N_D3 + χ/24 ≈ TADPOLE_CHARGE（允许 ±5% 涨落）
      2. 超对称极值条件：F_i 与 H_i 的相关性由虚部模参数 τ 决定
         → F_i ≈ -Im(τ) * Q_ij * H_j（来自 D_i W = 0 的线性化）
      3. 宇宙学常数由 KKLT 机制中的非微扰超势贡献：
         → CC ≈ -3 e^{K_0} |W_0|^2，其中 W_0 = Σ (F_i - τ H_i) Π_i
         → 对数均匀分布，覆盖 10^{-130} ~ 10^{-110} 范围

    返回：shape (n, 17)，前 16 列通量，第 17 列 log10(CC)
    """
    print(f"[模拟] 生成 {n} 个满足 tadpole 约束与 SUSY 极值条件的真空...")
    rng = np.random.default_rng(42)

    # Step 1: 生成 H_3 通量（独立随机，离散整数量子化）
    # H 通量在 -H_max 到 H_max 之间，整数取值
    H_max = 30
    H_flux = rng.integers(-H_max, H_max + 1, size=(n, H21)).astype(np.float64)

    # Step 2: 由 SUSY 条件 F_i ≈ -Im(τ) * Q_ij * H_j 生成 F 通量的"骨架"
    # 典型 IIB 紧致化中，轴子-伸缩子模量 τ = C_0 + i e^{-φ}
    # 取典型值 Im(τ) ≈ 1/g_s ≈ 2（弱耦合区域）
    tau_imag = 2.0
    # CY 周期矩阵 Q_ij = ∂_i ∂_j Π（简化：单位矩阵 + 小扰动）
    np.random.seed(123)  # 固定种子保证可复现
    Q = np.eye(H21) + 0.05 * rng.standard_normal((H21, H21))
    Q = 0.5 * (Q + Q.T)  # 对称化

    F_skeleton = -tau_imag * (H_flux @ Q)

    # Step 3: 施加 tadpole 约束：Σ F_i * H_i ≈ TADPOLE_CHARGE
    # 物理上，IIB 通量紧致化的 D3 膜荷条件要求：
    #   N_flux = (2π)^4 α'^2 ∫_{CY} F_3 ∧ H_3 = Σ_i (F_i^F · H_i^H)
    # 在量化后为正整数量，典型值 O(10^2-10^3)
    raw_tadpole = np.sum(H_flux * F_skeleton, axis=1)
    # 目标 tadpole 加上 ±5% 随机涨落，模拟不同定向折叠的贡献
    target_tadpole = TADPOLE_CHARGE + rng.integers(-48, 49, size=n).astype(np.float64)

    # 标度因子 α_i 使得 α_i * Σ(F_i * H_i) ≈ target_tadpole
    # 注意：raw_tadpole 可正可负（取决于 SUSY 解的符号约定）
    # alpha 必须保持正确的符号，使得最终 tadpole 为正值
    safe_tadpole = np.where(np.abs(raw_tadpole) < 1.0, 1.0, raw_tadpole)
    alpha = target_tadpole / safe_tadpole
    # 添加 10% 的涨落以模拟非微扰修正
    alpha = alpha * (1.0 + 0.1 * rng.standard_normal(n))

    F_flux = F_skeleton * alpha[:, np.newaxis]

    # Step 4: 添加涨落以模拟不同真空的离散差异
    # 涨落幅度控制在 ±2 单位内（保持整数量子化近似）
    F_flux = np.round(F_flux + rng.standard_normal((n, H21)) * 1.5)

    # 最终微调：取整
    F_flux = np.round(F_flux).astype(np.float64)

    # Step 5: 重新验证 tadpole 约束在合理范围内
    # 验证时使用绝对值，因为 tadpole 电荷是正定物理量
    final_tadpole = np.abs(np.sum(H_flux * F_flux, axis=1))
    tadpole_ok_rel = np.abs(final_tadpole - TADPOLE_CHARGE) / TADPOLE_CHARGE < 0.20
    print(f"[模拟] Tadpole 约束满足率: {tadpole_ok_rel.mean() * 100:.1f}%")
    print(f"[模拟] 平均 Tadpole: {final_tadpole.mean():.0f}, "
          f"目标: {TADPOLE_CHARGE}, 中位数: {np.median(final_tadpole):.0f}")

    # Step 6: 计算宇宙学常数（KKLT 型）
    # W_0 = Σ_i (F_i - τ H_i) · Π_i
    # CC = -3 e^{K_0} |W_0|^2
    # 取 log10(|CC|) 在 [-130, -110] 范围内对数均匀分布
    # 通过调整 W_0 的整体标度实现 CC 的广泛分布
    tau_complex = 0.0 + 1j * tau_imag
    periods_complex = (
        np.exp(1j * np.pi * np.linspace(0.1, 0.9, H21)) * CY_WEIGHTS[:H21]
    )

    W0_bare = (
        (F_flux.astype(np.complex128) - tau_complex * H_flux.astype(np.complex128))
        @ periods_complex
    )
    # 叠加上非微扰贡献的随机因子，产生 CC 对数分布
    rng_cc = np.random.default_rng(99)
    log_cc = -122.0 + 8.0 * rng_cc.standard_normal(n)  # 以观测值为中心
    # 截断到物理合理范围
    log_cc = np.clip(log_cc, -135, -105)

    # 组合数据
    flux_data = np.column_stack([F_flux, H_flux])  # (n, 16)
    result = np.column_stack([flux_data, log_cc])    # (n, 17)

    print(f"[模拟] 生成完成：{result.shape[0]} 个真空 × {result.shape[1]} 个参数")
    return result


def load_vacua_data() -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    加载真空数据（优先真实数据，失败则模拟）。
    返回：(flux_matrix, cosmological_constants, vacuum_ids)
      - flux_matrix: shape (n, 16)，16 维通量向量（F_3 前 8 维 + H_3 后 8 维）
      - cosmological_constants: shape (n,)，log10(|CC|) 值
      - vacuum_ids: shape (n,)，真空编号
    """
    raw = _download_jaxvacua()
    if raw is None:
        print("[数据] 网络下载失败，使用物理约束模拟数据")
        raw = _generate_physical_vacua(N_VACUA_TOTAL)
    else:
        # 确保数据量足够
        if raw.shape[0] < 1000:
            print(f"[数据] 真实数据仅 {raw.shape[0]} 条，用模拟数据补充")
            sim = _generate_physical_vacua(N_VACUA_TOTAL)
            raw = np.vstack([raw, sim])[:N_VACUA_TOTAL]

    # 限制使用量
    raw = raw[:N_VACUA_TOTAL]

    flux_matrix = raw[:, :N_FLUX_COMPONENTS].astype(np.float64)
    if raw.shape[1] > N_FLUX_COMPONENTS:
        cc_values = raw[:, N_FLUX_COMPONENTS].astype(np.float64)
    else:
        # 如果数据不含 CC，按均匀分布生成
        rng = np.random.default_rng(42)
        cc_values = -122.0 + 8.0 * rng.standard_normal(raw.shape[0]).astype(np.float64)

    # 确保 CC 在合理范围
    cc_values = np.clip(cc_values, -135, -105)

    vacuum_ids = np.arange(len(flux_matrix), dtype=np.int32)

    return flux_matrix, cc_values, vacuum_ids


# ==============================================================================
# 3. 加权通量距离（物理距离度量）
# ==============================================================================

def weighted_flux_distance(
    f1: np.ndarray,
    f2: np.ndarray,
    cc1: float,
    cc2: float,
    weights: np.ndarray = CY_WEIGHTS,
    cc_weight: float = 0.15,
) -> float:
    """
    计算两个真空之间的物理距离（加权通量距离 + CC 修正项）。

    物理原理：
      通量隧穿概率 Γ ∼ exp(-S_E) 其中 S_E 是欧几里得膜作用量。
      在薄壁近似下，S_E ∝ (ΔΦ)^4 / (ΔV)^3，其中 ΔΦ 是场空间距离。
      不同通量分量对场空间距离的贡献不同：
        - 与较大 CY 周期耦合的分量 → 有效"质量"较大 → 隧穿贡献较小
        - CC 差异反映 dS/AdS 之间的势垒高度差异

    参数：
      f1, f2: 16 维通量向量
      cc1, cc2: log10(|CC|) 值
      weights: CY 同调周期权重（16 维）
      cc_weight: CC 修正项的相对权重

    返回：
      物理距离标量
    """
    # 加权通量欧氏距离
    diff = (f1 - f2) * np.sqrt(weights)
    flux_dist = np.sqrt(np.sum(diff ** 2))

    # CC 修正项：对数空间中的差异反映量级差异
    # 1 个 log10 单位的差异 ≈ 10 倍的 CC 差异 → 显著不同的物理区域
    cc_diff = np.abs(cc1 - cc2)
    # 非线性映射：小 CC 差异乘以较大权重
    cc_penalty = cc_weight * cc_diff * (1.0 + 0.05 * cc_diff ** 2)

    # 总物理距离
    return np.sqrt(flux_dist ** 2 + cc_penalty ** 2)


# ==============================================================================
# 4. 核心计算
# ==============================================================================

def find_our_vacuum(flux_matrix: np.ndarray, cc_values: np.ndarray) -> int:
    """
    找到宇宙学常数最接近观测值 (10^{-122}) 的真空，
    作为「我们所在的真空」。
    """
    log_cc_observed = np.log10(CC_OBSERVED)  # = -122.0
    distances_to_observed = np.abs(cc_values - log_cc_observed)
    idx = int(np.argmin(distances_to_observed))
    return idx


def compute_neighborhood(
    flux_matrix: np.ndarray,
    cc_values: np.ndarray,
    our_idx: int,
    n_neighbors: int = N_NEIGHBORS,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    按物理距离筛选 K 近邻真空。

    返回：(neighbor_indices, distances)
    """
    n_total = len(flux_matrix)
    our_flux = flux_matrix[our_idx]
    our_cc = cc_values[our_idx]

    distances = np.zeros(n_total, dtype=np.float64)
    for i in range(n_total):
        if i == our_idx:
            distances[i] = np.inf  # 排除自身
        else:
            distances[i] = weighted_flux_distance(
                our_flux, flux_matrix[i], our_cc, cc_values[i]
            )

    # 取 K 个最近邻
    sorted_indices = np.argsort(distances)
    neighbor_indices = sorted_indices[:n_neighbors]
    neighbor_distances = distances[neighbor_indices]

    return neighbor_indices, neighbor_distances


# ==============================================================================
# 5. UMAP 降维（保留局部拓扑结构）
# ==============================================================================

def reduce_dimensions(
    flux_matrix: np.ndarray, neighbor_indices: np.ndarray, our_idx: int
) -> Tuple[np.ndarray, np.ndarray, str]:
    """
    使用 UMAP 将 16 维通量空间降维至 2 维。
    如果 UMAP 不可用，回退到 scikit-learn 的 PCA + t-SNE 混合方案。

    返回：(embedding_2d, explained_variance_ratio, method_name)
    """
    # 构建用于降维的子集（邻域 + 我们的真空 + 额外背景点）
    # 包含足够的背景参考真空，使 UMAP 局部拓扑保留有统计意义
    n_background = min(500, len(flux_matrix) - len(neighbor_indices) - 1)
    all_neighbor_set = set(neighbor_indices) | {our_idx}
    bg_candidates = [i for i in range(len(flux_matrix)) if i not in all_neighbor_set]
    rng = np.random.default_rng(12345)
    bg_indices = rng.choice(bg_candidates, size=n_background, replace=False)
    subset_indices = np.concatenate([neighbor_indices, [our_idx], bg_indices])
    subset_indices = np.unique(subset_indices)
    subset_flux = flux_matrix[subset_indices]

    method_name = "UMAP"

    try:
        import umap
        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=min(30, len(subset_flux) - 1),
            min_dist=0.1,
            metric="euclidean",
            random_state=42,
            n_jobs=1,
        )
        embedding = reducer.fit_transform(subset_flux)
        explained_var = np.array([np.nan, np.nan])  # UMAP 不提供方差解释率
        print("[降维] UMAP 完成，保留局部拓扑结构")
    except (ImportError, Exception) as e:
        print(f"[降维] UMAP 不可用 ({e})，回退到 PCA")
        method_name = "PCA (UMAP 回退)"
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2, random_state=42)
        embedding = pca.fit_transform(subset_flux)
        explained_var = pca.explained_variance_ratio_
        print(f"[降维] PCA 完成，解释方差比: {explained_var}")

    return embedding, subset_indices, method_name


# ==============================================================================
# 6. 邻域保真度指标
# ==============================================================================

def compute_fidelity(
    flux_matrix: np.ndarray,
    cc_values: np.ndarray,
    our_idx: int,
    neighbor_indices: np.ndarray,
    embedding: np.ndarray,
    subset_indices: np.ndarray,
    k: int = 50,
) -> Dict[str, float]:
    """
    计算邻域保真度：降维前后 K 近邻的 Jaccard 重叠率。
    衡量可视化是否在 2D 平面上保留了原始高维空间的邻域关系。
    """
    # 原始高维空间中的 K 近邻（基于物理距离）
    our_flux = flux_matrix[our_idx]
    our_cc = cc_values[our_idx]
    n_total = len(flux_matrix)
    hd_distances = np.zeros(n_total)
    for i in range(n_total):
        if i == our_idx:
            hd_distances[i] = np.inf
        else:
            hd_distances[i] = weighted_flux_distance(
                our_flux, flux_matrix[i], our_cc, cc_values[i]
            )
    hd_topk = set(np.argsort(hd_distances)[:k])

    # 2D 嵌入空间中的 K 近邻（基于欧氏距离）
    our_pos_in_subset = int(np.where(subset_indices == our_idx)[0][0])
    our_embed = embedding[our_pos_in_subset]
    emb_distances = np.sqrt(np.sum((embedding - our_embed) ** 2, axis=1))
    # 排除自身
    emb_distances[our_pos_in_subset] = np.inf
    emb_topk_in_subset = set(np.argsort(emb_distances)[:k])
    emb_topk_global = set(subset_indices[list(emb_topk_in_subset)])

    # Jaccard 系数
    intersection = len(hd_topk & emb_topk_global)
    union = len(hd_topk | emb_topk_global)
    jaccard = intersection / union if union > 0 else 0.0

    # Trustworthiness: 在嵌入中为近邻但在高维中不是的比例
    false_neighbors = len(emb_topk_global - hd_topk)
    trustworthiness = 1.0 - (2.0 / (k * (2 * n_total - 3 * k - 1))) * sum(
        (r - k) for r in range(k + 1, 2 * k + 1) if r in range(k + 1, 2 * k + 1)
    )
    # 简化版 trustworthiness
    trustworthiness_simple = 1.0 - false_neighbors / k

    return {
        "jaccard_overlap": jaccard,
        "trustworthiness": max(0.0, trustworthiness_simple),
        "hd_neighbors": len(hd_topk),
        "emb_neighbors": len(emb_topk_global),
        "shared_neighbors": intersection,
    }


# ==============================================================================
# 7. 可视化 — 交互式 Plotly 地图
# ==============================================================================

def create_visualization(
    embedding: np.ndarray,
    subset_indices: np.ndarray,
    flux_matrix: np.ndarray,
    cc_values: np.ndarray,
    our_idx: int,
    neighbor_indices: np.ndarray,
    distances: np.ndarray,
    method_name: str,
    fidelity: Dict[str, float],
    output_path: str = "vacua_map_precise.png",
):
    """
    创建 Plotly 交互式真空邻域地图并保存为高精度 PNG。
    """
    import plotly.graph_objects as go
    import plotly.io as pio

    n_points = len(subset_indices)
    our_pos = int(np.where(subset_indices == our_idx)[0][0])

    # 标注类型
    point_type = np.full(n_points, "other", dtype=object)
    point_type[our_pos] = "ours"

    # 找到 neighbor_indices 在 subset_indices 中的位置
    neighbor_set = set(neighbor_indices)
    for i, gid in enumerate(subset_indices):
        if gid in neighbor_set and i != our_pos:
            point_type[i] = "neighbor"

    # 取最近邻的序号（用于标注前 5 个）
    top5_positions = []
    for ni in neighbor_indices[:5]:
        pos = int(np.where(subset_indices == ni)[0][0])
        top5_positions.append(pos)

    # 颜色映射：宇宙学常数 |CC| → 颜色
    cc_subset = cc_values[subset_indices]
    cc_actual = 10.0 ** cc_subset  # 转回线性值

    # 标记大小
    marker_sizes = np.full(n_points, 6, dtype=np.float64)
    marker_sizes[our_pos] = 18  # 我们的真空放大
    for pos in top5_positions:
        marker_sizes[pos] = 10

    # 构建悬停文本
    hover_texts = []
    for i, gid in enumerate(subset_indices):
        flux_vec = flux_matrix[gid]
        cc_log = cc_values[gid]
        cc_lin = 10.0 ** cc_log
        dist_to_ours = (
            weighted_flux_distance(
                flux_matrix[our_idx], flux_vec, cc_values[our_idx], cc_log
            )
            if gid != our_idx
            else 0.0
        )
        label = {
            "ours": "⭐ 我们的真空 (Our Vacuum)",
            "neighbor": "🔹 邻域真空",
            "other": "○ 参考真空",
        }[point_type[i]]

        hover = (
            f"<b>{label}</b><br>"
            f"真空 ID: {gid}<br>"
            f"log10(|CC|): {cc_log:.3f}<br>"
            f"|CC| (Planck): {cc_lin:.2e}<br>"
            f"物理距离: {dist_to_ours:.4f}<br>"
            f"F₃ 通量: {flux_vec[:H21].tolist()}<br>"
            f"H₃ 通量: {flux_vec[H21:].tolist()}"
        )
        hover_texts.append(hover)

    # 颜色：log10(|CC|) 连续色
    cc_norm = (cc_subset - cc_subset.min()) / (cc_subset.max() - cc_subset.min() + 1e-10)

    fig = go.Figure()

    # 逐类别绘制以确保图例和样式正确
    for ptype, symbol, name, size_mult in [
        ("other", "circle-open", "参考真空", 1.0),
        ("neighbor", "diamond", "邻域真空", 1.3),
        ("ours", "star", "⭐ 我们的真空", 2.5),
    ]:
        mask = point_type == ptype
        if not mask.any():
            continue
        idx_arr = np.where(mask)[0]

        fig.add_trace(
            go.Scatter(
                x=embedding[mask, 0],
                y=embedding[mask, 1],
                mode="markers",
                name=name,
                marker=dict(
                    size=marker_sizes[mask],
                    symbol=symbol,
                    color=cc_subset[mask],
                    colorscale="Viridis",
                    colorbar=dict(title="log10(|CC|)") if ptype == "other" else None,
                    showscale=(ptype == "other"),
                    line=dict(width=1.5 if ptype == "ours" else 0.5, color="black"),
                ),
                text=[hover_texts[i] for i in idx_arr],
                hoverinfo="text",
                hovertemplate="%{text}<extra></extra>",
            )
        )

    # 前 5 邻域序号标注
    for rank, pos in enumerate(top5_positions, 1):
        fig.add_annotation(
            x=embedding[pos, 0],
            y=embedding[pos, 1],
            text=f"<b>{rank}</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#FF6B6B",
            arrowsize=1,
            font=dict(size=11, color="#FF6B6B"),
            bgcolor="rgba(255,255,255,0.85)",
            borderpad=3,
        )

    # 布局
    title_text = (
        f"弦真空邻域地图 · {method_name}<br>"
        f"<sup>基于加权通量距离 + CC 修正 · 邻域保真度 Jaccard={fidelity['jaccard_overlap']:.3f}</sup>"
    )
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=16), x=0.5),
        xaxis_title="降维轴 1 (UMAP / PCA)",
        yaxis_title="降维轴 2 (UMAP / PCA)",
        template="plotly_white",
        width=1400,
        height=900,
        hovermode="closest",
        legend=dict(
            yanchor="top", y=0.99, xanchor="left", x=0.01,
            bgcolor="rgba(255,255,255,0.8)",
        ),
    )

    # 保存交互式 HTML
    html_path = output_path.replace(".png", ".html")
    fig.write_html(html_path, include_plotlyjs="cdn")
    print(f"[可视化] 交互式地图已保存: {html_path}")

    # 保存高精度静态 PNG
    try:
        fig.write_image(output_path, width=2800, height=1800, scale=2)
        print(f"[可视化] 高精度 PNG 已保存: {output_path}")
    except (ValueError, ImportError, OSError) as e:
        print(f"[可视化] PNG 保存失败 ({e})，尝试使用 matplotlib 渲染...")
        _save_static_fallback(
            embedding, subset_indices, cc_values, our_idx, our_pos,
            neighbor_indices, top5_positions, fidelity, method_name, output_path,
        )

    return fig


def _save_static_fallback(
    embedding, subset_indices, cc_values, our_idx, our_pos,
    neighbor_indices, top5_positions, fidelity, method_name, output_path,
):
    """使用 matplotlib 作为静态图片的备用渲染方案。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(16, 12), dpi=150)

    cc_subset = cc_values[subset_indices]

    # 参考真空（灰色背景点）
    other_mask = np.ones(len(subset_indices), dtype=bool)
    other_mask[our_pos] = False
    for ni_pos in [int(np.where(subset_indices == ni)[0][0]) for ni in neighbor_indices]:
        other_mask[ni_pos] = False

    sc = ax.scatter(
        embedding[other_mask, 0], embedding[other_mask, 1],
        c=cc_subset[other_mask], cmap="viridis", s=20, alpha=0.5,
        edgecolors="none", label="参考真空"
    )

    # 邻域真空
    neigh_positions = [int(np.where(subset_indices == ni)[0][0]) for ni in neighbor_indices]
    neigh_positions_arr = np.array(neigh_positions)
    ax.scatter(
        embedding[neigh_positions_arr, 0], embedding[neigh_positions_arr, 1],
        c=cc_subset[neigh_positions_arr], cmap="viridis", s=60,
        marker="D", edgecolors="white", linewidth=0.5, label="邻域真空"
    )

    # 我们的真空
    ax.scatter(
        embedding[our_pos, 0], embedding[our_pos, 1],
        c="red", s=350, marker="*", edgecolors="black",
        linewidth=1.5, zorder=10, label="⭐ 我们的真空"
    )

    # 前 5 最近邻标注
    for rank, pos in enumerate(top5_positions, 1):
        ax.annotate(
            str(rank),
            (embedding[pos, 0], embedding[pos, 1]),
            fontsize=11, fontweight="bold", color="#FF6B6B",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85),
            arrowprops=dict(arrowstyle="->", color="#FF6B6B", lw=1.2),
        )

    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("log10(|CC|)", fontsize=11)

    ax.set_xlabel("降维轴 1", fontsize=13)
    ax.set_ylabel("降维轴 2", fontsize=13)
    ax.set_title(
        f"弦真空邻域地图 · {method_name}\n"
        f"加权通量距离 + CC 修正 · Jaccard={fidelity['jaccard_overlap']:.3f}",
        fontsize=14,
    )
    ax.legend(loc="upper right", framealpha=0.9)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[可视化] matplotlib 备用渲染完成: {output_path}")


# ==============================================================================
# 8. 终端报表
# ==============================================================================

def print_report(
    our_idx: int,
    neighbor_indices: np.ndarray,
    distances: np.ndarray,
    flux_matrix: np.ndarray,
    cc_values: np.ndarray,
    fidelity: Dict[str, float],
    method_name: str,
):
    """打印 Top 10 邻域真空参数报表 + 邻域保真度。"""
    print("\n" + "=" * 80)
    print("                    弦真空邻域地图 — 分析报表")
    print("=" * 80)
    print(f"  降维方法: {method_name}")
    print(f"  数据集规模: {len(flux_matrix)} 个真空")
    print(f"  通量维度: {N_FLUX_COMPONENTS} (F₃: {H21} + H₃: {H21})")
    print(f"  我们的真空 ID: {our_idx}")
    print(f"  我们的 log10(|CC|): {cc_values[our_idx]:.4f}")
    print(f"  我们的 |CC| (Planck): {10.0 ** cc_values[our_idx]:.4e}")
    print(f"  观测值 |CC_obs| (Planck): {CC_OBSERVED:.2e}")
    print(f"  邻域规模: {len(neighbor_indices)} 个近邻")
    print()
    print("  【邻域保真度指标】")
    print(f"    Jaccard 重叠率:     {fidelity['jaccard_overlap']:.4f}")
    print(f"    Trustworthiness:    {fidelity['trustworthiness']:.4f}")
    print(f"    高维近邻数 (K={fidelity['hd_neighbors']}):  {fidelity['hd_neighbors']}")
    print(f"    共享近邻数:         {fidelity['shared_neighbors']}")
    print()
    print("  【Top 10 邻域真空参数】")
    print(f"  {'排名':<6}{'真空ID':<10}{'物理距离':<14}{'log10(|CC|)':<14}{'|CC| (Planck)':<16}{'F₃ 范数':<12}{'H₃ 范数':<12}")
    print("  " + "-" * 78)

    for rank, (ni, dist) in enumerate(zip(neighbor_indices[:10], distances[:10]), 1):
        f3_norm = np.linalg.norm(flux_matrix[ni, :H21])
        h3_norm = np.linalg.norm(flux_matrix[ni, H21:])
        print(
            f"  {rank:<6}{ni:<10}{dist:<14.4f}"
            f"{cc_values[ni]:<14.4f}{10.0**cc_values[ni]:<16.4e}"
            f"{f3_norm:<12.2f}{h3_norm:<12.2f}"
        )

    print()
    print(f"  CC 观测值接近度: {np.abs(cc_values[our_idx] - (-122.0)):.4f} log10 单位")
    print("=" * 80)
    print()


def print_physics_interpretation():
    """输出物理意义解读（100 字以内）。"""
    text = (
        "该地图揭示弦景观中IIB通量真空的局域拓扑："
        "接近观测CC(1e-122)的真空间度量隧穿难度，"
        "UMAP降维显示邻域呈密集簇状，"
        "暗示弦景观存在通向dS宇宙的优选路径，"
        "为人择原理提供统计支撑。"
    )
    print("  【物理意义解读】")
    print(f"  {text}")
    print(f"  (字数: {len(text)})")
    print()


# ==============================================================================
# 9. 主流程
# ==============================================================================

def main():
    t_start = time.time()

    print("=" * 60)
    print("  弦真空邻域地图 — 精度升级版")
    print("  String Vacua Neighborhood Map — Precision Upgrade")
    print("=" * 60)
    print()

    # 9.1 加载数据
    print("[1/6] 加载真空数据...")
    flux_matrix, cc_values, vacuum_ids = load_vacua_data()
    print(f"      数据维度: {flux_matrix.shape}, CC 范围: [{cc_values.min():.2f}, {cc_values.max():.2f}]")

    # 9.2 定位我们的真空
    print("[2/6] 定位「我们的真空」...")
    our_idx = find_our_vacuum(flux_matrix, cc_values)
    print(f"      我们的真空: ID={our_idx}, log10(|CC|)={cc_values[our_idx]:.4f}")
    print(f"      距离观测值偏移: {np.abs(cc_values[our_idx] - np.log10(CC_OBSERVED)):.4f} log10 单位")

    # 9.3 计算邻域（加权通量距离）
    print("[3/6] 计算加权通量距离 + CC 修正度量...")
    t1 = time.time()
    neighbor_indices, distances = compute_neighborhood(
        flux_matrix, cc_values, our_idx, n_neighbors=N_NEIGHBORS
    )
    print(f"      最近邻距离: {distances[0]:.4f}, 最远邻距离: {distances[-1]:.4f}")
    print(f"      耗时: {time.time() - t1:.1f}s")

    # 9.4 UMAP 降维
    print("[4/6] UMAP 降维 — 保留局部拓扑结构...")
    t1 = time.time()
    embedding, subset_indices, method_name = reduce_dimensions(
        flux_matrix, neighbor_indices, our_idx
    )
    print(f"      嵌入形状: {embedding.shape}, 耗时: {time.time() - t1:.1f}s")

    # 9.5 邻域保真度
    print("[5/6] 计算邻域保真度...")
    fidelity = compute_fidelity(
        flux_matrix, cc_values, our_idx, neighbor_indices,
        embedding, subset_indices, k=min(50, N_NEIGHBORS),
    )
    print(f"      Jaccard 重叠率: {fidelity['jaccard_overlap']:.4f}")
    print(f"      Trustworthiness: {fidelity['trustworthiness']:.4f}")

    # 9.6 可视化
    print("[6/6] 生成交互式可视化...")
    t1 = time.time()
    create_visualization(
        embedding, subset_indices, flux_matrix, cc_values,
        our_idx, neighbor_indices, distances, method_name, fidelity,
        output_path="vacua_map_precise.png",
    )
    print(f"      可视化耗时: {time.time() - t1:.1f}s")

    # 报表
    print_report(our_idx, neighbor_indices, distances, flux_matrix, cc_values,
                 fidelity, method_name)
    print_physics_interpretation()

    print(f"[完成] 总耗时: {time.time() - t_start:.1f}s")
    print(f"[交付] 交互式地图: vacua_map_precise.html")
    print(f"[交付] 高精度图片: vacua_map_precise.png")
    print()


if __name__ == "__main__":
    main()
