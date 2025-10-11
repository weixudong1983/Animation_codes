from manim import *

class DP1(Scene):
    def construct(self):
        title = Text("斐波那契数列", font_size=48).to_edge(UP).shift(DOWN*0.3).set_color(GREEN)
        self.play(Write(title))
        self.wait(1)

        fib = Text("0, 1, 1, 2, 3, 5, 8 ...", font_size=36)
        self.play(Write(fib[:3]))
        self.wait(1)

        brace = Brace(fib[:3], DOWN, buff=0.38)
        self.play(GrowFromCenter(brace))
        self.wait(2)

        self.play(Write(fib[3:5]))
        self.wait(1)

        self.play(brace.animate.become(Brace(fib[2:5], DOWN, buff=0.38)))
        self.play(Write(fib[5:7]))
        self.wait(2)

        self.play(brace.animate.become(Brace(fib[4:7], DOWN, buff=0.38)))
        self.play(Write(fib[7:9]))
        self.wait(2)

        self.play(FadeOut(brace), Write(fib[9:]))
        self.wait(2)

        self.play(fib.animate.shift(UP*0.8))

        formula = Text("F(n) = F(n-1) + F(n-2)", font_size=36).next_to(fib, DOWN).shift(DOWN)
        self.play(Write(formula))

        base_case = Text("F(0) = 0, F(1) = 1", font_size=36).next_to(formula, DOWN).shift(DOWN*0.6)
        self.play(Write(base_case))
        self.wait(2)


PURE_RED = "#FF0000"
PURE_BLUE = "#0000FF"
PURE_GREEN = "#00FF00"


