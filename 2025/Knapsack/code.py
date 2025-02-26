from manimlib import *

PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"

class Knapsack(Scene):

    def construct(self):


        knapsack = ImageMobject("knapsack.png").to_edge(DOWN).scale(0.8).shift(DOWN*0.4).set_z_index(1)
        self.play(GrowFromCenter(knapsack))
        self.wait(2)

        red = ImageMobject("red.png").scale(0.58).next_to(knapsack, UP, buff=1)
        teal = ImageMobject("teal.png").scale(0.58).next_to(red, LEFT, buff=0.78)
        brown = ImageMobject("brown.png").scale(0.58).next_to(red, RIGHT, buff=0.78)
        blue = ImageMobject("blue.png").scale(0.58).next_to(teal, LEFT, buff=0.78)
        yellow = ImageMobject("yellow.png").scale(0.58).next_to(brown, RIGHT, buff=0.78)
        self.play(GrowFromCenter(red), GrowFromCenter(teal), GrowFromCenter(brown), GrowFromCenter(blue), GrowFromCenter(yellow))
        self.wait(3)


        profit = Text("Profit = 0").set_color(BLACK).next_to(knapsack, LEFT, buff=0.7)
        weight = Text("Weight = 9").set_color(BLACK).next_to(knapsack, RIGHT, buff=0.7)
        self.play(Write(weight))
        self.wait(2)
        self.play(Write(profit))
        self.wait(2)



        self.play(Indicate(red))

        self.play(red.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 70").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 5").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait()

        self.play(Indicate(teal))
        self.play(teal.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 130").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 2").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)

        self.play(Indicate(yellow))
        self.play(yellow.animate.move_to(knapsack).scale(0.00001))
        self.wait()
        self.play(profit.animate.become(Text("Profit = 160").set_color(BLACK).move_to(profit)), run_time=0.5)
        self.wait()
        self.play(weight.animate.become(Text("Weight = 0").set_color(BLACK).move_to(weight)), run_time=0.5)
        self.wait(1)





        self.wait(2)

