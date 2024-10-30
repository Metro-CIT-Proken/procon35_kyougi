# ビームサーチソルバー

## ソースコードについて

- AnswerTree : 解答を保存しておくデータ構造
- BeamEvaluator : ビームサーチ用の評価関数
- BeamSolver : ビームサーチをする
- BeamSolver_chokudai : chokudaiサーチをする
- LineCountSolver : 行ごとに各値の数をゴール盤面に揃える
- SimpleSolver : 左上から1セルずつ直す
- SpinMutex : 排他処理用のクラス（スレッド並列ビームサーチで使用しています）
- VDivideSolver : 問題を縦方向に分割してビームサーチに渡すソルバ
- bitboard : ビット演算を用いた高速な盤面
- board : 盤面
- pext : 抜き型処理を高速にできるpext命令のx64/ARM両対応版
- main : ビームサーチで問題を解く
- main_SimpleSolver : SimpleSolverで問題を解く
