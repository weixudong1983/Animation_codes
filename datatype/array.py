from manim import *

# 可配置全局透明背景（剪辑友好）
config.background_color = '#333333'
# config.pixel_width = 1920
# config.pixel_height = 1080



class ArrayCell(VGroup):
    """单个格子对象，支持淡入淡出与内容更新"""
    def __init__(self, index, value=None, width=1.0, height=1.0, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.width = width
        self.height = height
        self.value = value

        # 绘制边框
        self.rect = Square(side_length=1.0).set_stroke(BLUE, 2).set_fill(BLACK, 0)
        # 索引文字
        self.index_text = Text(str(index), font_size=28,font="Consolas").next_to(self.rect, DOWN)
        # 内容文字
        self.value_text = Text(str(value), font_size=36,font="Consolas").move_to(self.rect) if value is not None else None

        self.add(self.rect, self.index_text)
        if self.value_text:
            self.add(self.value_text)

    def set_value(self, value, scene: Scene):
        """淡入显示新值"""
        self.value = value
        new_text = Text(str(value), font_size=36,font="Consolas", color=BLACK).move_to(self.rect)
        new_bg = self.rect.copy().set_fill(YELLOW, opacity=1)
        scene.play(
            FadeIn(new_bg, scale=1.1),
            FadeIn(new_text),
            run_time=0.5
        )
        # 保存对值的背景和文字的引用，便于 later 清理
        self.add(new_bg, new_text)
        self.value_text = new_text
        self.value_bg = new_bg

    def clear_value(self, scene: Scene):
        """淡出删除值"""
        animations = []
        if getattr(self, "value_text", None):
            animations.append(FadeOut(self.value_text, shift=DOWN, run_time=0.4))
        if getattr(self, "value_bg", None):
            # 背景淡出不移动，只淡出
            animations.append(FadeOut(self.value_bg, run_time=0.4))

        if animations:
            scene.play(*animations)

        # 从群组中移除已删除的子项，避免累积不可见对象
        if getattr(self, "value_text", None) in self:
            try:
                self.remove(self.value_text)
            except Exception:
                pass
        if getattr(self, "value_bg", None) in self:
            try:
                self.remove(self.value_bg)
            except Exception:
                pass

        # 恢复原始方块填充与状态
        self.rect.set_fill(BLACK, 0)
        self.value_text = None
        self.value_bg = None
        self.value = None


class ArrayQueue(VGroup):
    """数组实现的队列，带入队出队动画"""
    def __init__(self, size=6, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.front = 0
        self.back = 0
        self.count = 0

        # 初始化格子
        self.cells = [ArrayCell(i) for i in range(size)]
        for i, c in enumerate(self.cells):
            c.shift(RIGHT * i)
        self.add(*self.cells)

        # F 和 B 标签

        self.front_label = Text("Head", color=GREEN, font_size=36).next_to(self.cells[0].rect, UP)
        #self.back_label = Text("Tail", color=PURPLE, font_size=36).next_to(self.cells[0].rect, UP)
        self.add(self.front_label)
        self.update_pointer_positions()

    def update_pointer_positions(self):
        """更新 F / B 指针位置"""
        self.front_label.next_to(self.cells[self.front].rect, UP)
        #self.back_label.next_to(self.cells[self.back].rect, UP)

    def enqueue(self, scene: Scene, value):
        """入队操作：在尾部设置值"""
        if self.count == self.size:
            print("队列已满")
            return
        cell = self.cells[self.back]
        cell.set_value(value, scene)
        self.back = (self.back + 1) % self.size
        self.count += 1
        #scene.play(self.back_label.animate.next_to(self.cells[self.back].rect, UP), run_time=0.5)
        scene.wait(2.2)

    def dequeue(self, scene: Scene):
        """出队操作：从头部删除"""
        if self.count == 0:
            print("队列为空")
            return
        cell = self.cells[self.front]
        cell.clear_value(scene)
        self.front = (self.front + 1) % self.size
        self.count -= 1
        scene.play(self.front_label.animate.next_to(self.cells[self.front].rect, UP), run_time=0.5)
        scene.wait(2.1)

    def compact_front(self, scene: Scene, run_time: float = 0.8):
        """
        如果 head（front）前有空位，则将队列中的所有数据整体向前（靠左）移动到从 0 开始的位置。
        动画地把每个单元的值移动到新的格子中心，并在动画结束后更新内部引用与指针。

        使用场景示例：
            queue.compact_front(self)
        """
        # 没有数据或已经在头部，无需操作
        if self.count == 0 or self.front == 0:
            return

        animations = []
        moves = []  # 存放 (src_idx, tgt_idx) 的映射

        for i in range(self.count):
            src_idx = (self.front + i) % self.size
            tgt_idx = i
            src_cell = self.cells[src_idx]
            tgt_cell = self.cells[tgt_idx]

            # 收集要移动的可视对象（背景和文本）
            items = []
            if getattr(src_cell, "value_bg", None) is not None:
                items.append(src_cell.value_bg)
            if getattr(src_cell, "value_text", None) is not None:
                items.append(src_cell.value_text)

            if items:
                grp = VGroup(*items)
                animations.append(grp.animate.move_to(tgt_cell.rect.get_center()))
                moves.append((src_idx, tgt_idx, items))

        if animations:
            scene.play(*animations, run_time=run_time)

            # 动画完成后，调整父子关系并更新引用
            for src_idx, tgt_idx, items in moves:
                src_cell = self.cells[src_idx]
                tgt_cell = self.cells[tgt_idx]
                # 从源单元中移除对象并添加到目标单元
                try:
                    for it in items:
                        if it in src_cell:
                            src_cell.remove(it)
                except Exception:
                    pass
                try:
                    tgt_cell.add(*items)
                except Exception:
                    # 退化情况：无须中断
                    pass

                # 根据原来 src_cell 的引用更新目标单元的引用
                tgt_cell.value_bg = getattr(src_cell, "value_bg", None)
                tgt_cell.value_text = getattr(src_cell, "value_text", None)

                # 清理源单元的引用
                src_cell.value_bg = None
                src_cell.value_text = None

        # 更新 front/back 指针：数据从 0 开始，next 插入点为 count
        self.front = 0
        self.back = self.count % self.size

        # 更新指针位置（动画移动至新格子）
        scene.play(
            self.front_label.animate.next_to(self.cells[self.front].rect, UP),
            #self.back_label.animate.next_to(self.cells[self.back].rect, UP),
            run_time=0.4,
        )

    def mark_wasted_space(self, scene: Scene, count: int = 3, label: str = "wasted space", color=ORANGE):
        """
        在队列最左侧的前 `count` 个格子上方放置一个大括号（Brace）和可选标签，表示数组中被浪费的空间。

        参数:
            scene: 当前 Scene
            count: 要覆盖的格子数（从索引 0 开始）
            label: 要显示的标签文字，传入空字符串则不显示标签
            color: 大括号颜色

        示例:
            queue.mark_wasted_space(self, 3, "wasted space")
        """
        count = max(0, min(self.size, int(count)))
        if count == 0:
            return

        # 取出前 count 个单元的矩形用于创建 Brace
        rects = VGroup(*[self.cells[i].rect for i in range(count)])
        brace = Brace(rects, UP, buff=0.25).set_color(color)
        label_mob = None
        animations = [GrowFromCenter(brace)]
        if label:
            label_mob = Text(label, font_size=24).next_to(brace, UP, buff=0.08)
            animations.append(Write(label_mob))

        scene.play(*animations)

        # 保存引用以便后续清理或移动
        self.waste_brace = brace
        self.waste_label = label_mob

    def clear_wasted_space(self, scene: Scene):
        """
        清除之前创建的表示浪费空间的大括号与标签（如果存在）。
        """
        animations = []
        if getattr(self, "waste_brace", None):
            animations.append(FadeOut(self.waste_brace))
        if getattr(self, "waste_label", None):
            animations.append(FadeOut(self.waste_label))

        if animations:
            scene.play(*animations)

        self.waste_brace = None
        self.waste_label = None


class ArrayQueueDemo(Scene):
    """演示：数组队列入队出队过程"""
    def construct(self):
        queue = ArrayQueue(size=6).shift(LEFT * 3)
        self.play(FadeIn(queue))
        self.wait(0.7)

        

        queue.enqueue(self, 1)
        queue.enqueue(self, 2)
        queue.enqueue(self, 3)
        
        self.wait(1)
        queue.dequeue(self)

        #把数据提前到头
        queue.compact_front(self)


        queue.enqueue(self, 4)
        self.wait(1)
        queue.dequeue(self)
        queue.enqueue(self, 5)
        queue.enqueue(self, 6)
        queue.dequeue(self)
        queue.dequeue(self)
        queue.enqueue(self, 7)

        queue.mark_wasted_space(self, 3, "bbbb")

        self.wait(1.5)
