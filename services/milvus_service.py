# 模拟的聊天功能
from pymilvus import Collection, connections
import requests


class MilvusService:
    def __init__(self, model_id):
        self.model_id = model_id
        connections.connect(alias="default", host="44.236.217.101", port="19530")

    def get_vector_embedding(self, keyword):
        # 定义请求的 URL 和参数
        url = f"https://bge.yamibuy.net/zh/bge/vector"
        params = {"keyword": keyword}

        try:
            # 发送 GET 请求
            response = requests.get(url, params=params)

            # 检查响应状态码
            response.raise_for_status()

            # 返回 JSON 数据
            return response.json()

        except requests.RequestException as e:
            # 处理请求异常
            print(f"请求错误: {e}")
            return None

    def convert_string_to_float_array(self, embedding_str):
        """
        将包含浮点数的字符串转换为浮点数数组

        参数:
        embedding_str (str): 包含浮点数的字符串，每个浮点数由逗号分隔

        返回:
        List[float]: 转换后的浮点数数组
        """
        # 将字符串分割成列表
        embedding_list = embedding_str.split(",")

        # 将列表中的字符串转换为浮点数
        embedding_floats = [float(num) for num in embedding_list]

        return embedding_floats

    def run(self, prompt):
        milvus_collection_name = self.model_id.split(":")[1].strip()

        db = Collection(name=milvus_collection_name)
        print("schema \n")
        print(db.schema)
        # 加载集合
        db.load()

        print(f"集合 {milvus_collection_name} 已加载")

        query_vector = self.get_vector_embedding(prompt)["data"]
        embedding_list = self.convert_string_to_float_array(query_vector)
        print("完成keyword向量化")
        search_param = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nprobe": 10},
        }

        results = db.search(
            data=[embedding_list],
            anns_field="embedding",  # 向量字段名称
            param=search_param,
            limit=10,
            expr=None,
            output_fields=["item_number"],
        )
        connections.disconnect(alias="default")
        print("milvus 查询完成")
        items = []
        for result in results:
            for hit in result:
                goods_number = hit.entity.get("item_number")
                items.append(goods_number)
                print(goods_number)

        # 查询数据库

        # # 这里可以是一个复杂的生成逻辑，比如基于模型的回答
        # return f"Response from {model_id}: Echo: {prompt},Result:{results}"
        return f"查询到以下商品：\n {' \n '.join(items)}"  # 或者使用其他合适的连接符号
