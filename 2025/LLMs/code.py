from manimlib import *

class LLM(Scene):

    def construct(self):
 

        text = Text("Large Language Models").set_color(BLACK).to_edge(UP).shift(DOWN*0.4).scale(1.33)
        self.play(Write(text))
        self.wait()


        gpt = ImageMobject("gpt.png").scale(0.7).shift(LEFT*2+UP*0.2)
        deepseek = ImageMobject("deepseek.png").scale(0.61).next_to(gpt, RIGHT).shift(RIGHT*0.6)
        gemini = ImageMobject("gemini.png").next_to(gpt, DOWN).scale(0.74).shift(UP*0.93)
        meta = ImageMobject("meta.png").scale(0.6).next_to(deepseek, DOWN).shift(LEFT*0.22)
        gpt_text = Text("chatGPT").set_color(BLACK).next_to(gpt, LEFT)
        gemini_text = Text("Gemini").set_color(PURPLE_E).next_to(gemini, LEFT)
        deepseek_text = Text("DeepSeek").set_color("#0000FF").next_to(deepseek, RIGHT).shift(LEFT*0.25)
        meta_text = Text("Llama").set_color(GREY_D).next_to(meta, RIGHT).shift(RIGHT*0.25)

        self.play(GrowFromCenter(gpt), run_time=0.66)
        self.play(ShowCreation(gpt_text), run_time=0.66)

        self.play(GrowFromCenter(deepseek), run_time=0.66)
        self.play(ShowCreation(deepseek_text), run_time=0.66)

        self.play(GrowFromCenter(gemini), run_time=0.66)
        self.play(ShowCreation(gemini_text), run_time=0.66)

        self.play(GrowFromCenter(meta), run_time=0.66)
        self.play(ShowCreation(meta_text), run_time=0.66)

        self.wait(2)

        text1 = Text("Closed Source LLMs").set_color(BLACK).to_edge(UP).shift(DOWN*0.4).scale(1.33)


        self.play(ReplacementTransform(text, text1),
                  FadeOut(Group(deepseek, deepseek_text, meta_text, meta)),
                  Group(gpt, gpt_text, gemini, gemini_text).animate.shift(RIGHT*3.1))

        self.wait(2)

        text = Text("Open Source LLMs").set_color(BLACK).to_edge(UP).shift(DOWN*0.4).scale(1.33)

        self.play(FadeOut(Group(gpt, gpt_text, gemini, gemini_text)))


        self.play(ReplacementTransform(text1, text),
                  Group(deepseek, deepseek_text, meta_text, meta).animate.shift(LEFT*3),
                  )


        self.wait(2)






class LLM1(Scene):

    def construct(self):

        # Create a full-screen rectangle
        background = Rectangle(
            width=100, height=100, color="#ECE7E2",fill_color="#ECE7E2", fill_opacity=1
        )
        background.move_to(ORIGIN)
        self.add(background)

        a1 = (
            RoundedRectangle(stroke_width=50, fill_opacity=1, width=3)
            .set_fill(GREEN, opacity=1)  # Fully opaque fill
            .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
            .scale(0.77)
            .shift(LEFT * 3 + DOWN * 0.5)
        )

        text = Text("LLM", font=BOLD).set_color(BLACK).move_to(a1).scale(1.37)
        a = VGroup(a1, text).shift(RIGHT*3 + UP*2.37)
        self.play(GrowFromCenter(a))

        self.wait(2)

        book = ImageMobject("book.png").scale(0.7).shift(DOWN*1.9+LEFT*4.3)
        wikipedia = ImageMobject("wikipedia.png").scale(0.7).next_to(book, RIGHT, buff=0.7).shift(RIGHT*0.3)
        website = ImageMobject("website.png").scale(0.78).next_to(wikipedia, RIGHT, buff=0.7).shift(RIGHT*1)

        self.play(GrowFromCenter(book))
        self.wait(0.1)
        self.play(GrowFromCenter(wikipedia))
        self.wait(0.1)
        self.play(GrowFromCenter(website))

        self.wait(2)

        self.play(book.animate.move_to(a).scale(0.000001))
        self.play(wikipedia.animate.move_to(a).scale(0.000001))
        self.play(website.animate.move_to(a).scale(0.000001))

        self.wait(2)

        text = Text("""What is Deep Learning?""").set_color(BLACK).next_to(a, DOWN, buff=0.7).shift(DOWN*2).scale(1.4)
        self.play(Write(text))
        self.wait(2)

        self.play(text.animate.move_to(a).scale(0.000001),
                  self.camera.frame.animate.shift(DOWN*0.4))
        self.wait()


        text = Text("Deep learning is a type of AI that uses ").set_color(BLACK).scale(0.8)
        text1 = Text("multi-layered neural networks to learn").set_color(BLACK).scale(0.8)
        text2 = Text("patterns from data. It powers tasks").set_color(BLACK).scale(0.8)
        text3 = Text("like image recognition and language").set_color(BLACK).scale(0.8)
        text4 = Text("processing, improving with more data").set_color(BLACK).scale(0.8)
        text5 = Text("and computation.").set_color(BLACK).scale(0.8)

        # Arrange in a vertical stack
        grouped_text = VGroup(text, text1, text2, text3, text4, text5).arrange(DOWN, buff=0.2).scale(0.9).next_to(a, DOWN).shift(DOWN*0.77)

        # Show the grouped text

        self.play(ReplacementTransform(a.copy(), grouped_text[0][:4]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][4:12]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][12:14]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][14:15]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][15:19]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][19:21]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][21:23]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][23:27]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[0][27:31]), run_time=0.3)

        self.play(ReplacementTransform(a.copy(), grouped_text[1][:5]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[1][5:13]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[1][13:19]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[1][19:27]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[1][27:29]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[1][29:]), run_time=0.3)


        self.play(ReplacementTransform(a.copy(), grouped_text[2][:8]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][8:12]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][12:16]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][16:17]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][17:19]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][19:25]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[2][25:34]), run_time=0.3)


        self.play(ReplacementTransform(a.copy(), grouped_text[3][:4]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[3][4:9]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[3][9:20]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[3][20:23]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[3][23:31]), run_time=0.3)

        self.play(ReplacementTransform(a.copy(), grouped_text[4][:10]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[4][10:11]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[4][11:20]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[4][20:24]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[4][24:28]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[4][28:32]), run_time=0.3)

        self.play(ReplacementTransform(a.copy(), grouped_text[5][:3]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[5][3:-2]), run_time=0.3)
        self.play(ReplacementTransform(a.copy(), grouped_text[5][-2:]), run_time=0.3)

        self.wait(2)