class DP2(MovingCameraScene):
    def construct(self):
        code = Text("""
int fib(int n) { 
    if (n <= 1) 
        return n; 
    return fib(n-1) + fib(n-2);    
}
""", font_size=24, t2c={
            "int": ORANGE,
            "fib": PURE_RED,
            "return": ORANGE,
            "if": ORANGE,
        })
        
        self.play(Write(code[:10]))
        self.wait(2)
        self.play(Write(code[10:17]))
        self.wait(2)
        self.play(Write(code[17:24]))
        self.wait(2)
        self.play(Write(code[24:]))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*14).scale(1.2).shift(DOWN), FadeOut(code))

        first = Text("f(5)", font_size=36, t2c={"f": PURE_RED}).shift(RIGHT*14).to_edge(UP).shift(DOWN*0.3)
        self.play(Write(first))

        second = Text("f(4)", font_size=36, t2c={"f": PURE_RED}).shift(RIGHT*14).to_edge(UP).shift(DOWN*2.2+LEFT*3.9)
        third = Text("f(3)", font_size=36, t2c={"f": PURE_RED}).shift(RIGHT*14).to_edge(UP).shift(DOWN*2.2+RIGHT*3.9)
        self.play(GrowFromCenter(second), GrowFromCenter(third))
        
        line1 = Line(first.get_bottom(), second[2].get_top()+UP*0.1)
        line2 = Line(first.get_bottom(), third[2].get_top()+UP*0.1)
        self.play(Create(line1), Create(line2))
        
        fourth = Text("f(2)", font_size=36, t2c={"f": PURE_RED}).next_to(second, DOWN).shift(LEFT*2+DOWN*1.4)
        fifth = Text("f(3)", font_size=36, t2c={"f": PURE_RED}).next_to(second, DOWN).shift(RIGHT*2+DOWN*1.4)
        self.play(GrowFromCenter(fourth), GrowFromCenter(fifth))
        
        line3 = Line(second.get_bottom(), fourth[2].get_top()+UP*0.1)     
        line4 = Line(second.get_bottom(), fifth[2].get_top()+UP*0.1)
        self.play(Create(line3), Create(line4))
        
        sixth = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(third, DOWN).shift(LEFT*1.7+DOWN*1.4)
        seventh = Text("f(2)", font_size=36, t2c={"f": PURE_RED}).next_to(third, DOWN).shift(RIGHT*1.7+DOWN*1.4)
        self.play(GrowFromCenter(sixth), GrowFromCenter(seventh))
        
        line5 = Line(third.get_bottom(), sixth[2].get_top()+UP*0.1)
        line6 = Line(third.get_bottom(), seventh[2].get_top()+UP*0.1)
        self.play(Create(line5), Create(line6))
        
        eighth = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(fourth, DOWN).shift(LEFT*1.2+DOWN*1)
        ninth = Text("f(2)", font_size=36, t2c={"f": PURE_RED}).next_to(fourth, DOWN).shift(RIGHT*0.9+DOWN*1)
        self.play(GrowFromCenter(eighth), GrowFromCenter(ninth))
        
        line7 = Line(fourth.get_bottom(), eighth[2].get_top()+UP*0.1)
        line8 = Line(fourth.get_bottom(), ninth[2].get_top()+UP*0.1)
        self.play(Create(line7), Create(line8))
        
        tenth = Text("f(0)", font_size=36, t2c={"f": PURE_RED}).next_to(ninth, DOWN).shift(LEFT*1+DOWN*0.8)
        eleventh = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(ninth, DOWN).shift(RIGHT*0.7+DOWN*0.8)
        
        line9 = Line(ninth.get_bottom(), tenth[2].get_top()+UP*0.1)
        line10 = Line(ninth.get_bottom(), eleventh[2].get_top()+UP*0.1)
        
        twelfth = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(fifth, DOWN).shift(LEFT*1.2+DOWN*1)
        thirteenth = Text("f(2)", font_size=36, t2c={"f": PURE_RED}).next_to(fifth, DOWN).shift(RIGHT*0.9+DOWN*1)
        
        line11 = Line(fifth.get_bottom(), twelfth[2].get_top()+UP*0.1)
        line12 = Line(fifth.get_bottom(), thirteenth[2].get_top()+UP*0.1)
        
        fourteenth = Text("f(0)", font_size=36, t2c={"f": PURE_RED}).next_to(thirteenth, DOWN).shift(LEFT*1+DOWN*0.8)
        fifteenth = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(thirteenth, DOWN).shift(RIGHT*0.7+DOWN*0.8)
        
        line13 = Line(thirteenth.get_bottom(), fourteenth[2].get_top()+UP*0.1)
        line14 = Line(thirteenth.get_bottom(), fifteenth[2].get_top()+UP*0.1)
        
        sixteenth = Text("f(0)", font_size=36, t2c={"f": PURE_RED}).next_to(seventh, DOWN).shift(LEFT*1+DOWN*0.8)
        seventeenth = Text("f(1)", font_size=36, t2c={"f": PURE_RED}).next_to(seventh, DOWN).shift(RIGHT*0.7+DOWN*0.8)
        
        line15 = Line(seventh.get_bottom(), sixteenth[2].get_top()+UP*0.1)
        line16 = Line(seventh.get_bottom(), seventeenth[2].get_top()+UP*0.1)
        
        self.play(GrowFromCenter(sixteenth), GrowFromCenter(seventeenth), GrowFromCenter(fourteenth), 
                  GrowFromCenter(fifteenth), GrowFromCenter(twelfth), GrowFromCenter(thirteenth),
                  GrowFromCenter(tenth), GrowFromCenter(eleventh))
        self.play(Create(line15), Create(line16), Create(line13), Create(line14), 
                  Create(line11), Create(line12), Create(line9), Create(line10))

        self.wait(2)

        a = Ellipse(width=1.5, height=1, stroke_width=9).move_to(third).scale(1.6).set_color(PURE_GREEN)
        b = Ellipse(width=1.5, height=1, stroke_width=9).move_to(fifth).scale(1.6).set_color(PURE_GREEN)
        self.play(Create(b), Create(a))
        self.wait(2)

        c, d = a.copy(), b.copy()

        self.play(b.animate.move_to(fourth),
                  a.animate.move_to(seventh),
                  c.animate.move_to(thirteenth),
                  d.animate.move_to(ninth))
        self.wait(2)

        self.play(Uncreate(a), Uncreate(b), Uncreate(c), Uncreate(d))
        self.wait()

        self.play(self.camera.frame.animate.shift(LEFT*3))

        brace = Brace(VGroup(first, tenth), LEFT, buff=0.7).shift(LEFT)
        self.play(GrowFromCenter(brace))
        comp = MathTex("O(2^n)").next_to(brace, LEFT).shift(LEFT*0.5).scale(1.44)
        self.play(Write(comp))
        self.wait(2)

        self.play(FadeOut(brace), FadeOut(comp), self.camera.frame.animate.shift(RIGHT*3))

        self.play(self.camera.frame.animate.scale(1.2).shift(DOWN*1.2))

        array = Array(array_size=6).next_to(fifteenth, DOWN).shift(DOWN*0.4+RIGHT*0.3)

        array.append_element(self, "-1")
        array.append_element(self, "-1")
        array.append_element(self, "-1")
        array.append_element(self, "-1")
        array.append_element(self, "-1")
        array.append_element(self, "-1")

        self.wait(2)

        self.play(Create(array), *[Create(array.square_contents[i]) for i in range(6)])
        self.wait(2)

        a = Ellipse(width=1.5, height=1, stroke_width=9).move_to(first).scale(1.6).set_color(PURE_GREEN)
        self.play(Create(a), self.camera.frame.animate.shift(UP*0.3))
        self.wait(1)

        self.play(array.square_contents[4][0].animate.set_fill(GREEN))
        self.wait(1)

        self.play(a.animate.move_to(third), array.square_contents[4][0].animate.set_fill(YELLOW), 
                  self.camera.frame.animate.shift(DOWN*0.3))
        self.play(array.square_contents[3][0].animate.set_fill(GREEN))
        self.wait(2)

        self.play(a.animate.move_to(sixth), array.square_contents[3][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[1][0].animate.set_fill(GREEN))
        self.wait(1)

        self.play(array.square_contents[1][1].animate.become(Text("1", color=BLACK, font_size=36).move_to(array.square_contents[1])))
        self.play(array.square_contents[1][0].animate.set_fill(YELLOW))
        
        self.play(a.animate.move_to(third))
        self.play(a.animate.move_to(seventh))
        self.play(array.square_contents[2][0].animate.set_fill(GREEN))
        self.wait(1)

        self.play(a.animate.move_to(sixteenth).scale(0.85), array.square_contents[2][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[0][0].animate.set_fill(GREEN))
        self.wait(1)
        
        self.play(array.square_contents[0][1].animate.become(Text("0", color=BLACK, font_size=36).move_to(array.square_contents[0][1])))
        self.play(array.square_contents[0][0].animate.set_fill(YELLOW))
        self.wait(1)

        self.play(a.animate.move_to(seventeenth))
        self.play(array.square_contents[1][0].animate.set_fill(BLUE))
        self.wait(1)

        self.play(a.animate.move_to(seventh).scale(1/0.85), array.square_contents[1][0].animate.set_fill(YELLOW))
        self.play(array.square_contents[2][0].animate.set_fill(BLUE))
        self.wait(1)

        self.play(array.square_contents[2][1].animate.become(Text("1", color=BLACK, font_size=36).move_to(array.square_contents[2][1])))
        self.play(array.square_contents[2][0].animate.set_fill(YELLOW))
        self.wait(1)
        
        self.play(a.animate.move_to(third))
        self.play(array.square_contents[3][0].animate.set_fill(BLUE))
        self.wait(1)
        
        self.play(array.square_contents[3][1].animate.become(Text("2", color=BLACK, font_size=36).move_to(array.square_contents[3][1])))
        self.play(array.square_contents[3][0].animate.set_fill(YELLOW))
        self.wait(1)

        self.play(a.animate.move_to(first), self.camera.frame.animate.shift(UP*0.3))
        self.play(array.square_contents[5][0].animate.set_fill(GREEN))
        self.wait()
        
        self.play(a.animate.move_to(second), self.camera.frame.animate.shift(DOWN*0.3), 
                  array.square_contents[5][0].animate.set_fill(YELLOW))
        self.wait(1)

        self.play(array.square_contents[4][0].animate.set_fill(GREEN))
        self.wait()

        b = a.copy()

        self.play(a.animate.move_to(fourth), b.animate.move_to(fifth), 
                  array.square_contents[4][0].animate.set_fill(YELLOW))

        self.play(array.square_contents[3][0].animate.set_fill(BLUE), 
                  array.square_contents[2][0].animate.set_fill(BLUE))
        self.wait(2)

        self.play(a.animate.move_to(second), b.animate.move_to(second), 
                  array.square_contents[3][0].animate.set_fill(YELLOW), 
                  array.square_contents[2][0].animate.set_fill(YELLOW), 
                  array.square_contents[4][0].animate.set_fill(BLUE))
        self.remove(b)
        self.wait(1)

        self.play(array.square_contents[4][1].animate.become(Text("3", color=BLACK, font_size=36).move_to(array.square_contents[4][1])))
        self.play(array.square_contents[4][0].animate.set_fill(YELLOW))
        self.wait(2)

        self.play(a.animate.move_to(first), self.camera.frame.animate.shift(UP*0.3))
        self.play(array.square_contents[5][0].animate.set_fill(BLUE))
        self.wait(1)
        
        self.play(array.square_contents[5][1].animate.become(Text("5", color=BLACK, font_size=36).move_to(array.square_contents[5][1])))
        self.play(array.square_contents[5][0].animate.set_fill(YELLOW), 
                  self.camera.frame.animate.shift(DOWN*0.3), FadeOut(a))
        self.wait(3)

        self.play(self.camera.frame.animate.shift(LEFT*1.8))

        arrow = Arrow(UP*3, DOWN*7, stroke_width=9).next_to(fourth, LEFT).set_color(ORANGE).shift(DOWN*0.85+LEFT*2.6)
        self.play(GrowArrow(arrow))
        self.wait(2)

        # 清理所有对象
        all_objects = [arrow, array, *[array.square_contents[i] for i in range(6) if array.square_contents[i] is not None],
                       first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, tenth,
                       eleventh, twelfth, thirteenth, fourteenth, fifteenth, sixteenth, seventeenth,
                       line1, line2, line3, line4, line5, line6, line7, line8, line9,
                       line10, line11, line12, line13, line14, line15, line16]
        
        self.play(FadeOut(Group(*all_objects)), FadeIn(code),
                  self.camera.frame.animate.shift(UP).shift(LEFT*14).scale(1/1.2).scale(1/1.2).shift(RIGHT*2+UP))
        self.wait(2)

        text = Text("""
int fib(int n, vector<int>& dp) {
    if (dp[n] != -1) {
        return dp[n];
    }
    
    if (n <= 1) {  
        dp[n] = n; 
        return dp[n];
    }

    dp[n] = fib(n - 1, dp) + fib(n - 2, dp); 
    return dp[n];
}

int main() {
    int n = 5;
    vector<int> dp(n + 1, -1);  
    cout << fib(n, dp) << endl; 
    return 0;
}
""", font_size=20, t2c={
            "int": ORANGE,
            "fib": PURE_RED,
            "return": ORANGE,
            "if": ORANGE,
            "vector": ORANGE,
            "cout": YELLOW_E,
            "main": ORANGE,
        }).move_to(code).shift(DOWN*0.25)

        self.play(FadeOut(code), Write(text[:13]))
        self.wait(2)
        self.play(Write(text[12:36]))
        self.wait(2)
        self.play(Write(text[36:61]))
        self.wait(2)
        self.play(Write(text[61:90]))
        self.wait(2)
        self.play(Write(text[90:101]))
        self.wait(2)
        self.play(Write(text[101:104]))
        self.wait(2)
        self.play(Write(text[104:117]))
        self.wait(2)
        self.play(Write(text[117:]))
        self.wait(2)


class DP_TABULATION(MovingCameraScene):
    def construct(self):
        text = Text("fib(5)", font_size=48, t2c={"fib": PURE_RED}).to_edge(UP).shift(DOWN*0.5)
        self.play(Create(text))

        array = Array(array_size=6).shift(DOWN*0.82)
        array.append_element(self, "0")
        array.append_element(self, "0")
        array.append_element(self, "0")
        array.append_element(self, "0")
        array.append_element(self, "0")
        array.append_element(self, "0")
        self.wait(2)

        self.play(Create(array), *[Create(array.square_contents[i]) for i in range(6)])
        self.wait(2)

        self.play(array.square_contents[0][0].animate.set_fill(BLUE))
        self.wait(2)
        self.play(array.square_contents[0][0].animate.set_fill(YELLOW))
        self.wait(1)
        self.play(array.square_contents[1][0].animate.set_fill(BLUE))
        self.wait(1)
        self.play(array.square_contents[1][1].animate.become(Text("1", color=BLACK, font_size=36).move_to(array.square_contents[1])))
        self.wait()
        self.play(array.square_contents[1][0].animate.set_fill(YELLOW))
        self.wait(1)

        i = Text("i", font_size=36).next_to(array.square_contents[2], DOWN, buff=0.66)
        self.play(Write(i))
        self.wait()
        
        self.play(array.square_contents[2][0].animate.set_fill(BLUE))
        brace = Brace(VGroup(array.square_contents[1], array.square_contents[0]), UP, buff=0.38)
        self.play(GrowFromCenter(brace))
        self.wait()
        
        self.play(array.square_contents[2][1].animate.become(Text("1", color=BLACK, font_size=36).move_to(array.square_contents[2])))
        self.play(array.square_contents[2][0].animate.set_fill(YELLOW))
        self.play(i.animate.next_to(array.square_contents[3], DOWN, buff=0.66))

        self.play(array.square_contents[3][0].animate.set_fill(BLUE))
        self.play(brace.animate.become(Brace(VGroup(array.square_contents[1], array.square_contents[2]), UP, buff=0.38)))
        self.wait()
        
        self.play(array.square_contents[3][1].animate.become(Text("2", color=BLACK, font_size=36).move_to(array.square_contents[3])))
        self.play(array.square_contents[3][0].animate.set_fill(YELLOW))
        self.play(i.animate.next_to(array.square_contents[4], DOWN, buff=0.66))

        self.play(array.square_contents[4][0].animate.set_fill(BLUE))
        self.play(brace.animate.become(Brace(VGroup(array.square_contents[3], array.square_contents[2]), UP, buff=0.38)))
        self.wait(1)
        
        self.play(array.square_contents[4][1].animate.become(Text("3", color=BLACK, font_size=36).move_to(array.square_contents[4])))
        self.play(array.square_contents[4][0].animate.set_fill(YELLOW))
        self.play(i.animate.next_to(array.square_contents[5], DOWN, buff=0.66))

        self.play(array.square_contents[5][0].animate.set_fill(BLUE))
        self.play(brace.animate.become(Brace(VGroup(array.square_contents[4], array.square_contents[3]), UP, buff=0.38)))
        self.wait(1)
        
        self.play(array.square_contents[5][1].animate.become(Text("5", color=BLACK, font_size=36).move_to(array.square_contents[5])))
        self.play(array.square_contents[5][0].animate.set_fill(PINK))

        self.play(FadeOut(i), FadeOut(brace))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*2.3))

        first = Text("fib(0)", font_size=36, t2c={"fib": PURE_RED}).to_edge(DOWN).shift(LEFT*6.3).shift(UP*0.12)
        second = Text("fib(1)", font_size=36, t2c={"fib": PURE_RED}).next_to(first, UP, buff=0.5)
        third = Text("fib(2)", font_size=36, t2c={"fib": PURE_RED}).next_to(second, UP, buff=0.5)
        fourth = Text("fib(3)", font_size=36, t2c={"fib": PURE_RED}).next_to(third, UP, buff=0.5)
        fifth = Text("fib(4)", font_size=36, t2c={"fib": PURE_RED}).next_to(fourth, UP, buff=0.5)
        sixth = Text("fib(5)", font_size=36, t2c={"fib": PURE_RED}).next_to(fifth, UP, buff=0.5)

        self.play(Write(first))
        self.wait()
        self.play(Write(second))
        self.wait()
        self.play(Write(third), Write(fourth), Write(fifth), Write(sixth))
        self.wait(1)

        arrow = Arrow(first.get_bottom(), sixth.get_top(), stroke_width=9).set_color(ORANGE).shift(LEFT*2)
        self.play(GrowArrow(arrow))
        self.wait(2)

        self.play(FadeOut(arrow), FadeOut(first), FadeOut(second), FadeOut(third), 
                  FadeOut(fourth), FadeOut(fifth), FadeOut(sixth),
                  self.camera.frame.animate.shift(LEFT*17))
        self.wait(1)

        code = Text("""
int fib(int n) {
    if (n <= 1)
        return n;
    vector<int> dp(n + 1); 
    dp[0] = 0; 
    dp[1] = 1;
    for (int i = 2; i <= n; i++) {
        dp[i] = dp[i - 1] + dp[i - 2];
    }
    return dp[n];
}
""", font_size=36, t2c={
            "int": ORANGE,
            "fib": PURE_RED,
            "return": ORANGE,
            "if": ORANGE,
            "vector": ORANGE,
            "for": ORANGE,
        }).shift(LEFT*19).shift(LEFT*0.5).scale(1.2)

        self.play(Write(code[:10]))
        self.wait(1)
        self.play(Write(code[10:24]))
        self.wait(2)
        self.play(Write(code[24:36]))
        self.wait(2)
        self.play(Write(code[36:50]))
        self.wait(2)
        self.play(Write(code[50:90]))
        self.wait(2)
        self.play(Write(code[90:]))
        self.wait(2)


