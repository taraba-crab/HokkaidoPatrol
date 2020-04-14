# 概要: 北海道の観光都市を効率的に巡回するルートを求めるプログラムの作成

## 巡回セールスマン問題

函館→小樽→札幌→旭川→室蘭→函館

のように、ある地点を出発してから他の観光都市を一度だけ訪問し、元の地点に戻るルートの最短距離を求めるプログラムを作成しました。

巡回ルートの最短距離を求める問題は「**巡回セールスマン問題**」と呼ばれています。

巡回セールスマン問題とは、セールスマンが各町を一度だけ訪問するとしたら、どういう順番で巡回したら最短距離になるのかを求める問題です。最適なルートを決める法則のようなものは発見されておらず、愚直に解こうとすると膨大な時間がかかります。

現実世界では、**ヤマト運輸**や**佐川急便**が**燃料費削減、配達時間短縮**などの課題として毎日この問題と向き合っています。

この問題の**準**最適解を**遺伝的アルゴリズム**で求めました。

## 遺伝的アルゴリズム

遺伝的アルゴリズムとは、優秀なパラメータを持つデータを確率的に混ぜ合わせ(**交叉**)たり、ランダムに**変異**をさせたりを繰り返して、徐々にさらに優秀なデータにしていくアルゴリズムです。進化論における**自然選択説**の、情報科学への応用です。

巡回セールスマン問題における「優秀なデータ」とは、巡回ルートの距離が短いルートのことです。

また、この問題における「データの混ぜ合わせ(交叉)」とは、二つのデータ間でルートの部分区間を交換することです。参考(http://ono-t.d.dooo.jp/GA/GA-order.html)

交叉には「**部分写像交叉**」という方式を採用しました。

この方式について解説します。

はじめに、ルートは{札幌, 旭川, 函館, 釧路, 北見, 小樽, 稚内, 富良野}のような配列で表すとします。

交叉には親となる二つのルートが必要です。

- 親１ {札幌, 旭川, 函館, 釧路, 北見, 稚内, 小樽, 富良野}
- 親２ {稚内, 北見, 小樽, 函館, 釧路, 旭川, 札幌, 富良野}

ルートにおける部分写像交叉では、親の順番をできるだけ多く受け継ぐことを目的として、部分区間を交換します。

以下、交叉の流れです。

ランダムに区間を選択します。

- 親１ {札幌, 旭川,| 函館, 釧路, 北見, 稚内,| 小樽, 富良野}
- 親２ {稚内, 北見,| 小樽, 函館, 釧路, 旭川,| 札幌, 富良野}

|(縦棒)で区間を表現しました。はさまれている区間を交換し、結果を子とします。

- 子１ {札幌, 旭川,| **小樽**, **函館**, **釧路**, **旭川**,| 小樽, 富良野}
- 子２ {稚内, 北見,| **函館**, **釧路**, **北見**, **稚内**,| 札幌, 富良野}

このままではルートに同じ市町村が含まれるので、被っている市町村を区間外から見つけ、交換します。

ここでは子1が**旭川**と**小樽**、子2が**稚内**と**北見**でかぶっていますので要素番号が小さい順に交換します。

- 子１ {札幌,   **稚内**,| 小樽, 函館, 釧路, 旭川,| **北見**, 富良野}
- 子２ {**旭川**, **小樽**,| 函館, 釧路, 北見, 稚内,| 札幌,   富良野}

必ずしも交叉がより良い結果を生むわけではありません。

結果的に良くなった子を取得し、再び親として採用します。これを何世代か繰り返します。

遺伝的アルゴリズムは、このように確率的な変化に依存するので大抵は"準最適"な結果が得られます。

また、親の集団(**母集団**)の要素数は多いほど交叉のバリエーションが増えますので、適宜母集団の要素数も設定します。

## 開発工程

### 各市町村間の距離の測定

「北の道ナビ」というサイトで北海道の208の各2市町村間の距離を調べ、結果をDBに保存。(21528通り)

スクレイピングすることで実現しました。

### 遺伝的アルゴリズムの実装

- 入力:
  - ルートを調べたい市町村の配列 (例: {札幌, 旭川, 函館, 釧路, 北見, 小樽, 稚内, 富良野})

- 出力:
  - 巡回ルートを以下条件の遺伝的アルゴリズムで求め、ルートと距離を出力。例の結果は以下のようになりました。
  - 条件
    - 世代数: 10000
    - 母集団の要素数: 50
  - 結果
    - 富良野 -> 札幌 -> 小樽 -> 函館 -> 釧路 -> 北見 -> 稚内 -> 旭川 (-> 富良野): 1731.5 km
