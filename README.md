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

## 現在の運用フロー
1. `add` コマンドで当日の作業内容を記録します。
2. `generate` コマンドで当日分の Markdown 日報を生成します。
3. push をきっかけに GitHub Actions が実行されます。
4. Actions 内で `python src/main.py generate` を実行し、生成した日報を Dropbox にアップロードします。
5. Dropbox 上の journal ファイルを Logseq から参照します。

## 現在の入出力
### 入力
- `data/logs/YYYY-MM-DD.json`
- `add` コマンドで追記されます

### 出力
- `reports/YYYY_MM_DD.md`
- GitHub Actions ではこのファイルを Dropbox にアップロードします
- Dropbox 上では `target-path` で指定した journal パスに保存されます

## 日報の追加例
```bash
py src/main.py add --section done --project api "認証処理を修正"
py src/main.py add --section issue --project api "テスト不足"
py src/main.py add --section next --project api "認証テストを追加"
py src/main.py add --section memo --project daily-report-system "Dropbox連携を確認"
```

## 現在の実行方法（ローカル）

1. `add` コマンドで作業内容を記録
2. `generate` コマンドで日報を生成

```bash
py src/main.py add --section done --project api "認証処理を修正"
py src/main.py generate
```