class DP4(MovingCameraScene):
    def construct(self):
        title = Text("动态规划", font_size=48).to_edge(UP).shift(DOWN*0.65).set_color(GREEN)
        self.play(Write(title))
        self.wait(1)

        definition = Text("""
        一种问题解决技术，将复杂问题分解为更简单的
        重叠子问题，并存储这些子问题的解决方案，
        重复使用以避免冗余计算。
        """, font_size=24).next_to(title, DOWN)

        self.play(Write(definition))
        self.wait(2)

        first = Text("• 记忆化搜索 (自顶向下)", font_size=36).shift(UP).next_to(definition, DOWN, buff=0.8)
        self.play(Write(first))
        self.wait(2)

        second = Text("• 制表法 (自底向上)", font_size=36).next_to(first, DOWN, buff=0.8)
        self.play(Write(second))
        self.wait(2)

        self.play(FadeOut(VGroup(first, second, definition)))

        first = Text("1. 重叠子问题", font_size=36).next_to(title, DOWN, buff=0.8)
        self.play(Create(first))
        self.wait(2)

        second = Text("2. 最优子结构", font_size=36).move_to(first)
        self.play(ReplacementTransform(first, second))
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*0.7))

        a = Circle(radius=1.5, color=RED, fill_color=RED, fill_opacity=1).next_to(second, DOWN, buff=1.4)
        self.play(GrowFromCenter(a))
        self.wait(2)

        b = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1).next_to(a, LEFT, buff=0)
        c = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1).next_to(a, RIGHT, buff=0)
        d = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1).next_to(a, ORIGIN, buff=0)
        e = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1).next_to(a, UP, buff=0).shift(DOWN*0.5)
        f = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=1).next_to(a, DOWN, buff=0).shift(UP*0.5)

        self.play(
            ReplacementTransform(a.copy(), b),
            ReplacementTransform(a.copy(), c),  
            ReplacementTransform(a.copy(), d),
            ReplacementTransform(a.copy(), e),
            ReplacementTransform(a, f),
        )
        self.wait(2)

        a.set_fill(TEAL)

        self.play(
            b.animate.set_color(TEAL).set_fill(TEAL),
            c.animate.set_color(TEAL).set_fill(TEAL),
            d.animate.set_color(TEAL).set_fill(TEAL),
            e.animate.set_color(TEAL).set_fill(TEAL),
            f.animate.set_color(TEAL).set_fill(TEAL),
        )
        self.wait(2)

        a = Circle(radius=1.5, color=TEAL, fill_color=TEAL, fill_opacity=1).next_to(second, DOWN, buff=1.4).set_color(TEAL)

        self.play(
            ReplacementTransform(b, a),
            ReplacementTransform(c, a),
            ReplacementTransform(d, a),
            ReplacementTransform(e, a),
            ReplacementTransform(f, a),
        )
        self.wait(2)

        self.play(FadeOut(VGroup(a, second, title)), self.camera.frame.animate.shift(RIGHT*13))

        text = Text("""
        1. 斐波那契数列
        2. 最长公共子序列
        3. 0/1背包问题
        4. 矩阵链乘法
        5. 找零钱问题
        6. 爬楼梯问题
        7. 旅行商问题
        """, font_size=36).shift(RIGHT*13+DOWN*0.5)

        self.play(Create(text[:18]))
        self.wait(2)
        self.play(Create(text[18:]))
        self.wait(2)


