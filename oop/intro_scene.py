from manim import *

class IntroScene(Scene):
    def construct(self):
        title = Text("C++ 面向对象编程", font_size=72, color=BLUE)
        subtitle = Text("封装 · 继承 · 多态", font_size=48, color=YELLOW)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(1)
