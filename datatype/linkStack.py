import numpy as np
from manim import *

# ===================== 节点类 =====================
class Node(VGroup):
    """链表节点"""
    def __init__(self, label: str, position: np.ndarray, color=BLUE_B, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=0.5, color=color, fill_opacity=0.9)
        self.circle.move_to(position)
        self.text = Text(label, font="Consolas").move_to(position)
        self.text.set_color(BLACK)
        self.arrow = Arrow(self.circle.get_right(),
                            self.circle.get_right() + np.array([1, 0, 0]),
                              buff=0.1)
        self.add(self.circle, self.text, self.arrow)

    def fade_in(self, scene: Scene, run_time=1.0):
        scene.play(FadeIn(self), run_time=run_time)

    def fade_out(self, scene: Scene, run_time=0.8):
        scene.play(FadeOut(self), run_time=run_time)


# ===================== 堆栈类 =====================
class LinkedStack(VGroup):
    """链表堆栈，可视化结构"""
    def __init__(self, scene: Scene, start_x=-4, start_y=0, scale=1, **kwargs):
        super().__init__(**kwargs)  # 继承 VGroup 以支持 next_to 等方法
        self.scene = scene
        self.nodes: list[Node] = []
        self.arrows: list[Arrow] = []
        self.start_x = start_x
        self.start_y = start_y
        self.scale = scale

        self.top_label = None
        self.null_label = None

    def build(self, labels):
        """初始化堆栈"""
        for i, label in enumerate(labels):
            pos = [self.start_x + i * 2 * self.scale, self.start_y * self.scale, 0]

            node = Node(label, pos)
            node.scale(self.scale)
            self.nodes.append(node)
            self.add(node)  # 添加到 VGroup
            self.scene.add(node)
            # self.scene.play(FadeIn(node), run_time=0.5)

        # Top 标签
        if self.nodes:
            self.top_label = Text("Top", font="Microsoft YaHei", color=RED).next_to(self.nodes[0], DOWN).scale(self.scale)
        else:
            # 堆栈为空时，将标签放在起始位置下方
            pos = np.array([self.start_x, -1 + self.start_y, 0])
            pos *= self.scale
            self.top_label = Text("Top", font="Microsoft YaHei", color=RED).move_to(pos).scale(self.scale)
        self.add(self.top_label)  # 添加到 VGroup
        self.scene.add(self.top_label)

        # NULL 标签
        self.update_null_label()

    def update_null_label(self):
        """更新 NULL 标签位置"""
        # if self.null_label:
        #     self.remove(self.null_label)
        # if self.nodes:
        #     # NULL 在最后一个节点的箭头末端
        #     last_node = self.nodes[-1]
        #     null_pos = last_node.circle.get_right() + np.array([1, 0, 0])
        #     self.null_label = Text("NULL", font="Consolas", color=BLUE).move_to(null_pos).scale(self.scale)
        # else:
        #     # 堆栈为空，NULL 在起始位置
        #     pos = np.array([self.start_x + 1, self.start_y, 0])  # 假设在起始节点的箭头位置
        #     pos *= self.scale
        #     self.null_label = Text("NULL", font="Consolas", color=BLUE).move_to(pos).scale(self.scale)
        # self.add(self.null_label)
        # self.scene.add(self.null_label)

    def push(self, label: str):
        """入栈操作：左边淡入，新元素插入栈顶，然后整体右移已有节点"""
        new_pos = np.array([self.start_x, self.start_y+2, 0])
        new_pos *= self.scale
        new_node = Node(label, new_pos)
        new_node.scale(self.scale)
        # 先淡入新节点
        self.scene.play(FadeIn(new_node), run_time=1.0)
        self.add(new_node)  # 添加到 VGroup

        # 然后整体右移已有节点（每个右移2）
        shift = 2 * self.scale
        move_anims = [node.animate.shift(shift * RIGHT) for node in self.nodes]
        move_anims.append(new_node.animate.shift(DOWN* 2 * self.scale))
        if move_anims:
            self.scene.play(*move_anims, run_time=0.8)


        
        # 更新结构：新节点插入到最左边
        self.nodes.insert(0, new_node)

        # 更新 Top 标签到新的栈顶（最左边）
        if self.nodes:
            new_top = Text("Top", font="Microsoft YaHei", color=RED).next_to(self.nodes[0], DOWN).scale(self.scale)
            self.scene.play(Transform(self.top_label, new_top), run_time=0.8)

        # 更新 NULL 标签
        self.update_null_label()

        self.scene.wait(0.7)

    def pop(self):
        """出栈操作：左边淡出，栈顶消失，然后整体左移"""
        if not self.nodes:
            return

        first = self.nodes.pop(0)
        first.fade_out(self.scene)
        self.remove(first)  # 从 VGroup 中移除

        # 整体左移剩余节点（每个左移2）
        shift = -2 * self.scale
        move_anims = [node.animate.shift(shift * RIGHT) for node in self.nodes]
        if move_anims:
            self.scene.play(*move_anims, run_time=0.8)

        # 更新 Top 标签的位置
        if self.nodes:
            new_top = Text("Top", font="Microsoft YaHei", color=RED).next_to(self.nodes[0], DOWN).scale(self.scale)
            self.scene.play(Transform(self.top_label, new_top), run_time=0.8)
        else:
            # 堆栈已空，将标签移动回起始位置
            pos = np.array([self.start_x, -1 + self.start_y, 0])
            pos *= self.scale
            self.scene.play(
                Transform(self.top_label, Text("Top", font="Microsoft YaHei", color=RED).move_to(pos).scale(self.scale)),
                run_time=0.8,
            )

        # 更新 NULL 标签
        self.update_null_label()

        self.scene.wait(1.4)