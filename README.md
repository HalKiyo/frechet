# frechet

荒川の年最大流量を対象に、極値分布 (Fréchet / Gumbel) の当てはめと順序統計量による確率流量 (Q100 など) の推定を行うスクリプト集です。

## ディレクトリ構成

```
frechet/
├── ranking.py      # OSSE アンサンブル全サンプルの順序統計量 (Weibull プロット位置) による確率流量
├── frechet_pdf.py  # 定常 Fréchet (GEV, c < 0) の当てはめと Q100
├── gumbel_pdf.py   # 定常 Gumbel の当てはめと Q100
└── evd_plot.py     # frechet_pdf.py / gumbel_pdf.py 共通のデータ読み込みと描画関数
```

## 実行方法

各スクリプトはカレントディレクトリからの相対パスでデータを読みます。

| スクリプト | 入力 | 出力 |
|---|---|---|
| `python ranking.py` | `./osse_gum_e3000_y120.bin` | 順位と流量の図 (画面表示)、T = 2〜500 年の確率流量を図中に表示 |
| `python frechet_pdf.py` | `../dat/arakawa_max_y120.bin` | 当てはめパラメータと Q100 を標準出力、散布図と PDF を画面表示 |
| `python gumbel_pdf.py` | `../dat/arakawa_max_y120.bin` | 同上 (Gumbel) |

依存パッケージは numpy, pandas, scipy, matplotlib です。
`frechet_pdf.py` と `gumbel_pdf.py` は同じディレクトリにある `evd_plot.py` を import するため、このディレクトリ内で実行してください。

## データ

### arakawa_max_y120.bin
- 荒川の 120 年分 (1980〜2099 年) の疑似観測年最大流量 (m³/s)。
- float32 で (年, 流量) の 2 列 × 120 行。
- CMIP6 ACCESS (オーストラリアのモデル) の気候シミュレーション出力を入力に、全球河川流下モデル **CaMa-Flood** (6 分解像度、約 10 km、日出力) で流量を計算し、各年の最大値を抽出したもの。

### osse_gum_e3000_y120.bin
- `arakawa_max_y120.bin` に非定常 Gumbel 分布を当てはめて生成した疑似観測データ。
- 1980〜2099 年の年最大流量 3,000 アンサンブル分、計 360,000 サンプル (float32、Fortran 順の 120 × 3000 行列)。
- 極端洪水の確率流量推定手法を評価する OSSE (Observing System Simulation Experiment) 用。

## スクリプトの概要

### ranking.py
360,000 サンプルすべてを降順に並べ、Weibull プロット位置 (超過確率 i / (n+1) = 1/T) に対応する順位の流量を各再現期間 T の確率流量とします。

### frechet_pdf.py
`scipy.stats.genextreme` で GEV 分布 (Fréchet 型なら c < 0) を当てはめ、99% 分位点を Q100 として出力します。

### gumbel_pdf.py
`scipy.stats.gumbel_r` で定常 Gumbel 分布を当てはめ、99% 分位点を Q100 として出力します。
