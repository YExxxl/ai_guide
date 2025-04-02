from flask import Flask, jsonify, send_from_directory, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.chat_models import ChatTongyi
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../../', static_url_path='')  # 指向根目录下的 index.html
CORS(app)  # 允许所有来源访问

# 获取当前脚本所在目录
base_dir = os.path.dirname(os.path.abspath(__file__))

# 加载数据
df = pd.read_csv(os.path.join(base_dir, 'chaozhou1.csv'))

# 处理数据和计算相似度
df['combined_features'] = df['标签'].fillna('') + ' ' + df['类别信息'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

@app.route('/', methods=['GET'])
def home():
    # 返回存储在根目录里的 index.html
    return send_from_directory(os.path.join(base_dir, '../../'), 'index.html')

@app.route('/api/tourist-routes', methods=['GET'])
def get_all_tourist_routes():
    # 返回所有景点的名称
    try:
        places = df['景点名'].dropna().tolist()
        return jsonify(places)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tourist-route/<string:place_name>', methods=['GET'])
def get_tourist_route(place_name):
    if not place_name:
        return jsonify({"error": "景点名称不能为空"}), 400

    try:
        # 获取与指定景点相似的景点推荐
        recommendations_similar = recommend_similar_places(place_name)
        recommendations_random = recommend_random_hot_places()
        
        # 合并推荐
        recommended_places = pd.concat([recommendations_similar, recommendations_random]).drop_duplicates().reset_index(drop=True)

        # 格式化为模型输入的格式
        places_info = "\n\n".join([
            f"景点名: {row['景点名']}\n标签: {row['标签']}\n坐标: {row['坐标']}\n距离: {row['距离']}\n价格: {row['价格']}\n评论数: {row['评论数']}"
            for _, row in recommended_places.iterrows()
        ])

        # 准备 API 密钥并初始化模型
        api_key = 'sk-841d558964ed40aeadea6bb2eeef03dd'  # 确保生产时安全存储
        llm = ChatTongyi(model="qwen-turbo-latest", temperature=0, api_key=api_key)

        # 创建聊天提示模板
        prompt_template = """
        你是一个旅游规划专家，帮助根据景点推荐生成合理的旅游路线。以下是我为你提供的几个推荐景点的信息：

        {places_info}

        请根据这些推荐景点，给出一个合理的旅游路线。输出的结果应包括：
        每个景点的访问顺序

        请根据起点的位置，到达每个景点的位置，距离给出路线，并考虑到旅行者的舒适度和观光顺序。不需要输出理由，
        只要输出一个访问顺序。每个景点前面加上潮州两个字。类似这样:
        潮州韩文公祠
        潮州广济桥
        潮州东山湖温泉度假村
        潮州绿太阳欢乐世界
        的格式

        """

        # 创建聊天提示
        chat_prompt = ChatPromptTemplate.from_template(prompt_template)

        # 创建链
        llm_chain = LLMChain(llm=llm, prompt=chat_prompt)

        # 获取路线建议
        tourist_route = llm_chain.run(places_info=places_info)

        # 在控制台输出
        print("Tourist Route:", tourist_route)

        # 返回响应，包括建议的路线
        return jsonify({"tourist_route": tourist_route})

    except Exception as e:
        # 错误处理
        return jsonify({"error": str(e)}), 500

def recommend_similar_places(place_name, top_n=5):
    try:
        idx = df[df['景点名'] == place_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
        place_indices = [i[0] for i in sim_scores]
        return df.iloc[place_indices]
    except IndexError:
        return pd.DataFrame()  # 返回空的 DataFrame 处理未找到的情况

def recommend_random_hot_places(top_n=4, top_range=15):
    top_places = df.sort_values(by='评论数', ascending=False).head(top_range)
    return top_places.sample(n=top_n)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 启动 Flask 应用，绑定到所有网络接口，端口为 5000
