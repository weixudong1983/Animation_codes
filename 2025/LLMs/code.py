from manimlib import *
import itertools as it




class Example(Scene):

    def construct(self):
        
        llm = Text("Language Models -> Text -> GPT-3").set_color(BLACK).shift(UP*2.68)
        images = Text("Images -> Dall-3").set_color(BLACK).next_to(llm,DOWN, buff=0.7)
        videos = Text("Videos -> Sora").set_color(BLACK).next_to(images,DOWN, buff=0.7)
        audio = Text("Audio -> Whisper").set_color(BLACK).next_to(videos,DOWN, buff=0.7)
        mm = Text("Multimodel Models-> Gemini").set_color(BLACK).next_to(audio,DOWN, buff=0.7)
        self.play(ShowCreation(llm))
        self.wait(2)
        self.play(ShowCreation(images))
        self.wait(2)            
        self.play(ShowCreation(videos))
        self.wait(2)
        self.play(ShowCreation(audio))
        self.wait(2)
        self.play(ShowCreation(mm)) 
        self.wait(2)






class LLM(Scene):

    def construct(self):
        text = Text("Large Language Models").set_color(BLACK).to_edge(UP).shift(DOWN * 0.4).scale(1.33)
        self.play(Write(text))
        self.wait()

        gpt = ImageMobject("gpt.png").scale(0.7).shift(LEFT * 2 + UP * 0.2)
        deepseek = ImageMobject("deepseek.png").scale(0.61).next_to(gpt, RIGHT).shift(RIGHT * 0.6)
        gemini = ImageMobject("gemini.png").next_to(gpt, DOWN).scale(0.74).shift(UP * 0.93)
        meta = ImageMobject("meta.png").scale(0.6).next_to(deepseek, DOWN).shift(LEFT * 0.22)
        gpt_text = Text("chatGPT").set_color(BLACK).next_to(gpt, LEFT)
        gemini_text = Text("Gemini").set_color(PURPLE_E).next_to(gemini, LEFT)
        deepseek_text = Text("DeepSeek").set_color("#0000FF").next_to(deepseek, RIGHT).shift(LEFT * 0.25)
        meta_text = Text("Llama").set_color(GREY_D).next_to(meta, RIGHT).shift(RIGHT * 0.25)

        self.play(GrowFromCenter(gpt), run_time=0.66)
        self.play(ShowCreation(gpt_text), run_time=0.66)

        self.play(GrowFromCenter(deepseek), run_time=0.66)
        self.play(ShowCreation(deepseek_text), run_time=0.66)

        self.play(GrowFromCenter(gemini), run_time=0.66)
        self.play(ShowCreation(gemini_text), run_time=0.66)

        self.play(GrowFromCenter(meta), run_time=0.66)
        self.play(ShowCreation(meta_text), run_time=0.66)

        self.wait(2)

        text1 = Text("Closed Source LLMs").set_color(BLACK).to_edge(UP).shift(DOWN * 0.4).scale(1.33)

        self.play(ReplacementTransform(text, text1),
                  FadeOut(Group(deepseek, deepseek_text, meta_text, meta)),
                  Group(gpt, gpt_text, gemini, gemini_text).animate.shift(RIGHT * 3.1))

        self.wait(2)

        text = Text("Open Source LLMs").set_color(BLACK).to_edge(UP).shift(DOWN * 0.4).scale(1.33)

        self.play(FadeOut(Group(gpt, gpt_text, gemini, gemini_text)))

        self.play(ReplacementTransform(text1, text),
                  Group(deepseek, deepseek_text, meta_text, meta).animate.shift(LEFT * 3),
                  )

        self.wait(2)


