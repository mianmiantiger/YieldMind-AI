# main.py
from agents.tools.yield_scout import get_best_yields

def run_yield_mind_agent(user_query):
    """
    这是 YieldMind AI 的核心启动逻辑
    """
    print(f"用户问题: {user_query}")
    
    # 逻辑判断：如果用户提到了“收益”或“赚钱”
    if "收益" in user_query or "yield" in user_query:
        # 调用你写在 agents/tools 里的工具
        result = get_best_yields(protocol="DODO")
        print(f"AI Agent 响应: {result}")
    else:
        print("AI Agent 响应: 我现在专门负责找高收益池子，请问你想了解哪个协议？")

# 模拟运行
if __name__ == "__main__":
    run_yield_mind_agent("帮我看看 DODO 上哪个收益最高？")