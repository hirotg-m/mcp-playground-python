# ローカル MCP サーバーを実行し、Amazon Q Developer から使う手順

このドキュメントでは、このリポジトリの `server.py` をローカルで動かし、Amazon Q Developer から `get_price_list` ツールを呼び出すまでを説明します。

## 1. 前提

- Python 3.12
- VS Code
- Amazon Q Developer 拡張機能がインストール済み

## 2. セットアップ

ワークスペースのルート（`mcp-playground-python`）で実行します。

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` には `mcp>=1.0.0` が定義されています。

## 3. サーバー単体での起動確認

まずは MCP サーバー自体が起動できることを確認します。

```bash
source .venv/bin/activate
python3.12 server.py
```

エラーが出なければ起動成功です（終了するときは `Ctrl + C`）。

## 4. Amazon Q Developer から使えるように登録する

Amazon Q Developer は `~/.aws/amazonq/mcp.json` を読み込んで MCP サーバーを認識します。

```bash
mkdir -p ~/.aws/amazonq
```

`~/.aws/amazonq/mcp.json` を以下の内容で作成します（パスは環境に合わせて変更してください）。

```json
{
  "mcpServers": {
    "price-list-server": {
      "command": "/絶対パス/mcp-playground-python/.venv/bin/python",
      "args": [
        "/絶対パス/mcp-playground-python/server.py"
      ]
    }
  }
}
```

> **注意:** Claude Code 用の `.mcp.json` と異なり、`${CLAUDE_PROJECT_DIR}` などの変数は使えません。絶対パスで指定してください。

現在のディレクトリの絶対パスは次のコマンドで確認できます。

```bash
pwd
```

## 5. IDE を再起動して認識させる

設定ファイルを作成したあと、VS Code（または Amazon Q Developer プラグイン）を再起動します。

## 6. Amazon Q Developer で呼び出す

Amazon Q Developer のチャットで、次のように依頼します。

- 「`get_price_list` を呼んで価格一覧を表示して」
- 「price-list-server のツールで品物一覧を取得して」

期待される結果（例）:

| 品物 | 価格 |
|------|------|
| りんご | 150円 |
| みかん | 100円 |
| バナナ | 80円 |

## 7. うまくいかないとき

- `.venv` が未作成 / 未有効化
  - `python3.12 -m venv .venv` と `source .venv/bin/activate` を再実行
- 依存未インストール
  - `pip install -r requirements.txt`
- `mcp.json` のパスが誤っている
  - `command` が `.venv/bin/python` の絶対パスを指しているか確認
- 登録後にツールが認識されない
  - VS Code の再読み込み（Developer: Reload Window）を実施

---

最小確認だけをする場合は、次の2ステップで十分です。

1. `python3.12 server.py` が起動する
2. Amazon Q Developer のチャットから `get_price_list` を呼び出せる