class LLM1(Scene):

    def construct(self):
        a1 = (
            RoundedRectangle(stroke_width=50, fill_opacity=1, width=3)
            .set_fill(GREEN, opacity=1)  # Fully opaque fill
            .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
            .scale(0.77)
            .shift(LEFT * 3 + DOWN * 0.5)
        )

        text = Text("LLM", font=BOLD).set_color(BLACK).move_to(a1).scale(1.37)
        a = VGroup(a1, text).shift(RIGHT * 3 + UP * 2.37)
        self.play(GrowFromCenter(a))

        self.wait(2)

        book = ImageMobject("book.png").scale(0.7).shift(DOWN * 1.9 + LEFT * 4.3)
        wikipedia = ImageMobject("wikipedia.png").scale(0.7).next_to(book, RIGHT, buff=0.7).shift(RIGHT * 0.3)
        website = ImageMobject("website.png").scale(0.78).next_to(wikipedia, RIGHT, buff=0.7).shift(RIGHT * 1)

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

        text = Text("""What is Deep Learning?""").set_color(BLACK).next_to(a, DOWN, buff=0.7).shift(DOWN * 2).scale(1.4)
        self.play(Write(text))
        self.wait(2)

        self.play(text.animate.move_to(a).scale(0.000001),
                  self.camera.frame.animate.shift(DOWN * 0.4))
        self.wait()

        text = Text("Deep learning is a type of AI that uses ").set_color(BLACK).scale(0.8)
        text1 = Text("multi-layered neural networks to learn").set_color(BLACK).scale(0.8)
        text2 = Text("patterns from data. It powers tasks").set_color(BLACK).scale(0.8)
        text3 = Text("like image recognition and language").set_color(BLACK).scale(0.8)
        text4 = Text("processing, improving with more data").set_color(BLACK).scale(0.8)
        text5 = Text("and computation.").set_color(BLACK).scale(0.8)

        # Arrange in a vertical stack
        grouped_text = VGroup(text, text1, text2, text3, text4, text5).arrange(DOWN, buff=0.2).scale(0.9).next_to(a,
                                                                                                                  DOWN).shift(
            DOWN * 0.77)

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


class LLM2(Scene):

    def construct(self):
        background = Rectangle(
            width=100, height=100, color="#ECE7E2", fill_color="#ECE7E2", fill_opacity=1
        )
        background.move_to(ORIGIN)
        self.add(background)

        brain1 = ImageMobject('brain_1.png')
        brain2 = ImageMobject('brain_2.png')
        baby = ImageMobject('baby.png').scale(1.25)

        self.play(GrowFromCenter(baby))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT * 4.5))

        brain1.next_to(baby, RIGHT, buff=3).shift(RIGHT * 0.9)
        self.play(GrowFromCenter(brain1))

        arrow = Arrow(start=baby.get_right() + LEFT * 0.8, end=brain1.get_left() + RIGHT * 0.15,
                      stroke_width=6).set_color(BLACK)
        self.play(GrowArrow(arrow))

        self.wait(2)

        brain2.move_to(brain1)

        book = ImageMobject('book.png').scale(0.5).next_to(arrow, UP).shift(UP * 1 + RIGHT * 0.16)
        self.play(GrowFromCenter(book), run_time=0.5)
        self.play(book.animate.move_to(brain1).scale(0.000001))
        ball = ImageMobject('ball.png').scale(0.5).next_to(arrow, DOWN).shift(DOWN * 1 + RIGHT * 0.16)
        self.play(GrowFromCenter(ball), run_time=0.5)
        self.play(ball.animate.move_to(brain1).scale(0.000001))
        school = ImageMobject('school.png').scale(0.4).next_to(arrow, UP).shift(UP * 1 + RIGHT * 0.16)
        self.play(GrowFromCenter(school), run_time=0.5)
        self.play(school.animate.move_to(brain1).scale(0.000001))
        dog = ImageMobject('dog.png').scale(0.5).next_to(arrow, DOWN).shift(DOWN * 1 + RIGHT * 0.16)
        self.play(GrowFromCenter(dog), run_time=0.5)
        self.play(dog.animate.move_to(brain1).scale(0.000001))

        self.wait(2)
        self.play(FadeIn(brain2), FadeOut(brain1))

        self.wait(2)


