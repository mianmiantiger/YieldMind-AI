# yield_scout.py

def get_best_yields(protocol="DODO"):
    """
    这是供 OpenClaw Agent 调用的函数。
    它会返回模拟的链上收益数据。
    """
    # 模拟数据：未来我们会接入 Alchemy API 替换它
    mock_data = [
        {"pool": "USDC/USDT", "apy": "5.2%", "risk": "Low"},
        {"pool": "ETH/USDC", "apy": "12.5%", "risk": "Medium"},
        {"pool": "DODO/USDT", "apy": "18.1%", "risk": "High"}
    ]
    
    # 找到 APY 最高的项
    best_pool = max(mock_data, key=lambda x: float(x['apy'].strip('%')))
    
    return f"我是你的 AI 助手。通过扫描，{protocol} 上最赚钱的是 {best_pool['pool']}，收益率高达 {best_pool['apy']}！"