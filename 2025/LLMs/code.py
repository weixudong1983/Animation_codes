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

 
