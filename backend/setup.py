from setuptools import setup, find_packages

setup(
    name='ai_guide',  # 项目名称
    version='0.1.0',  # 版本号
    packages=find_packages(),  # 自动查找所有包
    install_requires=[
        'Flask==2.0.1',  # 确保 Flask 版本兼容
        'pandas==2.2.3',  # 使用当前环境中的 pandas 版本
        'scikit-learn==1.6.0',  # 添加 scikit-learn 作为项目依赖
        'langchain-community==0.3.13',  # 添加 langchain-community 作为项目依赖
        'flask-cors==3.0.10',  # 添加 flask-cors 作为项目依赖
    ],
    entry_points={
        'console_scripts': [
            'ai_guide=backend.python.Map:app.run',  # Map.py 中的 Flask 应用实例名为 app
        ],
    },
)
