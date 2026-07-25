# mcp-playground-python

はじめてのMCPサーバー練習用の最小サンプルです。

## できること

`get_price_list` ツールで、品物と価格の一覧を返します。

- りんご: 150円
- みかん: 100円
- バナナ: 80円

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

```bash
python server.py
```

## MCP設定ファイル

- `.mcp.json` — Claude Code 用の MCP サーバー設定です。
- `.vscode/mcp.json` — GitHub Copilot 用の MCP サーバー設定です。