from manimlib import *



class DP1(Scene):

    def construct(self):

        title = Text("Fibonacci Sequence").to_edge(UP).scale(1.3).shift(DOWN*0.3).set_color(GREEN)
        self.play(Write(title))

        self.wait(1)

        fib = Text("0, 1, 1, 2, 3, 5, 8 ...")
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

        formula = Text("F(n) = F(n-1) + F(n-2)").next_to(fib, DOWN).shift(DOWN)
        self.play(Write(formula))

        base_case = Text("F(0) = 0, F(1) = 1").next_to(formula, DOWN).shift(DOWN*0.6)
        self.play(Write(base_case))

        self.wait(2)



    
