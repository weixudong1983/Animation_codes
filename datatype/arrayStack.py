from manim import *
from lib.code import CodeHighlight
from lib.fakeScene import FakeScene


class ArrayStack(VGroup):
    def __init__(self, capacity=6, box_size=0.9, gap=0.12, **kwargs):
        super().__init__(**kwargs)
        self.capacity = capacity
        self.box_size = box_size
        self.gap = gap
        self.top = -1  # 栈顶从左边开始（索引 -1 表示栈空）
        self.boxes = []
        self.value_texts = [None] * capacity
        self.index_labels = []
        # 创建一列 boxes 的 VGroup 再一次性 arrange（避免重复 add 导致索引重叠）
        boxes_group = VGroup()
        for i in range(capacity):
            box = Square(self.box_size, stroke_color=BLUE, stroke_width=3).set_fill("#f4d03f", opacity=0)
            boxes_group.add(box)
            self.boxes.append(box)
        boxes_group.arrange(RIGHT, buff=self.gap)
        # 添加到整体，并为每个 box 添加 index 标签（在下方）
        self.add(boxes_group)
        for i, box in enumerate(self.boxes):
            idx_label = Text(str(i), font_size=20)
            idx_label.next_to(box, DOWN, buff=0.25)
            self.index_labels.append(idx_label)
            self.add(idx_label)

        # Top 指针
        self.top_label = Text("Top", color=GREEN, font_size=36,)
        self.update_pointer_position()
        self.add(self.top_label)

    def update_pointer_position(self):
        # 将 Top 放到栈顶 box 的上方（如果栈空，则在最左边 box 上方或隐藏）
        if self.top >= 0:  # 如果有元素，放在当前 top 对应的 box 上方
            self.top_label.next_to(self.boxes[self.top], UP, buff=0.25)
        else:  # 栈空，放在最左边 box 上方
            self.top_label.next_to(self.boxes[0], UP, buff=0.25).shift(LEFT)

    def push(self, value, scene: Scene,speed=1.0):
        
        # 判满
        len = self.capacity - 1
        if self.top >= len:
            warn = Text("Stack full!", font_size=36, color=YELLOW).next_to(self.boxes[len], RIGHT, buff=0.2)
            scene.play(FadeIn(warn), run_time=0.4*speed)
            scene.wait(0.3)
            scene.play(FadeOut(warn), run_time=0.3*speed)
            return

        # 更新 top 指针（向右移动）
        self.top += 1
        # 在 self.top 的格子中显示值（淡入），从左边开始
        target = self.boxes[self.top]
        if self.value_texts[self.top] is not None:
            scene.play(FadeOut(self.value_texts[self.top]), run_time=0.5*speed)
        text = Text(str(value), font_size=28, color=BLACK).move_to(target.get_center())
        self.value_texts[self.top] = text
        target.set_fill("#f4d03f", opacity=1)
        # 仅渐入动画，无位移
        scene.play(FadeIn(text), run_time=1.5*speed)  # 调整时间，总约3秒

        # 更新指针位置
        scene.play(
            self.top_label.animate.next_to(self.boxes[self.top], UP, buff=0.25),
            run_time=0.5*speed,
        )

    def pop(self, scene: Scene):
        # 判空
        if self.top < 0:
            warn = Text("Stack empty!", font_size=24, color=YELLOW).next_to(self, UP, buff=0.2)
            scene.play(FadeIn(warn), run_time=0.5)
            scene.wait(0.5)
            scene.play(FadeOut(warn), run_time=0.5)
            return

        # 在栈顶位置淡出文字并清空填充
        if self.value_texts[self.top] is not None:
            # 仅渐出动画，无位移
            scene.play(FadeOut(self.value_texts[self.top]), run_time=1.5)  # 调整时间，总约3秒
            self.value_texts[self.top] = None
        self.boxes[self.top].set_fill("#f4d03f", opacity=0)

        # 更新 top 指针（向左移动）
        self.top -= 1
        # 更新指针位置
        scene.play(
            self.top_label.animate.next_to(self.boxes[self.top] if self.top >= 0 else self.boxes[0], UP, buff=0.25),
            run_time=0.5,
        )

    def set_data(self, data_list,scene: Scene):
        # 将指定数据写入堆栈（data_list 的长度 <= capacity）
        # 先清空
        for i in range(self.capacity):
            if self.value_texts[i] is not None:
                self.value_texts[i].become(Text(str(i), font_size=20))  # 替换为 index 文本占位
            self.boxes[i].set_fill("#f4d03f", opacity=0)
            self.value_texts[i] = None

        # 从左边开始设置数据
        self.top = -1
        for v in data_list:
            self.push(v, scene,0.1)  # 使用辅助场景仅改变内部状态（无动画）
        # 重新更新指针位置
        self.update_pointer_position()