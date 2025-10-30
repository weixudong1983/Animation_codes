from manim import *


class CodeHighlight:
    def __init__(self, code_string, language="cpp", formatter_style="rrt", 
                 background=None, add_line_numbers=True, 
                 paragraph_config={"font_size": 24, "line_spacing": 0.8}, 
                 scale_factor=0.9, edge_buff=0.5,shift_top=0):
        # 初始化Code对象，封装大部分参数
        self.code_display = Code(
            code_string=code_string,
            language=language,
            #background=background,
            add_line_numbers=add_line_numbers,
            formatter_style=formatter_style,
            paragraph_config=paragraph_config,
        ).scale(scale_factor).to_edge(LEFT, buff=edge_buff)
        if shift_top != 0:
            self.code_display.shift(UP*shift_top)
        print(self.code_display.get_styles_list())
        # 存储Scene引用，用于动画（在add_to_scene时设置）
        self.scene = None

    def add_to_scene(self, scene):
        self.scene = scene
        #self.scene.camera.background_color = WHITE  # 设置背景为白色，匹配friendly样式
        self.scene.play(Write(self.code_display))
        self.scene.wait(1)

    def highlight(self, start, end, color=YELLOW, buff=0.1):
        if self.scene is None:
            raise ValueError("CodeHighlight must be added to a scene first.")
        lines = VGroup(*self.code_display.code_lines[start:end+1])
        box = SurroundingRectangle(lines, color=color, buff=buff, corner_radius=0, stroke_width=3)
        box.shift(UP*0.25)  # 微调位置，避免偏下
        self.scene.play(Create(box))
        self.scene.wait(1)
        self.scene.play(FadeOut(box))
        self.scene.wait(1)