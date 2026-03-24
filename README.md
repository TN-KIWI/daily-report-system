# daily-report-system

Pythonで日報を扱うCLIベースの最小プロジェクトです。
今回は初期構造のみを作成し、実処理は今後追加していきます。

## 概要
- `init`: 初期化の入口コマンド
- `add`: 日報エントリ追加の入口コマンド
- `generate`: レポート生成の入口コマンド

## 使い方
### Windows（pyランチャー）

```bash
py src/main.py --help
py src/main.py init
py src/main.py add --section done --project SampleProject "タスクAを完了"
py src/main.py generate
```

### macOS / Linux（python3）

```bash
python3 src/main.py --help
python3 src/main.py init
python3 src/main.py add --section done --project SampleProject "タスクAを完了"
python3 src/main.py generate
```

## ディレクトリ
- `src/`: CLI本体とモジュール
- `data/logs/`: 生ログ保存先
- `reports/`: 生成レポート保存先
- `tests/`: テストコード
