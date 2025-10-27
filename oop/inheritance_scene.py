from manim import *

class InheritanceScene(Scene):
    def construct(self):
        title = Text("继承与派生类", font_size=56, color=BLUE)
        code = Code(code="""class Enemy {
public:
    int hp;
    void Attack() { cout << "Enemy attacks!" << endl; }
};

class Boss : public Enemy {
public:
    void Attack() { cout << "Boss attacks fiercely!" << endl; }
};""", language="cpp", insert_line_no=False, style="monokai", background="rectangle", font="Consolas")
        code.scale(0.6)
        code.next_to(title, DOWN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(code))
        self.wait(2)
