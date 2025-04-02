from flask import Flask, request, jsonify, render_template
import os
from langchain_community.chat_models import ChatTongyi
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import pandas as pd

# 初始化 Flask 应用
app = Flask(__name__)

# 获取当前脚本所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 读取 CSV 文件
df = pd.read_csv(os.path.join(base_dir, 'chaozhou1.csv'))
# 格式化为模型输入的格式
places_info = ""
for idx, row in df.iterrows():
    places_info += f"景点名: {row['景点名']}\n标签: {row['标签']}\n坐标: {row['坐标']}\n距离: {row['距离']}\n价格: {row['价格']}\n评论数: {row['评论数']}\n\n"

# 准备 API 密钥并初始化模型
api_key = 'sk-841d558964ed40aeadea6bb2eeef03dd'  # 确保生产时安全存储
llm = ChatTongyi(model="qwen-turbo-latest", temperature=0, api_key=api_key)

# 创建聊天提示模板
prompt_template = """
这是一些潮州景点信息{places_info}
你是一个潮州推荐导游，下面是游客的问题，请根据潮州特点进行简要回答。{problem}不要出现奇怪的符号输出。
"""

# 创建聊天提示
chat_prompt = ChatPromptTemplate.from_template(prompt_template)

# 创建 LLMChain
llm_chain = LLMChain(llm=llm, prompt=chat_prompt)

# 设置聊天接口
@app.route('/api/tourist-route/chat', methods=['GET'])  # 允许 GET 方法
def chat():
    problem = request.args.get('message')  # 使用 request.args.get 获取 URL 参数
    print(f"Received user message: {problem}")
    if problem:
        # 获取 LLM 响应
        response = llm_chain.run({'places_info': places_info, 'problem': problem})
        print(f"LLM response: {response}")
        return jsonify({'reply': response})  # 修改返回的键为 'reply'
    return jsonify({'error': 'No message provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
