from manim import *

class InstructionPanel(VGroup):
    """一个独立的指令面板组件，包含指令文本列表和可移动的高亮框。

    用法:
        panel = InstructionPanel(instructions_list, t2c=..., start_index=0)
        panel.add_to_scene(scene)
        panel.next(scene)  # 移动到下一行并播放动画
    """
    def __init__(self, instructions_list, t2c=None, highlight_color=YELLOW, buff=0.1, font_size=28, start_index=0, left_buff=1.5):
        super().__init__()
        self.start_index = start_index
        self.instructions_list = list(instructions_list)
        self.t2c = t2c or {}
        # 创建指令 VGroup
        self.instructions = VGroup(*[Text(instr, font_size=font_size, font="sans-serif", t2c=self.t2c) for instr in self.instructions_list])
        self.instructions.arrange(DOWN, aligned_edge=LEFT)
        self.instructions.to_edge(LEFT, buff=left_buff)
        self.instructions.shift(UP)

        # 高亮框
        self.highlight_box = SurroundingRectangle(self.instructions[self.start_index], color=highlight_color, buff=buff, corner_radius=0, stroke_width=2)

    def add_to_scene(self, scene: Scene):
        scene.add(self.instructions)
        scene.add(self.highlight_box)

    def next(self, scene: Scene, run_time: float = 1.0, wait_time: float = 0.5):
        """把高亮框移动到下一行并播放动画，若已到末尾则不再移动。"""
        if self.start_index + 1 >= len(self.instructions_list):
            return
        self.start_index += 1
        target = self.instructions[self.start_index]
        scene.play(self.highlight_box.animate.move_to(target), run_time=run_time)
        scene.wait(wait_time)