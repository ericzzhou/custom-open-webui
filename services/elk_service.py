class ELKService:
    def __init__(self, model_id):
        self.model_id = model_id
        # connections.connect(alias="default", host="44.236.217.101", port="19530")

    def run(self, prompt):
        return f"prompt:{prompt},从elk里查询到数据"
