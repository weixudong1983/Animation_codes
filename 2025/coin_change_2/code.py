from manimlib import *


class Coins1(Scene):

    def construct(self):
        
        coins = Text("coins = [1, 2, 5]").to_edge(UP).shift(DOWN*0.3)
        amount = Text("Target = 5").next_to(coins, DOWN, buff=0.7)

        self.play(ShowCreation(coins))
        self.wait(2)
        self.play(ShowCreation(amount))
        self.wait()
        self.play(self.camera.frame.animate.shift(RIGHT*2.2))
        text = Text("infinite supply").next_to(coins, RIGHT).scale(0.66).set_color(GREEN)
        self.play(ShowCreation(text))

        self.wait(2)

        temp_1 = Text("1, 1, 1, 1, 1").scale(0.9).shift(RIGHT*2)
        temp_2 = Text("1, 1, 1, 2").scale(0.9).next_to(temp_1, DOWN, buff=0.5)
        temp_3 = Text("1, 2, 2").scale(0.9).next_to(temp_2, DOWN, buff=0.5)
        temp_4 = Text("5").scale(0.9).next_to(temp_3, DOWN, buff=0.5)
        self.play(Write(temp_1))
        self.wait(2)

        self.play(Write(temp_2))
        self.wait(2)
        self.play(Write(temp_3))
        self.wait()
        self.play(Write(temp_4))
        self.wait(2)

        brace = Brace(VGroup(temp_1, temp_4), RIGHT, buff=0.5)
        self.play(GrowFromCenter(brace))
        text = Text("4 ways").next_to(brace, RIGHT, buff=0.5)
        self.play(Write(text))

        self.wait(2)










        self.embed()

