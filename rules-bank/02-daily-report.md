# Daily Report

## Structure
日報は以下の4セクションで構成する

- done: 今日やったこと
- issue: 課題
- next: 次にやること
- memo: メモ

## Data Sources
日報は2つの情報源を統合する

1. 手動入力（add）
2. Gitログ（git-log）

## Rules
- Gitログは「事実」として扱う
- 手動入力は「補完」として扱う
- generate は両方を統合する

## Commands
- add
  py src/main.py add --section <done|issue|next|memo> --project <name> "<text>"

- generate
  py src/main.py generate

- git-log
  py src/main.py git-log --repo <path>

## Constraints
- formatterの構造は変更しない
- データ形式は変更しない
- time_utils を必ず使う