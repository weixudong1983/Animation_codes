from manim import *


class StackElement(VGroup):
    def __init__(self, value, **kwargs):
        """Stack element box. fill_color can be passed via kwargs or positional arg.

        Example: StackElement(5, fill_color=BLUE)
        """
        super().__init__(**kwargs)
        # allow caller to override via kwargs as well
        fill_color = YELLOW
        if "fill_color" in kwargs:
            fill_color = kwargs.get("fill_color", fill_color)
        self.rect = Rectangle(height=0.5, width=1.08, fill_opacity=1, fill_color=fill_color, color=BLACK)
        text = Text(str(value), font_size=27, color=BLACK)
        self.add(self.rect, text)


class Stack(VGroup):
    def __init__(self, max_size=5, **kwargs):
        super().__init__(**kwargs)
        self.max_size = max_size
        self.elements = []

        # Create the open-top bucket with filled interior
        bucket_width = 1.2
        bucket_height = self.max_size * 0.65

        # Create the filled interior
        bucket_interior = Rectangle(
            width=bucket_width,
            height=bucket_height,
            fill_color=LIGHT_GRAY,
            fill_opacity=0.2,
            stroke_width=0
        )
        bucket_interior.move_to(UP * bucket_height / 2)

        # Create the bucket outline
        bucket_outline = VGroup(
            Line(start=LEFT * bucket_width / 2, end=RIGHT * bucket_width / 2),
            Line(start=LEFT * bucket_width / 2, end=LEFT * bucket_width / 2 + UP * bucket_height),
            Line(start=RIGHT * bucket_width / 2, end=RIGHT * bucket_width / 2 + UP * bucket_height)
        )
        bucket_outline.set_stroke(color=GRAY, opacity=5)

        self.bucket = VGroup(bucket_interior, bucket_outline).shift(DOWN * 2.3)
        self.add(self.bucket)

    def push(self, scene, value, time=1, ):
        #if 5:
        fill_color = YELLOW
        if len(self.elements) > self.max_size:
            fill_color = RED

    # pass fill_color as a keyword argument (don't pass dict as positional)
        new_element = StackElement(value, fill_color=fill_color)
        new_element.next_to(self.bucket, UP)
        scene.play(Create(new_element))

        if self.elements:
            target_position = self.elements[-1].get_top() + UP * 0.29
        else:
            target_position = self.bucket[0].get_bottom() + UP * 0.3

        scene.play(new_element.animate.move_to(target_position), run_time=time)
        self.elements.append(new_element)
        self.add(new_element)

    def pop(self, scene):
        if self.elements:
            popped_element = self.elements.pop()
            self.remove(popped_element)
            scene.play(popped_element.animate.next_to(self.bucket, UP))
            scene.play(FadeOut(popped_element, shift=UP))
        else:
            scene.play(Indicate(self.bucket, color=RED))


class StackAnimation(Scene):



    def construct(self):

        # self.camera.frame.scale(0.6)
        # self.camera.frame.shift(RIGHT*2)
        # self.camera.frame.shift(DOWN*0.23)

        stack = Stack().shift(UP * 0.18)

        self.play(Create(stack))




        self.wait(2)





        self.wait(1)

        stack.push(self, 12)
        stack.push(self, 1)
        stack.push(self, 0)


        self.wait(2)

        stack.pop(self)
        self.wait(1)
        stack.push(self, 0)

