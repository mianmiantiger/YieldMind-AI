"""
OpenClaw 可调用工具集合：
1) `get_best_yields`：示例用的收益池扫描（模拟数据）。
2) `get_solana_status`：通过 SOLANA_RPC_URL 调用 `getSlot` 获取网络高度（slot）。
3) `get_solana_price`：通过 Jupiter API 获取 SOL 实时价格。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests

try:
    # 用于从项目根目录读取 .env
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None  # type: ignore[misc, assignment]


# 加载 .env（例如 SOLANA_RPC_URL）
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if load_dotenv is not None:
    load_dotenv(_PROJECT_ROOT / ".env")


_RPC_TIMEOUT_SEC = 30
_HTTP_TIMEOUT_SEC = 20


def get_best_yields(protocol: str = "DODO") -> str:
    """
    供 OpenClaw Agent 调用的工具函数（示例）。

    目前返回的是模拟链上收益数据，后续你可以把它替换为真实的多链抓取逻辑。
    """
    mock_data = [
        {"pool": "USDC/USDT", "apy": "5.2%", "risk": "Low"},
        {"pool": "ETH/USDC", "apy": "12.5%", "risk": "Medium"},
        {"pool": "DODO/USDT", "apy": "18.1%", "risk": "High"},
    ]

    # 找到 APY 最高的项（例如 "18.1%" -> 18.1）
    best_pool = max(mock_data, key=lambda x: float(x["apy"].strip("%")))
    return f"我是你的 AI 助手。通过扫描，{protocol} 上最赚钱的是 {best_pool['pool']}，收益率高达 {best_pool['apy']}！"


def get_solana_status() -> str:
    """
    获取 Solana 网络当前最新区块高度（slot）。

    - 从环境变量读取：`SOLANA_RPC_URL`
    - 向 RPC 发送 JSON-RPC：`getSlot`（commitment 使用 `finalized`）

    Returns:
        成功：包含 slot 的简短说明字符串
        失败：包含错误原因的可读字符串
    """
    rpc_url = (os.getenv("SOLANA_RPC_URL") or "").strip()
    if not rpc_url:
        return (
            "无法查询 Solana 网络高度：未配置 SOLANA_RPC_URL。"
            "请在项目根目录 .env 中设置有效的 HTTP RPC URL。"
        )

    payload: dict[str, Any] = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": [{"commitment": "finalized"}],
    }

    try:
        resp = requests.post(
            rpc_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=_RPC_TIMEOUT_SEC,
        )
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        return "Solana RPC 请求超时，请稍后重试或检查网络与 RPC 端点。"
    except requests.exceptions.ConnectionError:
        return "无法连接 Solana RPC，请检查 SOLANA_RPC_URL 是否可达。"
    except requests.exceptions.RequestException as exc:
        return f"Solana RPC 请求失败：{exc}"

    try:
        data = resp.json()
    except ValueError:
        return "Solana RPC 返回了非 JSON 响应，无法解析区块高度。"

    if not isinstance(data, dict):
        return "Solana RPC 返回格式异常，无法解析区块高度。"

    # RPC 错误分支：{"error": {"message": "..."}}
    err = data.get("error")
    if err is not None:
        msg = err.get("message", "unknown") if isinstance(err, dict) else str(err)
        return f"Solana RPC 错误：{msg}"

    result = data.get("result")
    if result is None:
        return "Solana RPC 响应中缺少 result 字段。"
    if not isinstance(result, int):
        return f"Solana getSlot 返回类型异常（期望整数）：{type(result).__name__}"

    return f"当前网络高度 (Slot，finalized) 为：{result}"


def get_solana_price() -> str:
    """
    获取 SOL 的实时价格（美元计价）：
    使用 Jupiter Price API：
    https://api.jup.ag/price/v2/full?ids=So11111111111111111111111111111111111111112

    Returns:
        成功：包含 SOL 实时价格（约值）的可读字符串
        失败：包含错误原因的可读字符串
    """
    url = "https://api.jup.ag/price/v2/full?ids=So11111111111111111111111111111111111111112"

    try:
        resp = requests.get(url, timeout=_HTTP_TIMEOUT_SEC)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        return "获取 SOL 价格超时，请稍后重试。"
    except requests.exceptions.ConnectionError:
        return "无法连接 Jupiter 价格 API，请检查网络连通性。"
    except requests.exceptions.RequestException as exc:
        return f"获取 SOL 价格失败：{exc}"

    try:
        data = resp.json()
    except ValueError:
        return "Jupiter API 返回了非 JSON 响应，无法解析价格。"

    if not isinstance(data, dict):
        return "Jupiter API 返回格式异常，无法解析价格。"

    token_id = "So11111111111111111111111111111111111111112"
    # Jupiter 返回结构通常在 data[token_id].price（不同版本可能略有差异，这里做了宽松解析）
    price = None
    if isinstance(data.get("data"), dict) and isinstance(data["data"].get(token_id), dict):
        price = data["data"][token_id].get("price")
    if price is None and isinstance(data.get(token_id), dict):
        price = data[token_id].get("price")

    if price is None:
        return "Jupiter API 响应中未找到 SOL 价格字段。"

    # 尝试把价格转成数字（如果是字符串也能解析）
    try:
        price_num = float(price)
        return f"SOL 实时价格约为：{price_num:.6f} USD"
    except (TypeError, ValueError):
        return f"SOL 实时价格约为：{price} USD"


if __name__ == "__main__":
    # 简单的本地测试：同时输出网络高度与 SOL 实时价格
    print(get_solana_status())
    print(get_solana_price())
