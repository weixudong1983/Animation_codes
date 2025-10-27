from manim import *


# ===================== 节点类 =====================
class Node(VGroup):
    """链表节点"""
    def __init__(self, label: str, position: np.ndarray, color=BLUE_B, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=0.5, color=color, fill_opacity=0.8)
        self.circle.move_to(position)
        self.text = Text(label).move_to(position)
        self.add(self.circle, self.text)

    def fade_in(self, scene: Scene):
        scene.play(FadeIn(self))

    def fade_out(self, scene: Scene):
        scene.play(FadeOut(self))


# ===================== 队列类 =====================
class LinkedQueue:
    """链表队列，用于可视化"""
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
            self.scene.add(node)
            if i > 0:
                arrow = Arrow(self.nodes[i - 1].circle.get_right(),
                              node.circle.get_left(),
                              buff=0.1)
                self.arrows.append(arrow)
                self.scene.add(arrow)

        # Head / Tail 标签
        self.head_label = Text("Head", color=RED).next_to(self.nodes[0], DOWN)
        self.tail_label = Text("Tail", color=PURPLE).next_to(self.nodes[-1], DOWN)
        self.scene.add(self.head_label, self.tail_label)

    def enqueue(self, label: str):
        """入队操作：右侧淡入"""
        last_node = self.nodes[-1]
        new_pos = last_node.circle.get_center() + np.array([2, 0, 0])
        new_node = Node(label, new_pos)
        new_arrow = Arrow(last_node.circle.get_right(),
                          new_node.circle.get_left(),
                          buff=0.1)
        new_node.set_opacity(0)
        new_arrow.set_opacity(0)
        self.scene.add(new_arrow, new_node)

        # 动画：淡入
        self.scene.play(FadeIn(new_arrow), FadeIn(new_node))

        # 更新结构
        self.nodes.append(new_node)
        self.arrows.append(new_arrow)

        # 动画移动 Tail
        new_tail = Text("Tail", color=PURPLE).next_to(new_node, DOWN)
        self.scene.play(Transform(self.tail_label, new_tail))

    def dequeue(self):
        """出队操作：左侧淡出"""
        if not self.nodes:
            return

        first = self.nodes.pop(0)
        first.fade_out(self.scene)

        if self.arrows:
            first_arrow = self.arrows.pop(0)
            self.scene.play(FadeOut(first_arrow))

        # 整体左移保持左对齐
        shift = -2
        move_anims = [node.animate.shift(shift * RIGHT) for node in self.nodes] + \
                     [arrow.animate.shift(shift * RIGHT) for arrow in self.arrows]
        self.scene.play(*move_anims)

        # 更新 Head
        if self.nodes:
            new_head = Text("Head", color=RED).next_to(self.nodes[0], DOWN)
            self.scene.play(Transform(self.head_label, new_head))


# ===================== 动画场景 =====================
class LinkedQueueScene(Scene):
    def construct(self):
        queue = LinkedQueue(self)
        queue.build(["A", "B", "C"])
        self.wait(1)

        queue.enqueue("D")
        self.wait(1.5)

        queue.dequeue()
        self.wait(1.5)

        queue.enqueue("E")
        self.wait(2)
