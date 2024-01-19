# 此处是测试代码语法正确性的地方


class Buffrable:
    def __init__(self) -> None:
        # 角色的BUFF状态，初始啥都是空，空即为最初的状态
        self.Buff_state = {}

    """buff_num 为此BUFF对应的状态"""

    def add_Buff(self, buff_name: str, buff_num: int):
        self.Buff_state[buff_name] = buff_num


A = Buffrable()

A.add_Buff("a", 1)

print(A)
