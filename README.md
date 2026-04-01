# daily-report-system

Pythonで日報を扱うCLIベースのシンプルなツールです。
手動入力とGitログを統合して、日報を生成します。

---

## 概要

* `add`: 日報エントリを手動追加
* `generate`: 日報を生成
* `git-log`: 当日のGitコミットを確認（デバッグ用）

---

## 特徴

* 手動入力とGitログを統合
* 複数リポジトリ対応
* シンプルなCLI設計
* ローカル実行前提（自動化なし）

---

## セットアップ

特別なセットアップは不要です。

```bash
py src/main.py --help
```

---

## 使い方

### 1. 作業内容を記録

```bash
py src/main.py add --section done --project api "認証処理を修正"
py src/main.py add --section issue --project api "テスト不足"
py src/main.py add --section next --project api "認証テストを追加"
py src/main.py add --section memo --project daily-report-system "Git統合を確認"
```

---

### 2. 日報を生成

```bash
py src/main.py generate
```

---

### 3. Gitログ確認（任意）

```bash
py src/main.py git-log
```

---

## Gitログの統合

日報にはGitのコミットメッセージが自動で含まれます。

* 当日のコミットのみ取得
* `done` セクションに追加される
* プロジェクト名はハッシュタグで付与される

例:

```md
- #api feat: add login
- #daily-report-system fix: timezone bug
```

---

## リポジトリ設定

対象のGitリポジトリは `config/repos.json` で管理します。

### 例

```json
{
  "repos": [
    ".",
    "C:/dev/api",
    "C:/dev/project-a"
  ]
}
```

* `"."` はこのプロジェクト
* 複数リポジトリをまとめて日報に反映可能

---

## 日報の構造

日報は以下のセクションで構成されます。

* `done`: 今日やったこと（Gitログ + 手動入力）
* `issue`: 課題
* `next`: 次にやること
* `memo`: メモ

---

## ディレクトリ構成

* `src/`: CLI本体
* `data/logs/`: 手動入力ログ
* `reports/`: 生成された日報
* `config/`: 設定ファイル

---

## ルール

* Gitログは「事実」として扱う
* 手動入力は「補完」として扱う
* Gitログと同じ内容は手動で書かない
* シンプルな構成を保つ（過剰な抽象化をしない）

---

## 開発方針

* 小さく作る
* ローカルで動かす
* 必要になってから拡張する

---

## 今後の拡張案

* repo設定の柔軟化
* 重複防止（commit hashベース）
* 出力フォーマットの拡張

---

## ライセンス

MIT
