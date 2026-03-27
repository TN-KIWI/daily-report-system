# Git Workflow

## Branch Strategy
- main: 本番
- dev: 開発
- feature/*: 機能単位

## Flow
1. featureブランチ作成
2. 実装
3. devにマージ
4. mainに反映

## Commit Rules
- feat: 新機能
- fix: 修正
- refactor: リファクタ
- remove: 削除

## Example
feat: add git log reader
fix: timezone handling bug

## Staging Rule

- コミットは自動で行わない
- ステージングは以下のコマンドを必ず使用する

```bash
cmd /c "chcp 65001 >NUL & git --no-pager diff --staged > staged_diff.txt"
```