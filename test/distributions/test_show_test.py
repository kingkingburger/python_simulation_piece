import numpy as np
import matplotlib.pyplot as plt

# 시각화를 위한 샘플 데이터 개수 설정
# 시스템 설계 시, 실제 데이터의 양과 트래픽을 예측하여 충분한 샘플로 테스트하는 것이 중요합니다.
NUM_SAMPLES = 10000

# 서브플롯(Subplot)을 생성하여 여러 분포를 한 번에 비교할 수 있도록 합니다.
# 이는 코드의 유지보수성과 가독성을 높여줍니다.
fig, axes = plt.subplots(3, 2, figsize=(12, 12))
fig.suptitle('Inter-arrival Time Probability Distributions (도착 간격 확률 분포)', fontsize=16)
axes = axes.flatten() # 2D 배열을 1D로 만들어 순차적으로 접근하기 쉽게 합니다.

# --- 1. Constant (상수) ---
# 모든 값이 하나의 상수로 고정되는 경우입니다.
value = 10
# 모든 샘플을 동일한 값으로 생성합니다.
samples_const = np.full(NUM_SAMPLES, value)
axes[0].hist(samples_const, bins=1, edgecolor='black')
axes[0].set_title(f'Constant(value={value})')
axes[0].set_xlabel('Time Interval (sec)')
axes[0].set_ylabel('Frequency')


# --- 2. Normal (정규 분포) ---
# 평균(mean) 주변에 데이터가 집중되는 종 모양 분포입니다.
mean, stddev = 10, 2
samples_normal = np.random.normal(loc=mean, scale=stddev, size=NUM_SAMPLES)
axes[1].hist(samples_normal, bins=50, edgecolor='black', color='skyblue')
axes[1].set_title(f'Normal(mean={mean}, stddev={stddev})')
axes[1].set_xlabel('Time Interval (sec)')
axes[1].set_ylabel('Frequency')


# --- 3. Uniform (균등 분포) ---
# 특정 범위(min, max) 내의 모든 값이 발생할 확률이 동일한 분포입니다.
min_val, max_val = 5, 15
samples_uniform = np.random.uniform(low=min_val, high=max_val, size=NUM_SAMPLES)
axes[2].hist(samples_uniform, bins=50, edgecolor='black', color='lightgreen')
axes[2].set_title(f'Uniform(min={min_val}, max={max_val})')
axes[2].set_xlabel('Time Interval (sec)')
axes[2].set_ylabel('Frequency')


# --- 4. Exponential (지수 분포) ---
# 어떤 사건이 발생할 때까지 걸리는 시간을 모델링할 때 주로 사용됩니다. (예: 콜센터에 다음 전화가 올 때까지의 시간)
# 작은 값들이 발생할 확률이 높고, 값이 커질수록 확률이 기하급수적으로 줄어듭니다.
exp_mean = 10
samples_exp = np.random.exponential(scale=exp_mean, size=NUM_SAMPLES)
axes[3].hist(samples_exp, bins=50, edgecolor='black', color='salmon')
axes[3].set_title(f'Exponential(mean={exp_mean})')
axes[3].set_xlabel('Time Interval (sec)')
axes[3].set_ylabel('Frequency')


# --- 5. Triangular (삼각 분포) ---
# 최소(min), 최빈(mode), 최대(max) 값을 알 때 사용하는 분포입니다.
# 최빈값(mode)에서 가장 높은 확률을 가지며 양쪽으로 갈수록 확률이 선형적으로 감소합니다.
tri_min, tri_mode, tri_max = 5, 8, 12
samples_tri = np.random.triangular(left=tri_min, mode=tri_mode, right=tri_max, size=NUM_SAMPLES)
axes[4].hist(samples_tri, bins=50, edgecolor='black', color='gold')
axes[4].set_title(f'Triangular(min={tri_min}, mode={tri_mode}, max={tri_max})')
axes[4].set_xlabel('Time Interval (sec)')
axes[4].set_ylabel('Frequency')


# 마지막 빈 서브플롯은 보이지 않도록 처리합니다.
axes[5].set_visible(False)

# 레이아웃을 자동으로 조정하여 플롯들이 겹치지 않게 합니다.
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 최종 플롯을 화면에 표시합니다.
plt.show()