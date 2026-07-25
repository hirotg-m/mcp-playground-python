# ローカル MCP サーバーを実行し、Claude Code から使う手順

このドキュメントでは、このリポジトリの `server.py` をローカルで動かし、Claude Code から `get_price_list` ツールを呼び出すまでを説明します。

## 1. 前提

- Python 3.12
- Claude Code CLI（VS Code 拡張機能でも可）

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

## 4. Claude Code から使えるように登録する

Claude Code は、プロジェクト直下の `.mcp.json` を読み込んで MCP サーバーを自動的に認識します。このリポジトリには既に登録済みの設定が含まれています。

> **`.mcp.json` は Claude Code 専用の設定ファイルです。**
> JSON はコメントをサポートしていないためファイル内に記載していませんが、これは Claude Code がプロジェクトルートから自動検出する設定ファイルであり、他ツール（例: Copilot）向けの設定ではありません。Copilot 側の設定は別ファイル（VS Code の MCP 設定など）で管理してください。

`.mcp.json`:

```json
{
  "mcpServers": {
    "price-list-server": {
      "type": "stdio",
      "command": "${CLAUDE_PROJECT_DIR:-.}/.venv/bin/python",
      "args": [
        "${CLAUDE_PROJECT_DIR:-.}/server.py"
      ]
    }
  }
}
```

- `command` / `args` は `CLAUDE_PROJECT_DIR`（プロジェクトルート）からの相対パスで、`.venv` の Python を使って `server.py` を起動する設定です。
- このファイルが存在すれば、Claude Code 起動時に自動でサーバーが登録されます。手動での追加登録は不要です。

未登録の別プロジェクトで一から追加したい場合は、CLI から次のように登録することもできます。

```bash
claude mcp add price-list-server -- "${PWD}/.venv/bin/python" "${PWD}/server.py"
```

## 5. 登録状態の確認

Claude Code のセッション内、または CLI から確認できます。

```bash
claude mcp list
```

`price-list-server` が表示され、接続状態が確認できれば登録成功です。

## 6. Claude Code で呼び出す

Claude Code のチャットで、次のように依頼します。

- 「`get_price_list` を呼んで価格一覧を表示して」
- 「price-list-server のツールで品物一覧を取得して」

Claude Code はツール `mcp__price-list-server__get_price_list` を自動的に認識し、呼び出します。

期待される結果（例）:

- りんご: 150円
- みかん: 100円
- バナナ: 80円

## 7. うまくいかないとき

- `.venv` が未作成 / 未有効化
  - `python3.12 -m venv .venv` と `source .venv/bin/activate` を再実行
- 依存未インストール
  - `pip install -r requirements.txt`
- `.mcp.json` のパスが誤っている
  - `command` が `.venv/bin/python` を指しているか確認
- 登録後にツールが認識されない
  - `claude mcp list` で接続状態を確認
  - Claude Code のセッションを再起動

---

最小確認だけをする場合は、次の2ステップで十分です。

1. `python3.12 server.py` が起動する
2. Claude Code から `get_price_list` を呼び出せる
