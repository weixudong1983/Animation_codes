from manim import *

class PolymorphismScene(Scene):
    def construct(self):
        title = Text("多态与虚函数", font_size=56, color=BLUE)
        code = Code(code="""class Animal {
public:
    virtual void Speak() { cout << "Animal sound" << endl; }
};

class Dog : public Animal {
public:
    void Speak() override { cout << "Woof!" << endl; }
};""", language="cpp", insert_line_no=False, style="monokai", background="rectangle", font="Consolas")
        code.scale(0.6)
        code.next_to(title, DOWN)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(code))
        self.wait(2)
