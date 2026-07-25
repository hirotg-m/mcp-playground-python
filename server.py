
"""価格一覧を返す、最小構成の MCP サーバーです。

このモジュールは `get_price_list` ツールを公開し、
固定の品目データ（ITEMS）をそのまま返します。
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("price-list-server")


ITEMS: list[dict[str, int | str]] = [
    {"name": "りんご", "price_yen": 150},
    {"name": "みかん", "price_yen": 100},
    {"name": "バナナ", "price_yen": 80},
]


@mcp.tool()
def get_price_list() -> list[dict[str, int | str]]:
    """品物と価格の一覧を返します。"""
    return ITEMS


if __name__ == "__main__":
    mcp.run()
