# ローカル MCP サーバーを実行し、Copilot から使う手順

このドキュメントでは、このリポジトリの `server.py` をローカルで動かし、VS Code の Copilot Chat から `get_price_list` ツールを呼び出すまでを説明します。

## 1. 前提

- Python 3.12
- VS Code
- GitHub Copilot / Copilot Chat が利用可能

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

## 4. Copilot から使えるように登録する

Copilot 側では、MCP サーバーを「コマンドで起動する外部ツール」として登録します。

### 方法A: VS Code の UI から登録（推奨）

1. コマンドパレットを開く（`Ctrl+Shift+P` / `Cmd+Shift+P`）
2. MCP サーバー追加系のコマンドを選択
3. サーバー名: `price-list-server`
4. コマンド: `${workspaceFolder}/.venv/bin/python`
5. 引数: `${workspaceFolder}/server.py`
6. 保存

> 補足: コマンド名は VS Code / 拡張機能のバージョンで若干異なることがあります。

### 方法B: 設定ファイルで登録（UI が使えない場合）

MCP 設定ファイルに、`price-list-server` を `stdio` サーバーとして追加します。例:

```json
{
  "servers": {
    "price-list-server": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/server.py"]
    }
  }
}
```

> 注: 設定ファイル名や保存場所は環境により異なる場合があります。UI から追加できる場合は UI を優先してください。

## 5. Copilot Chat で呼び出す

1. Copilot Chat を開く
2. 例として次のように依頼する

- 「`get_price_list` を呼んで価格一覧を表示して」
- 「price-list-server のツールで品物一覧を取得して」

期待される結果（例）:

- りんご: 150円
- みかん: 100円
- バナナ: 80円

## 6. うまくいかないとき

- `.venv` が未作成 / 未有効化
  - `python3.12 -m venv .venv` と `source .venv/bin/activate` を再実行
- 依存未インストール
  - `pip install -r requirements.txt`
- サーバー起動コマンドのパス誤り
  - `command` が `.venv/bin/python` を指しているか確認
- 登録後に認識されない
  - VS Code の再読み込み（Developer: Reload Window）を実施

---

最小確認だけをする場合は、次の2ステップで十分です。

1. `python3.12 server.py` が起動する
2. Copilot Chat から `get_price_list` を呼び出せる
