from manim import *

class ClassDefinition(Scene):
    def construct(self):
        title = Text("类与对象的定义", font_size=56, color=BLUE)
        code = Code(code="""class Player {
public:
    string name;
    int hp;

    Player(string n, int h): name(n), hp(h) {}
    void ShowStatus() const {
        cout << name << " HP: " << hp << endl;
    }
};""", language="cpp", insert_line_no=False, style="monokai", background="rectangle", font="Consolas")
        code.scale(0.6)
        code.next_to(title, DOWN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(code))
        self.wait(2)