class LLM3(Scene):

    def construct(self):

        background = Rectangle(
            width=100, height=100, color="#ECE7E2",fill_color="#ECE7E2", fill_opacity=1
        )
        background.move_to(ORIGIN)
        self.add(background)

        a1 = (
            RoundedRectangle(stroke_width=50, fill_opacity=1, width=3)
            .set_fill(BLUE, opacity=1)  # Fully opaque fill
            .set_stroke(BLUE, opacity=0.6)  # 70% opaque stroke
            .scale(0.77)
            .shift(LEFT * 3.5)
        )

        text = Text("LLM", font=BOLD).set_color(BLACK).move_to(a1).scale(1.37)
        a = VGroup(a1, text).shift(LEFT*1.2)
        self.play(GrowFromCenter(a))
        self.wait()

        nn = ImageMobject("nn.png").next_to(a, RIGHT).shift(RIGHT*3.8)

        arrow = Arrow(start=a.get_right()+RIGHT*0.1, end=nn.get_left()+RIGHT*1, stroke_width=8, ).set_color(BLACK)
        self.play(GrowArrow(arrow))
        self.play(GrowFromCenter(nn))

        text = Text("Neural Network").set_color(BLACK).next_to(nn, DOWN).shift(LEFT*0.2)
        self.play(Write(text), self.camera.frame.animate.shift(DOWN*0.45))

        self.wait(3)


        self.play(self.camera.frame.animate.shift(RIGHT*14))

        neural = NeuralNetworkMobject([7,4,2]).shift(RIGHT*15.66).scale(1.3)
        neural.label_inputs("x")
        neural.label_outputs("y")
        neural.label_hidden_layers("h")
        self.play(Write(neural))

        # Create input source object (a circle with "Input" text)
        input_source = Circle(radius=0.5, fill_color=BLACK, fill_opacity=1, stroke_color=YELLOW_E, stroke_width=6)
        input_text = Text("Input", color=BLUE).scale(0.4)
        input_group = VGroup(input_source, input_text).scale(1.4)

        # Position the input source to the left of the neural network
        input_group.next_to(neural.layers[0], LEFT, buff=2).shift(LEFT*0.4)

        # Create connections to each input neuron
        connections = VGroup()
        for neuron in neural.layers[0].neurons:
            connection = Line(
                input_source.get_center(),
                neuron.get_center(),
                stroke_color=GREY,
                stroke_width=2
            ).set_z_index(-2)
            connections.add(connection)

        self.wait(2)

        self.play(self.camera.frame.animate.scale(0.85).shift(UP*0.4))

        # Animation sequence
        self.play(
            GrowFromCenter(input_group)
        )

        neural.set_z_index(1)
        input_group.set_z_index(1)

        # Animate connections appearing simultaneously
        for connection in connections:
            connection.set_stroke(opacity=1).set_z_index(-2)
        self.add(connections)



        # Play all connection animations simultaneously
        self.play(
            ShowCreation(connections[0]),
            ShowCreation(connections[1]),
            ShowCreation(connections[2]),
            ShowCreation(connections[3]),
            ShowCreation(connections[4]),
            ShowCreation(connections[5]),
            ShowCreation(connections[6]),
            run_time=1.5
        )

        self.wait()

        self.play(self.camera.frame.animate.scale(1/0.9))

        arrow = Arrow(start=input_group.get_right(), end=input_group.get_right()+1.75*RIGHT, stroke_width=8).set_color("#0000FF").shift(RIGHT*4+DOWN*3).rotate(PI/2).rotate(PI/4)

        self.play(GrowFromCenter(arrow))
        self.wait()

        self.play(arrow.animate.shift(RIGHT*2+UP))

        self.wait()

        self.play(arrow.animate.rotate(PI/2, about_edge=LEFT).shift(UP*3.2+RIGHT*0.1))
        self.wait()

        self.play(arrow.animate.shift(LEFT*2+UP*1.2))

        self.wait()
        transformer = ImageMobject("transformer.png").shift(RIGHT*28).scale(1.7)
        self.add(transformer)

        self.play(self.camera.frame.animate.shift(RIGHT*14))
        self.play(FadeOut(arrow))


        self.wait(3)











        self.embed()