class OptimisedCode(Scene):
    def construct(self):
        code = Text("""
int fib(int n) {
    if (n <= 1)
        return n;
    
    int prev2 = 0;  
    int prev1 = 1;  
    
    for (int i = 2; i <= n; i++) {
        int current = prev1 + prev2;  
        prev2 = prev1;  
        prev1 = current; 
    }
    
    return prev1;  
}
        """, font_size=24, t2c={
            "int": ORANGE,
            "fib": PURE_RED,
            "return": ORANGE,
            "if": ORANGE,
            "for": ORANGE,
        })

        self.play(Create(code))

        rect = SurroundingRectangle(code[:10], color=PURE_GREEN, stroke_width=7).scale(1.2)
        self.play(Create(rect))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[10:24], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[24:38], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)
        
        self.play(Transform(rect, SurroundingRectangle(code[38:57], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)
        
        self.play(Transform(rect, SurroundingRectangle(code[57:76], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[76:100], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[100:], color=PURE_GREEN, stroke_width=7).scale(1.2)))
        self.wait(2)

        self.play(Uncreate(rect))
        self.wait(2)


class Array(VGroup):
    def __init__(self, array_size=5, **kwargs):
        super().__init__(**kwargs)
        self.array_size = array_size
        self.square_contents = [None] * array_size
        self.array_group = self.create_array()
        self.add(self.array_group)

    def create_element(self, text):
        square = Square(side_length=1.42, fill_opacity=1, fill_color=BLACK, color=GREEN).set_color(GREEN)
        text = Text(text, font_size=44, color=BLACK).set_color(BLACK)
        return VGroup(square, text)

    def create_array(self):
        squares = VGroup(*[Square(side_length=1.42, color=PURE_RED, stroke_width=6).set_color(GREEN) for _ in range(self.array_size)])
        squares.arrange(RIGHT, buff=0)
        return VGroup(squares)

    def append_element(self, scene, value):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.42, fill_opacity=1, fill_color=YELLOW, color=GREEN, stroke_width=6)
                number = Text(str(value), color=BLACK, font_size=36).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def add_element(self, scene, value, color=YELLOW):
        for i, square in enumerate(self.array_group[0]):
            if self.square_contents[i] is None:
                new_square = Square(side_length=1.42, fill_opacity=1, fill_color=color, color=BLACK, stroke_width=6)
                number = Text(str(value), color=BLACK, font_size=50).set_z_index(1).set_color(BLACK)
                new_square1 = VGroup(new_square, number)
                new_square1.move_to(square.get_center())
                self.square_contents[i] = new_square1
                scene.play(FadeIn(new_square1))
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def pop_element(self, scene):
        for i in range(self.array_size - 1, -1, -1):
            if self.square_contents[i] is not None:
                scene.play(FadeOut(self.square_contents[i]))
                self.square_contents[i] = None
                break
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def delete_from_front(self, scene):
        if self.square_contents[0] is not None:
            scene.play(FadeOut(self.square_contents[0]))
            self.square_contents[0] = None
            animations = []
            for i in range(1, self.array_size):
                if self.square_contents[i] is not None:
                    animations.append(
                        self.square_contents[i].animate.move_to(self.array_group[0][i - 1].get_center())
                    )
                    self.square_contents[i - 1] = self.square_contents[i]
                    self.square_contents[i] = None
            if animations:
                scene.play(*animations)
        else:
            scene.play(Indicate(self.array_group, color=RED))

    def create_new_array(self, scene, new_size):
        new_array = Array(array_size=new_size)
        new_array.next_to(self, DOWN, buff=0.7)
        scene.play(Create(new_array))
        return new_array

    def transfer_elements_to_new_array(self, scene, new_array):
        for i, content in enumerate(self.square_contents):
            if content is not None:
                scene.play(Transform(content, new_array.array_group[0][i]))
                new_array.square_contents[i] = content
                self.square_contents[i] = None