import openai

# Set up the OpenAI API client
openai.api_key = "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"

# 定义一个函数生成 ChatGPT 的回复
def generate_response(prompt):
    # 调用 OpenAI API 生成回复
    completions = openai.Completion.create(
        engine="text-davinci-003",  # 指定使用的引擎名称
        prompt=prompt,  # API 请求的提示信息
        max_tokens=1024,  # API 响应的最大令牌数
        n=1,  # API 请求的完成数
        stop=None,  # API 响应的终止标志
        temperature=0.5,  # API 请求的温度参数
    )

    # 从 API 响应中取得回复
    message = completions.choices[0].text
    return message
"""
prompt：提问，提问描述越详细，回答越准确
temperature：控制结果的随机性，如果希望结果更有差异性 0.9，或者希望有固定结果可以尝试 0.0
max_tokens：生成结果时的最大 tokens 数。平均一个汉字是 2 个 tokens，text-davinci-003 最多是 4000 个 tokens，也就是 2000 个汉字左右
top_p：一个可用于代替 temperature 的参数，对应机器学习中 nucleus sampling，如果设置 0.1 意味着只考虑构成前 10% 概率质量的 tokens
frequency_penalty：控制字符的重复度，取值为 -2.0 ~ 2.0 之间的数字
presence_penalty：控制主题的重复度，取值为 -2.0 ~ 2.0 之间的数字
"""

# 初始化一个变量来存储对话上下文
context = "技术依赖性"

# 开始一个死循环来接受用户输入
while True:
    # 提示用户输入信息
    user_input = input("你：")
    # 如果用户输入结束命令，退出循环
    if user_input in ["结束", "退出", "end", "exit"]:
        break
    # 把用户输入信息添加到对话上下文中
    context = context + user_input + "\n"
    # 调用 generate_response() 函数生成回复
    response = generate_response(context)
    # 显示 ChatGPT 的回复
    print("ChatGPT：" + response)
    # 把 ChatGPT 的回复添加到对话上下文中
    context = context + response + "\n"