class  GPU(Scene):

    def construct(self):
        
        gpu = ImageMobject("gpu.png").scale(0.6).shift(LEFT*0.15+UP*0.65)
        data = ImageMobject("data.png").scale(0.6).next_to(gpu, LEFT).shift(LEFT*0.8)
        algo = ImageMobject("algorithms.png").scale(0.6).next_to(gpu, RIGHT).shift(RIGHT)

        self.play(GrowFromCenter(gpu), GrowFromCenter(data), GrowFromCenter(algo))

        gpu_text = Text("GPU").next_to(gpu, DOWN, buff=1).set_color(BLACK)
        data_text = Text("Data").next_to(data, DOWN, buff=1).set_color(BLACK)
        algo_text = Text("Algorithms").next_to(algo, DOWN, buff=1).set_color(BLACK)
        self.play(Write(gpu_text), Write(data_text), Write(algo_text))

        self.wait(2)

        self.play(Indicate(data))
        self.wait()


        # Create number plane with custom config
        axes = NumberPlane(
            x_range=(0, 6, 1),  # Changed to start from 0
            y_range=(0, 4, 1),
            width=12,
            height=8,
            background_line_style={
                "stroke_opacity": 0
            },
            axis_config={
                "stroke_color": BLACK,
                "stroke_width": 4,
                "include_tip": False,
                "color": BLACK,
            }
        ).scale(0.7).shift(LEFT*14)
        
        # Function for converting the x coordinate to year
        def x_to_year(x):
            return 1980 + (x * 10)
        
        # Function for converting the y coordinate to data value
        def y_to_value(y):
            return y * 100

        # Create x-axis labels
        x_labels = VGroup()
        for x in range(0, 6):  # Changed to start from 0
            year = x_to_year(x)
            label = Text(str(year)).scale(0.4).set_color(BLACK)  # Fixed color
            label.next_to(axes.c2p(x, 0), DOWN * 0.5)
            x_labels.add(label)

        # Create y-axis labels
        y_labels = VGroup()
        for y in range(0, 5):
            value = y_to_value(y)
            label = Text(str(value)).scale(0.4).set_color(BLACK)  # Fixed color
            label.next_to(axes.c2p(0, y), LEFT * 0.5)
            y_labels.add(label)

        # Create axis labels
        x_axis_label = Text("Year").scale(0.5).set_color(BLACK)  # Fixed color
        x_axis_label.next_to(axes.c2p(5, 0), RIGHT * 0.5)
        
        y_axis_label = Text("Data (Arbitrary Units)").scale(0.5).set_color(BLACK)  # Fixed color
        y_axis_label.next_to(axes.c2p(0, 4), UP * 0.5)

        # Define exponential growth function
        def exp_growth(x):
            t = x_to_year(x)
            return (np.exp(0.08 * (t - 1980)) - 1) / (np.exp(0.08 * (2025 - 1980)) - 1) * 4

        # Create graph
        graph = axes.get_graph(
            exp_growth,
            x_range=(0, 4.5),  # Changed to start from 0
            color=BLUE_E,  # Keep graph blue
            stroke_width=5
        )


        # Create dot for animation
        dot = Dot().set_color("#FF0000").scale(1.33)  # Fixed color to RED
        dot.move_to(axes.input_to_graph_point(0, graph))  # Changed to start from 0

        # Animation sequence
        self.add(axes)
        x_labels.shift(DOWN*0.37+RIGHT*0.4)
        y_axis_label.shift(UP*0.33)
        x_axis_label.shift(RIGHT*2)
        
        self.play(self.camera.frame.animate.shift(LEFT*14))


        self.play(
            Write(x_labels),
            Write(y_labels),
            Write(x_axis_label),
            Write(y_axis_label)
        )
        self.wait(0.5)
        
        self.play(ShowCreation(graph),)
        self.wait(0.5)

        self.add(dot)
        self.play(MoveAlongPath(dot, graph), run_time=3, rate_func=linear)
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*14))
        self.wait()
        self.play(Indicate(gpu))
        self.play(self.camera.frame.animate.shift(RIGHT*14))

        temp = gpu.copy().shift(RIGHT*11+DOWN*0.9).scale(0.9).shift(LEFT*0.5)
        
        cpu = ImageMobject("cpu.png").move_to(temp)
        self.play(GrowFromCenter(cpu))
        cpu_text = Text("CPU").next_to(cpu, DOWN,).set_color(BLACK).shift(DOWN*0.4)
        self.play(Write(cpu_text))

        # Create a group of squares (each is a "problem" block)
        problem_squares = VGroup(*[
            Rectangle(width=3,height=1, color=BLACK, stroke_width=6, fill_color=YELLOW, fill_opacity=1)
            for _ in range(6)
        ])
        # Arrange them in a vertical stack with a small gap between each
        problem_squares.arrange(DOWN, buff=0)
        # Optionally, move the entire group to the right edge of the frame
        problem_squares.next_to(cpu, RIGHT, buff=4.2)
    
        # Animate the drawing (creation) of the squares
        self.play(ShowCreation(problem_squares))

        for i in range(6):
            label = Text(f"Task {i+1}", font_size=40).set_color(BLACK)
            label.move_to(problem_squares[i].get_center())
            self.play(Write(label), run_time=0.1)
        self.wait(2)

        arrow = Arrow(start=cpu.get_right(), end=problem_squares[0].get_left(), color=BLACK, stroke_width=12)
        self.play(GrowArrow(arrow))
        self.play(problem_squares[0].animate.set_fill(GREEN))

        for i in range(1,6):
            self.play(arrow.animate.become(Arrow(start=cpu.get_right(), end=problem_squares[i].get_left(), color=BLACK, stroke_width=12)), run_time=0.5)
            self.play(problem_squares[i].animate.set_fill(GREEN), run_time=0.5)
        self.wait(2)


        temp_a = []

        for i in range(6):
            temp_a.append(problem_squares[i].animate.set_fill(YELLOW))


        self.play(FadeOut(Group(cpu, arrow)), GrowFromCenter(temp),
                  *[i for i in temp_a])
        
        self.play(Transform(cpu_text, Text("GPU").move_to(cpu_text).set_color(BLACK).shift(UP*0.8)))
        
        self.wait(2)



        # Create curvy arrows from GPU to each task
        curves = []
        for i in range(6):
            # Calculate control points for bezier curve
            start = temp.get_right()
            end = problem_squares[i].get_left()
            
            # Create control points for smooth curve
            control1 = start + RIGHT * 2 + UP * (1 - i * 0.4)
            control2 = end + LEFT * 2 + UP * (1 - i * 0.4)
            
            # Create the curve
            curve = CubicBezier(
                a0=start,
                h0=control1,
                h1=control2,
                a1=end,
                color=BLACK,
                stroke_width=4
            )
            curves.append(curve)

        # Animate the creation of curves
        self.play(*[ShowCreation(curve) for curve in curves])
        self.wait(1)



        # Create flowing dots to represent data/computation
        for _ in range(1):  
            flowing_dots = []
            fading_dots = []
            for curve in curves:
                dot = Dot(radius=0.15).set_color("#00FF00")
                dot.move_to(curve.get_start())  # Use get_start() method
                flowing_dots.append(dot)
                fading_dots.append(FadeOut(dot))

            # Add all dots to scene
            self.add(*flowing_dots)


            # Animate dots along their respective curves
            self.play(
                *[MoveAlongPath(dot, curve) for dot, curve in zip(flowing_dots, curves)],
                run_time=1.5,
                rate_func=linear
            )

            # Change task colors to indicate processing
            self.play(
                *[square.animate.set_fill(GREEN) for square in problem_squares],
                run_time=0.9
            )

            self.play(*fading_dots)
            


        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*14))

        self.wait(1)
        
        self.play(Indicate(algo))

        self.wait()





        self.embed()









