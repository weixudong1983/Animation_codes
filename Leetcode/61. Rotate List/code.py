from manimlib import *
PURE_RED = "#FF0000"
PURE_GREEN = "#00FF00"
PURE_BLUE = "#0000FF"



class RotateLinkedList1(Scene):

    def construct(self):

        self.camera.frame.scale(1.1).scale(1.19)
        self.camera.frame.shift(RIGHT*2.42+UP*0.7).scale(1.05)

        a1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("1", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.756).shift(LEFT*5.2)


        b1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.756).shift(LEFT*3.5).next_to(a, RIGHT, buff=2.1)


        c1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("3", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.756).shift(LEFT*3.5).next_to(b, RIGHT, buff=2.1)

        d1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(d1).set_z_index(1).scale(1.37)
        d=VGroup(d1, text).scale(0.756).shift(LEFT*3.5).next_to(c, RIGHT, buff=2.1)


        e1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("5", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(e1).set_z_index(1).scale(1.37)
        e=VGroup(e1, text).scale(0.756).shift(LEFT*3.5).next_to(d, RIGHT, buff=2.1)






        self.play(GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c), GrowFromCenter(d),GrowFromCenter(e))
        self.wait(2)

        arrow = Arrow(a.get_right()+RIGHT*0.18, b.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow1 = Arrow(b.get_right()+RIGHT*0.18, c.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow2 = Arrow(c.get_right()+RIGHT*0.18, d.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow3 = Arrow(d.get_right()+RIGHT*0.18, e.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow4 = arrow3.copy().shift(RIGHT*3.5)
        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3), GrowFromCenter(arrow4))

        self.wait(2)

        head = Text("head").set_color(BLACK).next_to(a, UP).shift(UP*0.72)
        self.play(GrowFromCenter(head))
        self.wait(2) 

        k = Text("k = 2").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(Write(k), FadeOut(head))

        self.wait(2)
        

        self.play(e[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C))
        self.wait(1)

        # Define the semi-circular path for VGroup(e, arrow4)
        start_point = VGroup(e,arrow4).get_center()  # Starting point of the semi-circle
        end_point = VGroup(a,arrow).get_center()  # Ending point of the semi-circle
        semi_circle = ArcBetweenPoints(start_point, end_point, angle=PI/2)  # Semi-circular path

        # Animate VGroup(e, arrow4) along the semi-circular path
        self.play(
            MoveAlongPath(VGroup(e, arrow4), semi_circle),  # Semi-circular motion for e and arrow4
            VGroup(a, b, c, d, arrow, arrow1, arrow2, arrow3).animate.shift(RIGHT * 3.57),  # Shift the rest to the right
            run_time=2  # Adjust run_time for smoother animation
        )
        self.wait(2)


        self.play(d[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C))
        self.wait(1)

        # Define the semi-circular path for VGroup(e, arrow4)
        start_point = VGroup(d,arrow3).get_center()  # Starting point of the semi-circle
        end_point = VGroup(e,arrow4).get_center()  # Ending point of the semi-circle
        semi_circle = ArcBetweenPoints(start_point, end_point, angle=PI/2)  # Semi-circular path

        # Animate VGroup(e, arrow4) along the semi-circular path
        self.play(
            MoveAlongPath(VGroup(d, arrow3), semi_circle),  # Semi-circular motion for e and arrow4
            VGroup(a, b, c, e, arrow, arrow1, arrow2, arrow4).animate.shift(RIGHT * 3.57),  # Shift the rest to the right
            run_time=2  # Adjust run_time for smoother animation
        )
        self.wait(2)

        self.play(e[0].animate.set_fill(GREEN).set_color(GREEN),
                  d[0].animate.set_fill(GREEN).set_color(GREEN))
        
        self.wait(2)

        self.play(Transform(k, Text("k = 7").set_color(BLACK).scale(2).move_to(k)))
        self.wait(2)
        self.play(Transform(k, Text("k = 7 % 5").set_color(BLACK).scale(2).move_to(k)))
        self.wait()
        self.play(Transform(k, Text("k = 2").set_color(BLACK).scale(2).move_to(k)))
        
        self.wait(2)





class RotateLinkedList2(Scene):

    def construct(self):

        self.camera.frame.scale(1.1).scale(1.19)
        self.camera.frame.shift(RIGHT*2.42+UP*0.7).scale(1.05)

        a1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("1", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.756).shift(LEFT*5.2)


        b1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.756).shift(LEFT*3.5).next_to(a, RIGHT, buff=2.1)


        c1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("3", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.756).shift(LEFT*3.5).next_to(b, RIGHT, buff=2.1)

        d1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(d1).set_z_index(1).scale(1.37)
        d=VGroup(d1, text).scale(0.756).shift(LEFT*3.5).next_to(c, RIGHT, buff=2.1)


        e1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("5", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(e1).set_z_index(1).scale(1.37)
        e=VGroup(e1, text).scale(0.756).shift(LEFT*3.5).next_to(d, RIGHT, buff=2.1)






        self.play(GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c), GrowFromCenter(d),GrowFromCenter(e))
        self.wait(2)

        arrow = Arrow(a.get_right()+RIGHT*0.18, b.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow1 = Arrow(b.get_right()+RIGHT*0.18, c.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow2 = Arrow(c.get_right()+RIGHT*0.18, d.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow3 = Arrow(d.get_right()+RIGHT*0.18, e.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow4 = arrow3.copy().shift(RIGHT*3.5)
        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3), GrowFromCenter(arrow4))

        self.wait(2)
 

        k = Text("k = 8").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(Write(k))
        self.wait(2)
        k1 = Text("k = 8 % 5").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(TransformMatchingTex(k, k1), run_time=0.5)
        self.wait(2)
        k = Text("k = 3").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(TransformMatchingTex(k1, k), run_time=0.5)

        self.wait(2)

        self.play(e[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  d[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  c[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C))




        self.wait(2)

        head = Text("head").set_color(BLACK).next_to(a, UP).shift(UP*0.72)
        tail = Text("tail").set_color(BLACK).next_to(e, UP).shift(UP*0.72)
        self.play(GrowFromCenter(tail), GrowFromCenter(head))
        self.wait(2)


        arrow5 = arrow4.copy().set_color("#FF0000").rotate(PI/2).next_to(e, DOWN).shift(DOWN*0.8).scale(1.2)
        self.play(GrowFromCenter(arrow5))
        self.wait(2)

        self.play(arrow5.animate.next_to(d, DOWN).shift(DOWN*0.8))
        self.wait()
        self.play(arrow5.animate.next_to(c, DOWN).shift(DOWN*0.8))
        self.wait(2)
        self.play(FadeOut(VGroup(arrow5, tail)))
        self.wait(2)

        k1 = Text("k = 8").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(TransformMatchingTex(k, k1), run_time=0.5)
        self.play(c[0].animate.set_fill(GREEN).set_color(GREEN),
                  d[0].animate.set_fill(GREEN).set_color(GREEN),
                  e[0].animate.set_fill(GREEN).set_color(GREEN))  

        self.wait(2) 

        self.play(self.camera.frame.animate.shift(DOWN*2.4))

        source_code = r'''
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1       
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":PURE_RED,
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "length":BLACK
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).scale(0.72).next_to(c, DOWN, buff=0.9).shift(DOWN*1.37+RIGHT*0.5).scale(1.18)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)

        rect = SurroundingRectangle(code[:8], color=PURE_BLUE, stroke_width=6.6).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait()

        length = Text("length = 1").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(1.2).shift(RIGHT*2)
        self.play(ShowCreation(length))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[8:17], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        tail = Text("tail").set_color(BLACK).next_to(a, DOWN,buff=0.88)
        self.play(GrowFromCenter(tail))
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[17:32], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[32:46], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(tail.animate.next_to(b, DOWN, buff=0.88))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[46:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(length, color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(length,Text("length = 2").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(1.2).shift(RIGHT*2)))

        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[17:32], color=PURE_BLUE, stroke_width=5).scale(1.1)))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[32:46], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(tail.animate.next_to(c, DOWN, buff=0.88))
        self.play(Transform(rect, SurroundingRectangle(code[46:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(rect, SurroundingRectangle(length, color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(length,Text("length = 3").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(1.2).shift(RIGHT*2)))
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(code[17:32], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(rect, SurroundingRectangle(code[32:46], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(tail.animate.next_to(d, DOWN, buff=0.88))
        self.play(Transform(rect, SurroundingRectangle(code[46:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(rect, SurroundingRectangle(length, color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(length,Text("length = 4").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(1.2).shift(RIGHT*2)))
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(code[17:32], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(rect, SurroundingRectangle(code[32:46], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(tail.animate.next_to(e, DOWN, buff=0.88))
        self.play(Transform(rect, SurroundingRectangle(code[46:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(rect, SurroundingRectangle(length, color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(Transform(length,Text("length = 5").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(1.2).shift(RIGHT*2)))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[17:32], color="#FF0000", stroke_width=5).scale(1.1)))

        self.wait(2)

        self.play(FadeOut(VGroup(rect, code, length)),)

        self.wait()


        source_code = r'''
        k = k % length
        if k == 0:
            return head      
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":PURE_RED,
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "length":BLACK
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).scale(0.72).next_to(c, DOWN, buff=0.9).shift(DOWN*1+RIGHT*0.5).scale(1.18).scale(1.3)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)

        self.play(self.camera.frame.animate.shift(UP*1.6),
                  k1.animate.shift(DOWN*0.3))
        
        self.wait(2)

        rect = SurroundingRectangle(code[:10], color=PURE_BLUE, stroke_width=6.6).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)



        k = Text("k = 8 % 5").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(Transform(k1, k), run_time=0.77)
        self.wait(2)
        k = Text("k = 3").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(ReplacementTransform(k1, k), run_time=0.77)

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[10:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)
        self.play(Uncreate(rect), FadeOut(VGroup(code)), self.camera.frame.animate.shift(UP*1))
        self.wait(2)

        self.play(c[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  d[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  e[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C))
        
        self.wait(2)
        self.play(self.camera.frame.animate.shift(DOWN*2.4),
                  FadeOut(k)
                  )

        
        source_code = r'''
        current = head
        for _ in range(length - k - 1):
            current = current.next      
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":"#FF0000",
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "length":BLACK
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).scale(0.72).next_to(c, DOWN, buff=0.9).shift(DOWN*1+RIGHT*0.5).scale(1.18).scale(1.3).scale(0.8).shift(DOWN*1.2)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)

        rect = SurroundingRectangle(code[:12], color=PURE_BLUE, stroke_width=6.6).scale(1.1)
        self.play(ShowCreation(rect))


        current = Text("current").set_color(BLACK).next_to(a, DOWN,buff=0.88)
        self.play(GrowFromCenter(current))
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[12:36], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[36:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.play(current.animate.next_to(b, DOWN, buff=0.88))

        self.wait(2)

        self.play(FadeOut(VGroup(rect, code,)),)



        source_code = r'''
        new_head = current.next
        current.next = None
        tail.next = head      
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":"#FF0000",
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "length":BLACK
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).scale(0.72).next_to(c, DOWN, buff=0.9).shift(DOWN*1+RIGHT*0.5).scale(1.18).scale(1.3).scale(0.8).shift(DOWN*1.2)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(2)

        rect = SurroundingRectangle(code[:21], color=PURE_BLUE, stroke_width=6.6).scale(1.1)
        self.play(ShowCreation(rect))
        self.wait(2)

        new_head = Text("new_head").set_color(BLACK).next_to(c, DOWN,buff=0.88)
        self.play(GrowFromCenter(new_head))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[21:38], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)


        self.play(VGroup(c,d,e,arrow2, arrow3, arrow4, new_head, tail).animate.shift(UP*1.5),
                  VGroup(head,current,arrow, arrow1, a, b).animate.shift(DOWN*1),
                          VGroup(code, rect).animate.shift(DOWN*0.5))
        
        self.wait(1.5)

        self.play(Transform(rect, SurroundingRectangle(code[38:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)


        

        self.play(VGroup(d,e,c,arrow2, arrow3, arrow4, tail,new_head).animate.shift(LEFT*7).shift(DOWN*0.3),
                  VGroup(a,b,arrow, arrow1, head, current).animate.shift(RIGHT*10.72).shift(UP*2.2).shift(LEFT*0.19))
        
        self.wait(2)

        self.play(VGroup(a,b,c,d,e,arrow,arrow1,arrow2,arrow3,arrow4,new_head).animate.shift(DOWN*2.1),
                  FadeOut(VGroup(head, current, tail, code, rect)),)
        

        self.play(c[0].animate.set_fill(GREEN).set_color(GREEN),
                  d[0].animate.set_fill(GREEN).set_color(GREEN),
                  e[0].animate.set_fill(GREEN).set_color(GREEN))
        
        self.wait(2)





        self.wait(2)





        



 

        self.embed()


class RotateLinkedList3(Scene):

    def construct(self):
        
        self.camera.frame.scale(1.1).scale(1.19)
        self.camera.frame.shift(RIGHT*2.42+UP*0.7).scale(1.05)

        a1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("1", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.756).shift(LEFT*5.2)


        b1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.756).shift(LEFT*3.5).next_to(a, RIGHT, buff=2.1)


        c1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("3", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.756).shift(LEFT*3.5).next_to(b, RIGHT, buff=2.1)

        d1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(d1).set_z_index(1).scale(1.37)
        d=VGroup(d1, text).scale(0.756).shift(LEFT*3.5).next_to(c, RIGHT, buff=2.1)


        e1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("5", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(e1).set_z_index(1).scale(1.37)
        e=VGroup(e1, text).scale(0.756).shift(LEFT*3.5).next_to(d, RIGHT, buff=2.1)






        self.play(GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c), GrowFromCenter(d),GrowFromCenter(e))
        self.wait(2)

        arrow = Arrow(a.get_right()+RIGHT*0.18, b.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow1 = Arrow(b.get_right()+RIGHT*0.18, c.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow2 = Arrow(c.get_right()+RIGHT*0.18, d.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow3 = Arrow(d.get_right()+RIGHT*0.18, e.get_left()+LEFT*0.18, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow4 = arrow3.copy().shift(RIGHT*3.5)
        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3), GrowFromCenter(arrow4))

        self.wait(2)

        k = Text("k = 3").set_color(BLACK).to_edge(UP).shift(DOWN*0.3).scale(2).shift(UP*1.4+2.2*RIGHT)
        self.play(Write(k),)

        self.wait(2)

        self.play(c[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  d[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C),
                  e[0].animate.set_fill(PURPLE_C).set_color(PURPLE_C))
        
        self.wait(2)

        first = VGroup(a,b,c,arrow, arrow1, arrow2).get_center()
        second = VGroup(c,d,arrow4, arrow3).get_center()

        # Define the semi-circular path for VGroup(e, arrow4)
        start_point = VGroup(a,b,arrow, arrow1).get_center()  # Starting point of the semi-circle
        end_point = VGroup(d,e,arrow3, arrow4).get_center()  # Ending point of the semi-circle
        semi_circle = ArcBetweenPoints(start_point, end_point, angle=PI/2)  # Semi-circular path



        self.play(VGroup(c,d,e,arrow2, arrow3, arrow4).animate.move_to(first),
                  MoveAlongPath(VGroup(a,b, arrow, arrow1) ,semi_circle)
                  )
        
        
        self.play(c[0].animate.set_fill(GREEN).set_color(GREEN),
                  d[0].animate.set_fill(GREEN).set_color(GREEN),
                  e[0].animate.set_fill(GREEN).set_color(GREEN))
        
        self.wait(2)
        




        self.embed()
