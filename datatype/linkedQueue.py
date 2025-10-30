from manim import *
import numpy as np

config.background_color = '#333333'  # None 表示透明


# ===================== 节点类 =====================
class Node(VGroup):
    """链表节点"""
    def __init__(self, label: str, position: np.ndarray, color=BLUE_B, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=0.5, color=color, fill_opacity=0.8)
        self.circle.move_to(position)
        self.text = Text(label,font="Consolas").move_to(position)
        self.arrow = Arrow(self.circle.get_right(),
                            self.circle.get_right() + np.array([1, 0, 0]),
                              buff=0.1)
        self.add(self.circle, self.text, self.arrow )

    def fade_in(self, scene: Scene, run_time=1.0):
        scene.play(FadeIn(self), run_time=run_time)

    def fade_out(self, scene: Scene, run_time=0.8):
        scene.play(FadeOut(self), run_time=run_time)


# ===================== 队列类 =====================
class LinkedQueue:
    """链表队列，可视化结构"""
    def __init__(self, scene: Scene, start_x=-4):
        self.scene = scene
        self.nodes: list[Node] = []
        self.arrows: list[Arrow] = []
        self.start_x = start_x

        self.head_label = None
        self.tail_label = None

    def build(self, labels):
        """初始化队列"""
        for i, label in enumerate(labels):
            pos = [self.start_x + i * 2, 0, 0]
            node = Node(label, pos)
            self.nodes.append(node)
            self.scene.play(FadeIn(node), run_time=0.5)
            # if i > 0:
            #     arrow = Arrow(self.nodes[i - 1].circle.get_right(),
            #                   node.circle.get_left(),
            #                   buff=0.1)
            #     self.arrows.append(arrow)
            #     self.scene.add(arrow)

        # Head / Tail 标签
        if self.nodes:
            self.head_label = Text("队首",font="Microsoft YaHei", color=RED).next_to(self.nodes[0], DOWN)
            self.tail_label = Text("队尾", font="Microsoft YaHei",color=PURPLE).next_to(self.nodes[-1], DOWN)
        else:
            # 队列为空时，将标签放在起始位置下方，保证显示不出错
            pos = np.array([self.start_x, -1, 0])
            self.head_label = Text("队首", font="Microsoft YaHei",color=RED).move_to(pos)
            self.tail_label = Text("队尾", font="Microsoft YaHei",color=PURPLE).move_to(pos).shift(RIGHT*1.2)
        self.scene.add(self.head_label, self.tail_label)

    def enqueue(self, label: str):
        """入队操作：右侧淡入"""
        if not self.nodes:
            # 第一个节点的位置使用 start_x
            new_pos = np.array([self.start_x, 0, 0])
        else:
            last_node = self.nodes[-1]
            new_pos = last_node.circle.get_center() + np.array([2, 0, 0])
        new_node = Node(label, new_pos)
        # new_arrow = Arrow(last_node.circle.get_right(),
        #                   new_node.circle.get_left(),
        #                   buff=0.1)
        #new_node.set_opacity(0)
        # new_arrow.set_opacity(0)
        #self.scene.add( new_node)

        # 动画：新节点与箭头淡入（1秒）
        self.scene.play(FadeIn(new_node), run_time=1.0)
        #new_node.fade_in(self.scene, run_time=1.0)

        # 更新结构
        self.nodes.append(new_node)
        #self.arrows.append(new_arrow)

        # Tail 平滑移动（1秒）
        # if self.tail_label is None:
        #     self.tail_label = Text("队尾", color=PURPLE).next_to(new_node, DOWN)
        #     self.scene.add(self.tail_label)
        # else:
        #     new_tail = Text("队尾", color=PURPLE).next_to(new_node, DOWN)
        #     self.scene.play(Transform(self.tail_label, new_tail), run_time=1.0)
        # 如果是第一个节点，也需要设置 Head
        if len(self.nodes) == 1:
            """"""
            # if self.head_label is None:
            #     self.head_label = Text("队首", color=RED).next_to(new_node, DOWN)
            #     self.scene.add(self.head_label)
            # else:
            #     new_head = Text("队首", color=RED).next_to(new_node, DOWN)
            #     self.scene.play(Transform(self.head_label, new_head), run_time=0.5)
        else:
            new_tail = Text("队尾", font="Microsoft YaHei",color=PURPLE).next_to(new_node, DOWN)
            self.scene.play(Transform(self.tail_label, new_tail), run_time=1.0)
            self.scene.wait(0.7)
            return
        self.scene.wait(3)

    def dequeue(self):
        """出队操作：左侧淡出"""
        if not self.nodes:
            return

        first = self.nodes.pop(0)
        first.fade_out(self.scene)

        # if self.arrows:
        #     first_arrow = self.arrows.pop(0)
        #     self.scene.play(FadeOut(first_arrow), run_time=0.8)

        # 整体左移保持左对齐
        shift = -2
        move_anims = [node.animate.shift(shift * RIGHT) for node in self.nodes]
        if move_anims:
            self.scene.play(*move_anims, run_time=0.8)

        # 更新 Head / Tail 标签的位置或隐藏到起始位置
        if self.nodes:
            new_head = Text("队首", font="Microsoft YaHei",color=RED).next_to(self.nodes[0], DOWN)
            self.scene.play(Transform(self.head_label, new_head), run_time=0.8)
            # 更新 Tail 为最后一个节点下方
            last_node = self.nodes[-1]
            new_tail = Text("队尾", font="Microsoft YaHei",color=PURPLE).next_to(last_node, DOWN)
            self.scene.play(Transform(self.tail_label, new_tail), run_time=1.0)
        else:
            # 队列已空，将标签移动回起始位置以避免无效 next_to 错误
            pos = np.array([self.start_x, -1, 0])
            self.scene.play(
                Transform(self.head_label, Text("队首",font="Microsoft YaHei", color=RED).move_to(pos)),
                Transform(self.tail_label, Text("队尾", font="Microsoft YaHei",color=PURPLE).move_to(pos)),
                run_time=0.8,
            )
        self.scene.wait(1.4)

class LinkedQueueExampleScene(Scene):
    def construct(self):
        queue = LinkedQueue(self)
        self.wait(2)
        queue.build([])
        
        self.wait(2)

        queue.enqueue("10")
        queue.enqueue("20")
        self.wait(2)
        queue.enqueue("30")
        self.wait(2)
        #queue.enqueue("F")
        #self.wait(1.0)

        queue.dequeue()
        #self.wait(1.0)

        #queue.enqueue("E")
        self.wait(1.5)
# ===================== 动画场景 =====================
class LinkedQueueScene(Scene):
    def construct(self):
        queue = LinkedQueue(self)
        queue.build(["A", "B", "C"])
        self.wait(0.8)

        queue.enqueue("D")
        
        #queue.enqueue("F")
        self.wait(1.0)

        queue.dequeue()
        #self.wait(1.0)

        #queue.enqueue("E")
        self.wait(1.5)