class NeuralNetworkMobject(VGroup):
    def __init__(
            self,
            neural_network,
            neuron_radius=0.24,
            neuron_to_neuron_buff=MED_SMALL_BUFF,
            layer_to_layer_buff=1.35,
            output_neuron_color=GREEN,
            input_neuron_color=BLUE,
            hidden_layer_neuron_color=RED,
            neuron_stroke_width=6,
            neuron_fill_color=GREEN,
            edge_color=GREY,
            edge_stroke_width=4,
            edge_propogation_color=YELLOW,
            edge_propogation_time=1,
            max_shown_neurons=16,
            brace_for_large_layers=True,
            average_shown_activation_of_large_layer=True,
            include_output_labels=False,
            arrow=False,
            arrow_tip_size=0.1,
            left_size=1,
            neuron_fill_opacity=1,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.layer_sizes = neural_network
        self.neuron_radius = neuron_radius
        self.neuron_to_neuron_buff = neuron_to_neuron_buff
        self.layer_to_layer_buff = layer_to_layer_buff
        self.output_neuron_color = output_neuron_color
        self.input_neuron_color = input_neuron_color
        self.hidden_layer_neuron_color = hidden_layer_neuron_color
        self.neuron_stroke_width = neuron_stroke_width
        self.neuron_fill_color = neuron_fill_color
        self.edge_color = edge_color
        self.edge_stroke_width = edge_stroke_width
        self.edge_propogation_color = edge_propogation_color
        self.edge_propogation_time = edge_propogation_time
        self.max_shown_neurons = max_shown_neurons
        self.brace_for_large_layers = brace_for_large_layers
        self.average_shown_activation_of_large_layer = average_shown_activation_of_large_layer
        self.include_output_labels = include_output_labels
        self.arrow = arrow
        self.arrow_tip_size = arrow_tip_size
        self.left_size = left_size
        self.neuron_fill_opacity = neuron_fill_opacity

        self.add_neurons()
        self.add_edges()
        self.add_to_back(self.layers)

    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size, index)
            for index, size in enumerate(self.layer_sizes)
        ])
        layers.arrange(RIGHT, buff=self.layer_to_layer_buff)
        self.layers = layers
        if self.include_output_labels:
            self.label_outputs_text([])

    def get_nn_fill_color(self, index):
        if index == -1 or index == len(self.layer_sizes) - 1:
            return self.output_neuron_color
        if index == 0:
            return self.input_neuron_color
        return self.hidden_layer_neuron_color

    def get_layer(self, size, index=-1):
        layer = VGroup()
        n_neurons = min(size, self.max_shown_neurons)
        neurons = VGroup(*[
            Circle(
                radius=self.neuron_radius,
                stroke_color=self.get_nn_fill_color(index),
                stroke_width=self.neuron_stroke_width,
                fill_color=BLACK,
                fill_opacity=self.neuron_fill_opacity,
            )
            for _ in range(n_neurons)
        ])
        neurons.arrange(DOWN, buff=self.neuron_to_neuron_buff)
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = Tex("\\vdots")
            dots.move_to(neurons.get_center())
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)



        return layer

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)

    def get_edge(self, neuron1, neuron2):
        if self.arrow:
            return Arrow(
                neuron1.get_center(),
                neuron2.get_center(),
                buff=self.neuron_radius,
                stroke_color=self.edge_color,
                stroke_width=self.edge_stroke_width,
                tip_length=self.arrow_tip_size
            ).set_z_index(-2)
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff=self.neuron_radius,
            stroke_color=self.edge_color,
            stroke_width=self.edge_stroke_width,
        )

    def label_inputs(self, l):
        self.input_labels = VGroup()
        for n, neuron in enumerate(self.layers[0].neurons):
            label = Tex(f"{l}_{{{n + 1}}}").set_color(WHITE)
            label.set_height(0.3 * neuron.get_height())
            label.move_to(neuron)
            self.input_labels.add(label)
        self.add(self.input_labels)

    def label_outputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = Tex(f"{l}_{{{n + 1}}}").set_color(WHITE)
            label.set_height(0.4 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_outputs_text(self, outputs):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = Tex("?" if n >= len(outputs) else outputs[n]).set_color(WHITE)
            label.set_height(0.75 * neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width() / 2) * RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_hidden_layers(self, l):
        self.hidden_labels = VGroup()
        for layer in self.layers[1:-1]:
            for n, neuron in enumerate(layer.neurons):
                label = Tex(f"{l}_{{{n + 1}}}").set_color(WHITE)
                label.set_height(0.4 * neuron.get_height())
                label.move_to(neuron)
                self.hidden_labels.add(label)
        self.add(self.hidden_labels)





