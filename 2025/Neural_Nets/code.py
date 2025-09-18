from manimlib import *
import numpy as np

class NeuronNetwork(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Colors
        self.SOMA_COLOR = "#E6A8A8"          
        self.NUCLEUS_COLOR = "#D4527A"       
        self.DENDRITE_COLOR = "#E6A8A8"      
        self.AXON_COLOR = "#F0E68C"          
        self.TERMINAL_COLOR = "#35FA35"      
        self.PULSE_COLOR = "#FF0000"
        self.CONNECTION_COLOR = "#00FFFF"
        
    def construct(self):
        self.create_neuron_network()
        self.animate_pulse_transmission()
    
    def create_neuron_network(self):
        """Create a network of biological neurons filling the screen"""
        self.neurons = VGroup()
        self.connections = VGroup()
        self.neuron_positions = []
        
        # Create more neurons to fill screen better
        rows = 5
        cols = 8
        x_spacing = 2.5
        y_spacing = 1.8
        
        # Calculate starting position to center the grid
        start_x = -(cols - 1) * x_spacing / 2
        start_y = (rows - 1) * y_spacing / 2
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * x_spacing
                y = start_y - row * y_spacing
                position = np.array([x, y, 0.0])
                
                neuron = self.create_biological_neuron()
                neuron.move_to(position)
                self.neurons.add(neuron)
                self.neuron_positions.append(position)
        
        # Create connections between nearby neurons
        self.create_connections()
    
    def create_biological_neuron(self):
        """Create a simplified biological neuron with smaller dendrites, longer axon and nerve endings"""
        neuron_group = VGroup()
        
        # Soma and nucleus (smaller for network view)
        soma = Circle(radius=0.2, color=self.SOMA_COLOR, fill_opacity=0.9, stroke_width=2)
        nucleus = Circle(radius=0.08, color=self.NUCLEUS_COLOR, fill_opacity=1.0, stroke_width=1)
        
        # SMALLER Dendrites (4 directions only, much shorter)
        dendrites = VGroup()
        for angle in [PI/4, 3*PI/4, 5*PI/4, 7*PI/4]:
            # Much shorter main dendrite
            start = soma.get_boundary_point(np.array([np.cos(angle), np.sin(angle), 0]))
            end = start + 0.15 * np.array([np.cos(angle), np.sin(angle), 0])  # Reduced from 0.3
            main_dendrite = Line(start, end, color=self.DENDRITE_COLOR, stroke_width=1.5)
            dendrites.add(main_dendrite)
            
            # Tiny branches
            for branch_offset in [-0.4, 0.4]:
                branch_angle = angle + branch_offset
                branch_end = end + 0.08 * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])  # Reduced from 0.15
                branch = Line(end, branch_end, color=self.DENDRITE_COLOR, stroke_width=1)
                dendrites.add(branch)
        
        # LONGER Axon extending right
        axon_start = soma.get_right()
        axon_end = axon_start + RIGHT * 0.8  # Increased from 0.4
        axon = Line(axon_start, axon_end, color=self.AXON_COLOR, stroke_width=3)
        
        # LONGER Axon terminals and nerve endings
        terminals = VGroup()
        for i in range(5):  # More terminals
            terminal_angle = -0.3 + i * 0.15
            terminal_end = axon_end + 0.4 * np.array([np.cos(terminal_angle), np.sin(terminal_angle), 0])  # Increased from 0.2
            terminal = Line(axon_end, terminal_end, color=self.TERMINAL_COLOR, stroke_width=2)
            terminals.add(terminal)
            
            # Add secondary nerve endings
            for j in range(2):
                secondary_angle = terminal_angle + (j - 0.5) * 0.2
                secondary_end = terminal_end + 0.25 * np.array([np.cos(secondary_angle), np.sin(secondary_angle), 0])
                secondary_terminal = Line(terminal_end, secondary_end, color=self.TERMINAL_COLOR, stroke_width=1.5)
                terminals.add(secondary_terminal)
        
        neuron_group.add(soma, nucleus, dendrites, axon, terminals)
        return neuron_group
    
    def create_connections(self):
        """Create synaptic connections between neurons"""
        for i, pos1 in enumerate(self.neuron_positions):
            for j, pos2 in enumerate(self.neuron_positions):
                if i != j:
                    distance = np.linalg.norm(np.array(pos2) - np.array(pos1))
                    
                    # Connect if neurons are close enough
                    if distance < 3.5:  # Adjusted for new spacing
                        connection = self.create_synapse(pos1, pos2)
                        self.connections.add(connection)
    
    def create_synapse(self, from_pos, to_pos):
        """Create a synaptic connection between two neurons"""
        from_pos = np.array(from_pos, dtype=float)
        to_pos = np.array(to_pos, dtype=float)
        
        # Create curved connection
        mid_point = (from_pos + to_pos) / 2
        # Add perpendicular offset for curve
        direction = to_pos - from_pos
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
            perpendicular = np.array([-direction[1], direction[0], 0])
            curve_offset = perpendicular * np.random.uniform(-0.2, 0.2)
            control_point = mid_point + curve_offset
        else:
            control_point = mid_point
        
        # Create smooth curve
        connection = VMobject()
        connection.set_points_as_corners([
            from_pos + direction * 0.25,
            control_point,
            to_pos - direction * 0.25
        ])
        connection.make_smooth()
        connection.set_stroke(self.CONNECTION_COLOR, width=1, opacity=0.2)
        
        return connection
    
    def animate_pulse_transmission(self):
        """Show the network and animate red pulse transmission"""
        # Show all neurons quickly
        self.play(
            LaggedStartMap(FadeIn, self.neurons, lag_ratio=0.02),
            run_time=2
        )
        
        # Show connections quickly
        self.play(
            LaggedStartMap(ShowCreation, self.connections, lag_ratio=0.01),
            run_time=1.5
        )
        
        self.wait(0.5)
        
        # Start MASSIVE continuous pulse activity for 10 seconds
        self.massive_pulse_activity()
    
    def massive_pulse_activity(self):
        """Create massive continuous red pulse activity for 10 seconds filling entire screen"""
        
        # Create initial burst of 60 pulses
        all_active_pulses = VGroup()
        
        for _ in range(60):
            start_pos = np.array(self.neuron_positions[np.random.randint(0, len(self.neuron_positions))], dtype=float)
            pulse = self.create_red_pulse(start_pos)
            all_active_pulses.add(pulse)
        
        # Show initial pulses
        self.play(
            LaggedStartMap(FadeIn, all_active_pulses, lag_ratio=0.005),
            run_time=0.5
        )
        
        # Run continuous activity for 10 seconds (20 rounds of 0.5 seconds each)
        for round_num in range(20):
            animations = []
            
            # Move all existing pulses to new random positions
            for pulse in all_active_pulses:
                new_pos = np.array(self.neuron_positions[np.random.randint(0, len(self.neuron_positions))], dtype=float)
                # Add screen-wide randomness to fill entire space
                noise = np.random.uniform(-0.3, 0.3, 3)
                final_pos = new_pos + noise
                animations.append(pulse.animate.move_to(final_pos))
            
            # Add 10-15 new pulses each round to maintain intensity
            if round_num % 2 == 0:  # Every other round
                for _ in range(np.random.randint(10, 16)):
                    new_start_pos = np.array(self.neuron_positions[np.random.randint(0, len(self.neuron_positions))], dtype=float)
                    new_pulse = self.create_red_pulse(new_start_pos)
                    all_active_pulses.add(new_pulse)
                    animations.append(FadeIn(new_pulse))
            
            # Remove some old pulses randomly to prevent overcrowding - FIXED VERSION
            if len(all_active_pulses) > 80:
                # Convert to list and randomly select indices
                pulse_list = list(all_active_pulses.submobjects)
                indices_to_remove = np.random.choice(len(pulse_list), size=min(10, len(pulse_list)), replace=False)
                
                # Remove selected pulses
                for idx in sorted(indices_to_remove, reverse=True):  # Remove from end to avoid index shifting
                    pulse_to_remove = pulse_list[idx]
                    all_active_pulses.remove(pulse_to_remove)
                    animations.append(FadeOut(pulse_to_remove))
            
            # Execute all animations
            if animations:
                self.play(*animations, run_time=0.5)
        
        # Final explosive fade
        self.play(
            *[pulse.animate.scale(2.5).set_opacity(0) for pulse in all_active_pulses],
            run_time=2
        )
        
        self.wait(1)
    
    def create_red_pulse(self, position):
        """Create a red pulse with glow effect at given position"""
        pulse_size = np.random.uniform(0.04, 0.09)
        pulse = Dot(radius=pulse_size, color=self.PULSE_COLOR, fill_opacity=1.0)
        glow = Circle(radius=pulse_size * 3, color=self.PULSE_COLOR, 
                     fill_opacity=0.3, stroke_opacity=0)
        
        pulse_group = VGroup(pulse, glow)
        pulse_group.move_to(position)
        
        return pulse_group



class BiologicalNeuron(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Colors
        self.SOMA_COLOR = "#E6A8A8"          
        self.NUCLEUS_COLOR = "#D4527A"       
        self.DENDRITE_COLOR = "#E6A8A8"      
        self.AXON_COLOR = "#F0E68C"          
        self.MYELIN_COLOR = "#FFE4B5"        
        self.SCHWANN_COLOR = "#DEB887"       
        self.NODE_COLOR = "#F0E68C"          
        self.TERMINAL_COLOR = "#35FA35"      
        self.LABEL_COLOR = "#000000"
        self.ELLIPSE_COLOR = "#CD5C5C"       # Indian red for organelles
        
    def construct(self):
        self.camera.frame.shift(RIGHT*3.64)
        self.create_neuron_structure()
        self.animate_complete_neuron()
    
    def create_neuron_structure(self):
        # Central soma and nucleus
        self.soma = Circle(radius=0.6, color=self.SOMA_COLOR, fill_opacity=1.0, stroke_width=2)
        self.soma.move_to(ORIGIN)
        
        self.nucleus = Circle(radius=0.25, color=self.NUCLEUS_COLOR, fill_opacity=1.0, stroke_width=1)
        self.nucleus.move_to(ORIGIN)
        
        # Add tiny ellipses in cytoplasm
        self.create_cytoplasm_ellipses()
        
        # Create shorter dense dendrites
        self.create_shorter_dense_dendrites()
        
        # Create axon system
        self.create_axon_system()
        
        # Create axon dots (NEW)
        self.create_axon_dots()
        
        # Create longer but less dense nerve endings
        self.create_longer_less_dense_nerve_endings()
    
    def create_cytoplasm_ellipses(self):
        """Add small ellipses inside soma as cytoplasmic organelles"""
        self.cytoplasm_ellipses = VGroup()
        
        # Create various tiny organelles in cytoplasm
        num_ellipses = 15
        
        for _ in range(num_ellipses):
            # Random size for variety
            width = np.random.uniform(0.04, 0.08)
            height = width * np.random.uniform(0.6, 1.2)
            
            # Create small ellipse
            ellipse = Ellipse(width=width, height=height, 
                            color=self.ELLIPSE_COLOR, 
                            fill_opacity=0.8, 
                            stroke_width=1)
            
            # Random position in cytoplasm (between nucleus and cell membrane)
            angle = np.random.uniform(0, 2*PI)
            radius = np.random.uniform(0.28, 0.55)  # Outside nucleus, inside soma
            pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])
            
            ellipse.move_to(pos)
            ellipse.rotate(np.random.uniform(0, 2*PI))  # Random orientation
            
            self.cytoplasm_ellipses.add(ellipse)
    
    def create_shorter_dense_dendrites(self):
        """Create shorter dendrites with dense endings"""
        self.dendrites = VGroup()
        
        main_dendrite_angles = [PI/6, PI/3, 2*PI/3, PI, 4*PI/3, 5*PI/3]
        
        for angle in main_dendrite_angles:
            self.create_short_dense_dendrite_branch(angle)
    
    def create_short_dense_dendrite_branch(self, base_angle):
        """Create shorter dendrite branches with dense endings"""
        start_point = self.soma.get_boundary_point(np.array([np.cos(base_angle), np.sin(base_angle), 0]))
        
        # Shorter main trunk
        trunk_length = 0.5
        trunk_end = start_point + trunk_length * np.array([np.cos(base_angle), np.sin(base_angle), 0])
        
        main_trunk = Line(start_point, trunk_end, color=self.DENDRITE_COLOR, stroke_width=3)
        self.dendrites.add(main_trunk)
        
        # Create dense branching
        self.create_dense_dendrite_branching(trunk_end, base_angle, 1, 0.4)
    
    def create_dense_dendrite_branching(self, start_point, base_angle, level, length_factor):
        """Create dense dendrite branching"""
        if level > 2:
            return
        
        # More branches for density
        if level == 1:
            num_branches = 4
            angle_spread = PI/3
        else:
            num_branches = 3
            angle_spread = PI/4
        
        branch_length = 0.3 * length_factor
        stroke_width = max(1, 4 - level * 2)
        
        for i in range(num_branches):
            branch_angle = base_angle + (i - (num_branches-1)/2) * (angle_spread/(num_branches-1))
            branch_angle += np.random.uniform(-0.15, 0.15)
            
            end_point = start_point + branch_length * np.array([np.cos(branch_angle), np.sin(branch_angle), 0])
            branch = Line(start_point, end_point, color=self.DENDRITE_COLOR, stroke_width=stroke_width)
            self.dendrites.add(branch)
            
            # Continue branching for density
            if level < 2:
                self.create_dense_dendrite_branching(end_point, branch_angle, level + 1, length_factor * 0.7)
            
            # Add extra fine branches at final level
            if level == 2:
                for j in range(2):
                    fine_angle = branch_angle + (j - 0.5) * PI/6
                    fine_end = end_point + 0.15 * np.array([np.cos(fine_angle), np.sin(fine_angle), 0])
                    fine_branch = Line(end_point, fine_end, color=self.DENDRITE_COLOR, stroke_width=1)
                    self.dendrites.add(fine_branch)
    
    def create_axon_system(self):
        """Create axon with opaque myelin sheaths"""
        axon_start = self.soma.get_boundary_point(RIGHT)
        
        self.axon_path = [
            axon_start,
            axon_start + RIGHT * 1.0,
            axon_start + RIGHT * 2.0 + DOWN * 0.1,
            axon_start + RIGHT * 3.0 + DOWN * 0.1,
            axon_start + RIGHT * 4.0 + DOWN * 0.2,
            axon_start + RIGHT * 5.5 + DOWN * 0.2
        ]
        
        # Main axon
        self.axon = VMobject()
        self.axon.set_points_smoothly(self.axon_path)
        self.axon.set_stroke(self.AXON_COLOR, width=4)
        
        # Create opaque myelin sheaths
        self.create_opaque_myelin_sheaths()
    
    def create_axon_dots(self):
        """Create small RED_E colored dots inside the axon (NEW METHOD)"""
        self.axon_dots = VGroup()
        
        # Create dots along the axon path
        num_dots = 20  # Number of dots to distribute along axon
        
        for i in range(num_dots):
            # Calculate position along axon (t from 0 to 1)
            t = (i + 0.5) / num_dots  # Slight offset so dots don't start exactly at beginning
            
            # Get position along axon path
            dot_position = self.get_axon_position(t)
            
            # Add some random offset perpendicular to axon for natural distribution
            if i < len(self.axon_path) - 1:
                # Get approximate direction of axon at this point
                next_t = min(1.0, t + 0.01)
                direction = self.get_axon_position(next_t) - self.get_axon_position(t)
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                    # Perpendicular direction
                    perp_direction = np.array([-direction[1], direction[0], 0])
                    # Small random offset perpendicular to axon
                    offset = np.random.uniform(-0.1, 0.1) * perp_direction
                    dot_position += offset
            
            # Create elliptical dot with slight randomness
            dot_width = np.random.uniform(0.03, 0.06)
            dot_height = np.random.uniform(0.03, 0.05)
            
            dot = Ellipse(width=dot_width, height=dot_height, 
                         color=RED_E, fill_opacity=1, stroke_width=1, fill_color=RED_E)
            dot.move_to(dot_position)
            dot.rotate(np.random.uniform(0, PI))  # Random orientation
            
            self.axon_dots.add(dot)
    
    def create_opaque_myelin_sheaths(self):
        """Create opaque myelin sheaths"""
        self.myelin_sheaths = VGroup()
        self.schwann_cells = VGroup()
        self.nodes_of_ranvier = VGroup()
        
        num_segments = 5
        segment_length = 0.8
        gap_length = 0.2
        
        for i in range(num_segments):
            start_t = (i * (segment_length + gap_length)) / 5.5
            end_t = (i * (segment_length + gap_length) + segment_length) / 5.5
            
            if end_t > 1.0:
                break
                
            start_pos = self.get_axon_position(start_t)
            end_pos = self.get_axon_position(end_t)
            center_pos = (start_pos + end_pos) / 2
            
            # Opaque myelin sheath
            myelin = Ellipse(width=segment_length, height=0.3, 
                           color=self.MYELIN_COLOR, fill_opacity=1.0, stroke_width=2)
            myelin.move_to(center_pos)
            self.myelin_sheaths.add(myelin)
            
            # Opaque Schwann cell
            schwann = Ellipse(width=segment_length + 0.1, height=0.4,
                            color=self.SCHWANN_COLOR, fill_opacity=0.8, stroke_width=1)
            schwann.move_to(center_pos)
            self.schwann_cells.add(schwann)
            
            # Opaque nodes
            if i < num_segments - 1:
                gap_pos = self.get_axon_position(end_t + gap_length/2/5.5)
                node = Circle(radius=0.06, color=self.NODE_COLOR, fill_opacity=1.0)
                node.move_to(gap_pos)
                self.nodes_of_ranvier.add(node)
    
    def get_axon_position(self, t):
        """Get position along axon path"""
        if t <= 0:
            return np.array(self.axon_path[0])
        elif t >= 1:
            return np.array(self.axon_path[-1])
        else:
            total_length = len(self.axon_path) - 1
            segment = int(t * total_length)
            local_t = (t * total_length) - segment
            
            if segment >= len(self.axon_path) - 1:
                return np.array(self.axon_path[-1])
            
            start = np.array(self.axon_path[segment])
            end = np.array(self.axon_path[segment + 1])
            return start + local_t * (end - start)
    
    def create_longer_less_dense_nerve_endings(self):
        """Create LONGER nerve endings (1.5x) but LESS DENSE"""
        self.nerve_endings = VGroup()
        
        terminal_start = self.axon_path[-1]
        
        # Fewer main terminal angles for less density
        main_terminal_angles = [
            0,          # Center
            PI/12,      # Upper right narrow
            -PI/12,     # Lower right narrow
            PI/8,       # Upper right
            -PI/8,      # Lower right
            PI/6,       # Upper right wide
            -PI/6,      # Lower right wide
            PI/5,       # Upper branch
            -PI/5       # Lower branch
        ]
        
        # Create LONGER main terminal branches but fewer secondary branches
        for angle in main_terminal_angles:
            # LONGER straight roots (1.5x longer)
            main_length = np.random.uniform(1.2, 1.8)  # 1.5x longer than before
            main_end = terminal_start + main_length * np.array([np.cos(angle), np.sin(angle), 0])
            
            # Main terminal branch - STRAIGHT and LONGER
            main_branch = Line(terminal_start, main_end, color=self.TERMINAL_COLOR, stroke_width=3)
            self.nerve_endings.add(main_branch)
            
            # Add FEWER secondary branches for less density
            if np.random.random() > 0.4:  # Only 60% chance instead of 100%
                num_secondary = 1  # Only 1 secondary branch instead of 3
                
                # Position along main branch
                t = 0.6  # Fixed position instead of multiple
                secondary_start = terminal_start + t * main_length * np.array([np.cos(angle), np.sin(angle), 0])
                
                # Secondary branch angle
                secondary_angle = angle + np.random.uniform(-PI/6, PI/6)
                secondary_length = np.random.uniform(0.25, 0.4)
                secondary_end = secondary_start + secondary_length * np.array([np.cos(secondary_angle), np.sin(secondary_angle), 0])
                
                # Secondary branch
                secondary_branch = Line(secondary_start, secondary_end, color=self.TERMINAL_COLOR, stroke_width=2)
                self.nerve_endings.add(secondary_branch)
        
        # Add fewer fine terminal branches
        for _ in range(3):  # Reduced from 8 to 3
            fine_angle = np.random.uniform(-PI/4, PI/4)
            fine_start = terminal_start + 0.4 * np.array([np.cos(fine_angle), np.sin(fine_angle), 0])
            fine_length = np.random.uniform(0.2, 0.35)
            fine_angle_end = fine_angle + np.random.uniform(-0.3, 0.3)
            
            fine_end = fine_start + fine_length * np.array([np.cos(fine_angle_end), np.sin(fine_angle_end), 0])
            fine_branch = Line(fine_start, fine_end, color=self.TERMINAL_COLOR, stroke_width=1)
            self.nerve_endings.add(fine_branch)
    
    def animate_complete_neuron(self):
        """Animate all components simultaneously"""
        
        # Create ALL components at the same time with staggered timing
        self.play(
            DrawBorderThenFill(self.soma),
            DrawBorderThenFill(self.nucleus),
            LaggedStartMap(FadeIn, self.cytoplasm_ellipses, lag_ratio=0.1),  # Show organelles
            LaggedStartMap(GrowFromCenter, self.dendrites, lag_ratio=0.05),
            ShowCreation(self.axon),
            LaggedStartMap(FadeIn, self.axon_dots, lag_ratio=0.05),  # Show axon dots (NEW)
            LaggedStartMap(FadeIn, self.schwann_cells, lag_ratio=0.08),
            LaggedStartMap(FadeIn, self.myelin_sheaths, lag_ratio=0.08),
            LaggedStartMap(FadeIn, self.nodes_of_ranvier, lag_ratio=0.1),
            LaggedStartMap(ShowCreation, self.nerve_endings, lag_ratio=0.04),
            run_time=1.5
        )
        
        self.wait()

        brace = Brace(self.nerve_endings, RIGHT)
        a = Text("Nerve\nEnding").next_to(brace, RIGHT)

        self.play(GrowFromCenter(brace), ShowCreation(a))
        
        self.wait()

        b = Text("Axon").next_to(self.axon, DOWN).shift(DOWN*0.17+LEFT*0.33)
        self.play(Write(b))

        self.wait(1)

        arrow = Arrow(self.nucleus.get_bottom()+DOWN*1.8, self.nucleus.get_center(), stroke_width=4).set_color(WHITE).shift(DOWN*0.4)
        self.play(GrowArrow(arrow))
        c = Text("Soma").next_to(arrow, DOWN).shift(DOWN*0.03)
        self.play(ShowCreation(c))

        self.wait()

        arrow1 = Arrow(self.nucleus.get_top()+UP*2.3, self.nucleus.get_center()+UP*0.2, stroke_width=4).shift(DOWN*0.4).set_color(TEAL_E)
        self.play(GrowArrow(arrow1))
        d = Text("Nucleus").next_to(arrow1, UP).shift(UP*0.03)
        self.play(ShowCreation(d))

        self.wait()

        arrow3 = Arrow(self.nucleus.get_top()+UP*2.3, self.nucleus.get_center()+UP*0.2, stroke_width=4).set_color(GREY_A)
        arrow3.rotate(-PI/2.38).shift(RIGHT*2.14+DOWN*0.1)

        self.play(ShowCreation(arrow3))

        e = Text("Dendrites").next_to(arrow3, RIGHT).shift(UP*0.3+RIGHT*0.02)
        self.play(ShowCreation(e))

        self.wait(2)
        self.play(FadeOut(VGroup(a,b,c,d,e,arrow3, arrow, arrow1, brace)))
        self.play(self.camera.frame.animate.shift(LEFT*0.4).scale(0.9))

        # Information flow animation - 3 iterations using your pulse style
        def create_pulse(start_point, color):
            pulse = Dot(radius=0.07, color=color, fill_opacity=1)
            pulse.move_to(start_point)
            glow = Circle(radius=0.18, color=color, fill_opacity=0.5, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow

        for iteration in range(1):
            pulses = VGroup()
            glows = VGroup()
            
            # Create pulses at dendrite endpoints
            dendrite_endpoints = []
            for dendrite in self.dendrites:
                if isinstance(dendrite, Line):
                    endpoint = dendrite.get_end()
                    dendrite_endpoints.append(endpoint)
            
            # Select some dendrite endpoints for pulses (not all to avoid clutter)
            selected_endpoints = dendrite_endpoints[::3]  # Every 3rd endpoint
            
            for endpoint in selected_endpoints:
                pulse, glow = create_pulse(endpoint, "#FF0000")
                pulses.add(pulse)
                glows.add(glow)
            
            # Show pulses appearing at dendrites
            self.play(
                LaggedStartMap(FadeIn, pulses, lag_ratio=0.1),
                LaggedStartMap(FadeIn, glows, lag_ratio=0.1),
                run_time=0.5
            )
            
            # Move pulses from dendrites to soma center
            soma_center = self.soma.get_center()
            
            animations = []
            for pulse, glow in zip(pulses, glows):
                animations.append(pulse.animate.move_to(soma_center))
                animations.append(glow.animate.move_to(soma_center))
            
            self.play(*animations, run_time=1.2)
            
            # Merge pulses at soma and create single pulse for axon
            self.play(FadeOut(pulses), FadeOut(glows), run_time=0.2)
            
            # Create larger pulse at soma
            soma_pulse, soma_glow = create_pulse(soma_center, "#FF0000")
            soma_pulse.scale(1.5)  # Make it slightly larger
            soma_glow.scale(1.2)
            
            self.play(FadeIn(soma_pulse), FadeIn(soma_glow), run_time=0.8)
            
            # Move pulse along axon path
            axon_positions = []
            num_axon_steps = 15
            for i in range(num_axon_steps + 1):
                t = i / num_axon_steps
                pos = self.get_axon_position(t)
                axon_positions.append(pos)
            
            # Animate along axon
            for pos in axon_positions[1:]:
                self.play(
                    soma_pulse.animate.move_to(pos),
                    soma_glow.animate.move_to(pos),
                    run_time=0.25
                )
            
            # At nerve endings, split into multiple pulses
            nerve_ending_positions = []
            for ending in self.nerve_endings:
                if isinstance(ending, Line):
                    nerve_ending_positions.append(ending.get_end())
            
            # Select some nerve ending positions
            selected_nerve_endings = nerve_ending_positions[::2]  # Every 2nd ending
            
            # Create multiple pulses at nerve endings
            nerve_pulses = VGroup()
            nerve_glows = VGroup()
            
            for ending_pos in selected_nerve_endings:
                pulse, glow = create_pulse(soma_pulse.get_center(), "#FF0606")
                nerve_pulses.add(pulse)
                nerve_glows.add(glow)
            
            # Hide soma pulse and show nerve pulses
            self.play(
                FadeOut(soma_pulse),
                FadeOut(soma_glow),
                FadeIn(nerve_pulses),
                FadeIn(nerve_glows),
                run_time=0.35
            )
            
            # Move to nerve endings
            animations = []
            for i, (pulse, glow) in enumerate(zip(nerve_pulses, nerve_glows)):
                if i < len(selected_nerve_endings):
                    animations.append(pulse.animate.move_to(selected_nerve_endings[i]))
                    animations.append(glow.animate.move_to(selected_nerve_endings[i]))
            
            self.play(*animations, run_time=0.6)
            
            # Fade out pulses at nerve endings
            self.play(
                LaggedStartMap(FadeOut, nerve_pulses, lag_ratio=0.05),
                LaggedStartMap(FadeOut, nerve_glows, lag_ratio=0.05),
                run_time=0.5
            )
            
            # Short pause between iterations
            if iteration < 2:  # Don't wait after last iteration
                self.wait(0.5)
        
        self.wait(2)




class NeuronsIntro(Scene):
    def construct(self):

        self.camera.frame.scale(0.9).shift(RIGHT*0.9+UP*0.1)
        # Create the main neuron (circular node) - full opacity
        neuron = Circle(radius=0.8, color=BLUE, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        neuron.move_to(ORIGIN)
        
        # Input nodes - full opacity, closer to make more space on right
        input1 = Circle(radius=0.3, color=GREEN, fill_opacity=1, stroke_width=7
                        , stroke_color=GREEN_B)
        input2 = Circle(radius=0.3, color=GREEN, fill_opacity=1, stroke_width=7, stroke_color=GREEN_B)
        input1.move_to(LEFT * 3.2 + UP * 1.5)
        input2.move_to(LEFT * 3.2 + DOWN * 1.5)
        
        # Larger input labels - scaled 1.8
        x1_label = Tex("x_1", font_size=40).scale(1.8).next_to(input1, LEFT, buff=0.2)
        x2_label = Tex("x_2", font_size=40).scale(1.8).next_to(input2, LEFT, buff=0.2)
        
        # Larger weight labels - scaled 1.8
        w1_label = Tex("w_1", font_size=36, color=RED).scale(1.8)
        w2_label = Tex("w_2", font_size=36, color=RED).scale(1.8)
        
        # Bias arrow and larger label - positioned slightly UP
        bias_arrow = Arrow(UP * 2.5, neuron.get_top() + UP * 0.1, stroke_width=3)
        bias_arrow.set_color(PURPLE)
        bias_label = Tex("b", font_size=40, color=PURPLE).scale(1.8).next_to(bias_arrow.get_start(), UP, buff=0.28)
        
        # Thicker connection lines from center to center with z_index = -1
        line1 = Line(input1.get_center(), neuron.get_center(), stroke_width=6, z_index=-1)
        line2 = Line(input2.get_center(), neuron.get_center(), stroke_width=6, z_index=-1)
        line1.set_color(WHITE)
        line2.set_color(WHITE)
        
        # Position weight labels
        w1_label.move_to(line1.get_center() + UP * 0.5)
        w2_label.move_to(line2.get_center() + DOWN * 0.5)
        
        # Output arrow
        output_arrow = Arrow(neuron.get_right(), RIGHT * 2.5, stroke_width=3)
        output_arrow.set_color(BLUE)
        output_label = Tex("y", font_size=40, color=BLUE).scale(1.8).next_to(output_arrow.get_end(), RIGHT)
        
        # Build structure
        self.play(
            ShowCreation(input1), ShowCreation(input2),
            Write(x1_label), Write(x2_label)
        )

        self.play(ShowCreation(neuron))
        self.wait(1)
        self.play(
            ShowCreation(line1), ShowCreation(line2),
            Write(w1_label), Write(w2_label)
        )

        self.wait(2)


        
        # First formula without bias - larger size
        linear_no_bias = Tex("z = w_1 x_1 + w_2 x_2", font_size=58)
        linear_no_bias.to_edge(RIGHT, buff=1)
        self.play(
            FadeIn(linear_no_bias[:2]),
            FadeIn(linear_no_bias[6]),

            TransformFromCopy(x1_label, linear_no_bias[4:6]),
            TransformFromCopy(w1_label, linear_no_bias[2:4]),
            TransformFromCopy(x2_label, linear_no_bias[-4:-2]),
            TransformFromCopy(w2_label, linear_no_bias[-2:]),
        )
        self.wait(2)

        self.play(linear_no_bias[2:4].animate.set_color(YELLOW).scale(1.32))
        self.wait(2)
        self.play(linear_no_bias[2:4].animate.set_color(YELLOW).scale(1/1.32*0.66))
        self.wait(2)
        self.play(linear_no_bias[2:4].animate.set_color(WHITE).scale(1.4))
        self.wait(2)

        

        brace = Brace(linear_no_bias[2:], DOWN)
        brace_text = Text("0", font_size=46, color=YELLOW)
        brace_text.next_to(brace, DOWN, buff=0.3)
        
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(2)


        self.play(FadeOut(brace), FadeOut(brace_text))
        self.wait(1)


        # Add bias term and arrow
        self.play(ShowCreation(bias_arrow), Write(bias_label))
        
        # Update formula with bias - same size
        linear_with_bias = Tex("z = w_1 x_1 + w_2 x_2 + b", font_size=48)
        linear_with_bias.move_to(linear_no_bias.get_center())
        self.play(Transform(linear_no_bias, linear_with_bias))
        self.wait(2)
        
        # Transform that formula into general form AT THE SAME PLACE
        general_formula = Tex(r"z = \sum_{i=1}^{n} w_i x_i + b", font_size=62)
        general_formula.move_to(linear_no_bias.get_center())
        self.play(Transform(linear_no_bias, general_formula))
        self.wait(2)

        self.play(linear_no_bias.animate.shift(UP))

        # BELOW it, show y = phi() first (fade in phi() without z)
        activation_phi = Tex(r"y = \phi(z)", font_size=68)
        activation_phi.next_to(linear_no_bias, DOWN, buff=1)
        self.play(FadeIn(activation_phi[:4]), FadeIn(activation_phi[-1]))
        self.wait(1.5)
        

        
        self.play(
            TransformFromCopy(linear_no_bias, activation_phi[4]),
        )
        self.wait(2)



        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2.9, 2.9, 1],
            axis_config={
                "stroke_width": 7,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },



        ).shift(RIGHT*12.6+DOWN*0.2)

        # Create axis labels (at the end of axes)
        x_label = Tex("z", font_size=63).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Tex("y", font_size=63).next_to(axes.y_axis.get_end(), UP, buff=0.2)

        # First, add little white bars at y = -2 and y = 2 on y-axis (but label them as -1 and 1)
        y_tick_neg2 = Line(
            axes.c2p(-0.2, -1.7), axes.c2p(0.2, -1.7),
            stroke_width=6, color=WHITE
        )
        y_tick_pos2 = Line(
            axes.c2p(-0.2, 1.7), axes.c2p(0.2, 1.7),
            stroke_width=6, color=WHITE
        )
        
        # Add labels showing -1 and 1 (for visual clarity) even though ticks are at -2 and 2
        y_label_neg1 = Tex("-1", font_size=40, color=WHITE).next_to(y_tick_neg2, LEFT, buff=0.3)
        y_label_pos1 = Tex("1", font_size=40, color=WHITE).next_to(y_tick_pos2, LEFT, buff=0.3)
        

        self.play(ShowCreation(axes), self.camera.frame.animate.shift(RIGHT*12), ShowCreation(y_tick_neg2), ShowCreation(y_tick_pos2),
           )

        self.play(ShowCreation(x_label), ShowCreation(y_label))

        self.wait(2)

        # Step Function (scaled to -2, 2 range)
        step_points = []
        x_vals = np.linspace(-5, 5, 1000)
        for x in x_vals:
            y = 1.7 if x >= 0 else -1.7  # Using 2 and -2 instead of 1 and 0
            step_points.append(axes.c2p(x, y))
        
        step_graph = VMobject()
        step_graph.set_points_as_corners(step_points)
        step_graph.set_stroke(RED, width=8)
        
        # Step function title and formula in second quadrant
        step_title = Text("Step Function", font_size=44, color=RED)
        step_title.move_to(axes.c2p(-3, 3.3))
        step_title.z_index = 10
        
        step_formula = Tex(r"\phi(z) = \begin{cases} 1 & \text{if } z \geq 0 \\ -1 & \text{if } z < 0 \end{cases}", 
                           font_size=40, color=RED)
        step_formula.next_to(step_title, DOWN, buff=0.46)
        step_formula.z_index = 10
        
        self.play(ShowCreation(step_graph), Write(step_title), Write(step_formula))
        self.wait(2)

        
        # Transform Step to ReLU (scaled to fit -2, 2 range)
        relu_points = []
        for x in x_vals:
            y = max(0, x)  # Scaled ReLU to fit in -2 to 2 range
            relu_points.append(axes.c2p(x, y))
        
        relu_graph = VMobject()
        relu_graph.set_points_as_corners(relu_points)
        relu_graph.set_stroke(GREEN, width=8)
        
        # ReLU title and formula in second quadrant
        relu_title = Text("ReLU Function", font_size=44, color=GREEN)
        relu_title.move_to(step_title)
        relu_title.z_index = 10
        
        relu_formula = Tex(r"ReLU(z) = \max(0, z)", font_size=46, color=GREEN)
        relu_formula.next_to(relu_title, DOWN, buff=0.44)
        relu_formula.z_index = 10
        
        self.play(
            Transform(step_graph, relu_graph),
            Transform(step_title, relu_title),
            Transform(step_formula, relu_formula)
        )
        self.wait(2)
        
        # Transform ReLU to Sigmoid (scaled to -2, 2 range)
        sigmoid_points = []
        for x in x_vals:
            sigmoid_val = 1 / (1 + np.exp(-x))  # Standard sigmoid (0 to 1)
            y = (sigmoid_val * 2 - 1) * 1.7  # Scale to -1.7 to +1.7 range
            sigmoid_points.append(axes.c2p(x, y))
        
        sigmoid_graph = VMobject()
        sigmoid_graph.set_points_smoothly(sigmoid_points)
        sigmoid_graph.set_stroke(PURPLE, width=8)
        
        # Sigmoid title and formula in second quadrant
        sigmoid_title = Text("Sigmoid Function", font_size=44, color=PURPLE)
        sigmoid_title.move_to(relu_title)
        sigmoid_title.z_index = 10
        
        sigmoid_formula = Tex(r"\sigma(z) = \frac{1}{1 + e^{-z}}", font_size=46, color=PURPLE)
        sigmoid_formula.next_to(relu_title, DOWN, buff=0.45)
        sigmoid_formula.z_index = 10
        
        self.play(
            Transform(step_graph, sigmoid_graph),
            Transform(step_title, sigmoid_title),
            Transform(step_formula, sigmoid_formula)
        )
        self.wait(3)


        
        self.wait(1)
        
        # Move camera back to the left
        self.play(
            self.camera.frame.animate.shift(LEFT*12+UP*0.24),
            run_time=2
        )
        self.wait(1)

        self.play(FadeOut(linear_no_bias), FadeOut(activation_phi), self.camera.frame.animate.shift(LEFT*1.55))
        

        # Add output arrow and label
        self.play(ShowCreation(output_arrow))
        
        # Information flow animation
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.2, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.4, color=color, fill_opacity=0.4, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        pulse1, glow1 = create_pulse(input1.get_center(), neuron.get_center(), color=YELLOW)
        pulse2, glow2 = create_pulse(input2.get_center(), neuron.get_center(), color=ORANGE)
        pulse_bias, glow_bias = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        self.add(pulse1, glow1, pulse2, glow2, pulse_bias, glow_bias)
        
        self.play(
            pulse1.animate.move_to(neuron.get_center()),
            glow1.animate.move_to(neuron.get_center()),
            pulse2.animate.move_to(neuron.get_center()),
            glow2.animate.move_to(neuron.get_center()),
            pulse_bias.animate.move_to(neuron.get_center()),
            glow_bias.animate.move_to(neuron.get_center()),
            run_time=2
        )
        
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse1), FadeOut(glow1),
            FadeOut(pulse2), FadeOut(glow2),
            FadeOut(pulse_bias), FadeOut(glow_bias),
            run_time=0.8
        )
        
        # Show phi in neuron - scale 1.7 and set_color BLACK
        phi_in_neuron = Tex(r"\phi(z)", font_size=32).scale(1.7)
        phi_in_neuron.set_color(BLACK)
        phi_in_neuron.move_to(neuron.get_center())
        
        self.play(Write(phi_in_neuron))
        self.wait(1)
        
        # Output pulse
        output_pulse, output_glow = create_pulse(neuron.get_center(), output_arrow.get_end(), color=BLUE)
        self.add(output_pulse, output_glow)
        
        self.play(
            output_pulse.animate.move_to(output_label),
            output_glow.animate.move_to(output_label),
            neuron.animate.set_fill(BLUE, opacity=1),
            run_time=1.5
        )
        
        self.play(FadeOut(output_pulse), FadeIn(output_label) ,FadeOut(output_glow),FadeOut(VGroup(axes, step_formula, sigmoid_graph, step_title, x_label, y_label, y_label_neg1, y_label_pos1, step_graph, y_tick_neg2, y_tick_pos2)))
        self.wait(2)

        self.camera.frame.save_state()

        self.camera.frame.restore()
       

        # OR gate truth table: output is 1 when at least one input is 1
        table_data = [
            ["x_1", "x_2", "y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "1"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 6.6
        row_height = 0.54
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Tex(cell, font_size=22, color=WHITE)
                cell_x = table_center_x + (j - 1) * 0.67
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.87).shift(RIGHT*2.69+DOWN*0.64)

        title = Text("OR Gate", weight=BOLD).next_to(table_group, UP, buff=0.69).set_color(GREEN_B).scale(1.3)
        self.play(ShowCreation(title))


        self.play(ShowCreation(table_group), self.camera.frame.animate.shift(RIGHT*9.9))
        
        self.wait(2)

        self.play(FadeOut(table_group),  FadeOut(title), self.camera.frame.animate.shift(LEFT*9.9))
        self.wait(2)

        weight_1 = Text("1").move_to(w1_label).scale(1.2)
        weight_2 = Text("1").move_to(w2_label).scale(1.2)
        bias = Text("0").move_to(bias_label).scale(1.2)

        self.play(
            ReplacementTransform(w1_label, weight_1),
            ReplacementTransform(w2_label, weight_2),
            ReplacementTransform(bias_label, bias),
        )

        self.wait(2)

        x1 = Text("1").move_to(x1_label).scale(1.2)
        x2 = Text("1").move_to(x2_label).scale(1.2)
        y = Text("1").move_to(output_label).scale(1.2)


        self.play(
            ReplacementTransform(x1_label, x1),
            ReplacementTransform(x2_label, x2),
        )




        # Information flow animation
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.2, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.4, color=color, fill_opacity=0.4, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        pulse1, glow1 = create_pulse(input1.get_center(), neuron.get_center(), color=YELLOW)
        pulse2, glow2 = create_pulse(input2.get_center(), neuron.get_center(), color=ORANGE)
        pulse_bias, glow_bias = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        self.add(pulse1, glow1, pulse2, glow2, pulse_bias, glow_bias)
        
        self.play(
            pulse1.animate.move_to(neuron.get_center()),
            glow1.animate.move_to(neuron.get_center()),
            pulse2.animate.move_to(neuron.get_center()),
            glow2.animate.move_to(neuron.get_center()),
            pulse_bias.animate.move_to(neuron.get_center()),
            glow_bias.animate.move_to(neuron.get_center()),
            run_time=2
        )
        
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse1), FadeOut(glow1),
            FadeOut(pulse2), FadeOut(glow2),
            FadeOut(pulse_bias), FadeOut(glow_bias),
            run_time=0.8
        )
        

        # Output pulse
        output_pulse, output_glow = create_pulse(neuron.get_center(), output_arrow.get_end(), color=BLUE)
        self.add(output_pulse, output_glow)
        
        self.play(
            output_pulse.animate.move_to(output_label),
            output_glow.animate.move_to(output_label),
            neuron.animate.set_fill(BLUE, opacity=1),
            run_time=1.5
        )
        
        self.play(FadeOut(output_pulse), FadeOut(output_glow),FadeOut(VGroup(axes, step_formula, sigmoid_graph, step_title, x_label, y_label, y_label_neg1, y_label_pos1, step_graph, y_tick_neg2, y_tick_pos2)))
        self.play(ReplacementTransform(output_label, y),)


        self.wait(2)



        self.play(
            Transform(x1, Text("0").scale(1.2).move_to(x1))
        )

        self.wait()

        self.play(
            Transform(x1, Text("1").scale(1.2).move_to(x1)),
            Transform(x2, Text("0").scale(1.2).move_to(x2)),
        )

        self.wait()

        self.play(
            Transform(x1, Text("0").scale(1.2).move_to(x1)),
            Transform(x2, Text("0").scale(1.2).move_to(x2)),
            Transform(y, Text("0").scale(1.2).move_to(y)),
        )


        self.wait(2)


        self.play(
            Transform(x1, Tex("x_1").scale(1.2).move_to(x1)),
            Transform(x2, Tex("x_2").scale(1.2).move_to(x2)),
            Transform(y, Tex("y").scale(1.2).move_to(y)),
            Transform(weight_1, Tex("w_1").scale(1.2).move_to(weight_1)),
            Transform(weight_2, Tex("w_2").scale(1.2).move_to(weight_2)),
            Transform(bias, Text("b").scale(1.2).move_to(bias)),
        )

        self.wait()


        self.camera.frame.save_state()
        self.camera.frame.restore()



        axes = Axes(
            x_range=[-0.4, 8, 0.1],
            y_range=[-0.4, 5.5, 0.1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },
        ).shift(LEFT * 12.7)

        # Add ticks at scaled positions (7 represents 1 on x, 4.5 represents 1 on y)
        x_tick = Line(axes.c2p(7, -0.2), axes.c2p(7, 0.2), stroke_width=4, color=WHITE)
        y_tick = Line(axes.c2p(-0.2, 4.5), axes.c2p(0.2, 4.5), stroke_width=4, color=WHITE)

        # Tick labels showing "1" 
        x_tick_label = Tex("1", font_size=36, color=WHITE).next_to(x_tick, DOWN, buff=0.2)
        y_tick_label = Tex("1", font_size=36, color=WHITE).next_to(y_tick, LEFT, buff=0.2)

        # Axis labels
        x1_label = Tex(r"x_1", font_size=48).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        x2_label = Tex(r"x_2", font_size=48).next_to(axes.y_axis.get_end(), UP, buff=0.2)
 
        # OR gate data points with proper scaling
        point_00 = Dot(axes.c2p(0, 0), radius=0.2, color=RED).set_color(RED)        # (0,0) → (0, 0)
        point_01 = Dot(axes.c2p(0, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (0,1) → (0, 4.5)
        point_10 = Dot(axes.c2p(7, 0), radius=0.2, color=GREEN).set_color(GREEN)      # (1,0) → (7, 0)
        point_11 = Dot(axes.c2p(7, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (1,1) → (7, 4.5)
        
        # Point labels
        label_00 = Tex("(0,0)", font_size=36, color=RED).next_to(point_00, DOWN+LEFT, buff=0.3)
        label_01 = Tex("(0,1)", font_size=36, color=GREEN).next_to(point_01, UP+LEFT, buff=0.3)
        label_10 = Tex("(1,0)", font_size=36, color=GREEN).next_to(point_10, DOWN+RIGHT, buff=0.3)
        label_11 = Tex("(1,1)", font_size=36, color=GREEN).next_to(point_11, UP+RIGHT, buff=0.3)
        
        # Linear separating line (separates (0,0) from others)
        line = Line(axes.c2p(-0.2, 3.25), axes.c2p(5.5, -0.2), stroke_width=6, color=YELLOW)
         
    

        
        # Animate creation
        self.play(ShowCreation(axes), self.camera.frame.animate.scale(1.15).shift(LEFT*12.1+DOWN*0.23))
        self.play(ShowCreation(x_tick), ShowCreation(y_tick))
        self.play(Write(x_tick_label), Write(y_tick_label))
        self.play(Write(x1_label), Write(x2_label))
        self.wait(1)
        
        # Add data points
        self.play(
            ShowCreation(point_00), Write(label_00),
            ShowCreation(point_01), Write(label_01),
            ShowCreation(point_10), Write(label_10),
            ShowCreation(point_11), Write(label_11)
        )
        self.wait(2)
        
        # Show separating line
        self.play(ShowCreation(line))

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1/1.15).shift(RIGHT*12.1+UP*0.23))
        self.wait(2)



        # OR gate truth table: output is 1 when at least one input is 1
        table_data = [
            ["x_1", "x_2", "y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "0"]
        ]
        
        # Create truth table with proper alignment
        table_group = VGroup()
        table_center_x = 6.6
        row_height = 0.54
        
        table_group.shift(DOWN*0.3)

        for i, row in enumerate(table_data):
            row_group = VGroup()
            for j, cell in enumerate(row):
                cell_text = Tex(cell, font_size=22, color=WHITE)
                cell_x = table_center_x + (j - 1) * 0.67
                cell_y = 1.5 - i * row_height
                cell_text.move_to(RIGHT * cell_x + UP * cell_y)
                row_group.add(cell_text)
            table_group.add(row_group)
        
        # Scale up the entire table group
        table_group.scale(1.87).shift(RIGHT*2.69+DOWN*0.64)

        title = Text("X-OR Gate", weight=BOLD).next_to(table_group, UP, buff=0.69).set_color(PURPLE_B).scale(1.3)
        self.play(ShowCreation(title))


        self.play(ShowCreation(table_group), self.camera.frame.animate.shift(RIGHT*9.9))
        
        self.wait(2)

        self.play(FadeOut(table_group), FadeOut(title), self.camera.frame.animate.shift(LEFT*9.9))

        # Animate creation
        self.play(FadeOut(axes),run_time=0.02 )
        self.play(FadeOut(x_tick), FadeOut(y_tick),run_time=0.02 )
        self.play(FadeOut(x_tick_label), FadeOut(y_tick_label),run_time=0.02 )
        self.play(FadeOut(x1_label), FadeOut(x2_label),run_time=0.02 )        
        # Add data points
        self.play(
            FadeOut(point_00), FadeOut(label_00),
            FadeOut(point_01), FadeOut(label_01),
            FadeOut(point_10), FadeOut(label_10),
            FadeOut(point_11), FadeOut(label_11),run_time=0.02 
        ) 
        # Show separating line
        self.play(FadeOut(line))  

        
        self.wait()
        self.camera.frame.save_state()



        axes = Axes(
            x_range=[-0.4, 8, 0.1],
            y_range=[-0.4, 5.5, 0.1],
            axis_config={
                "stroke_width": 4,
                "include_tip": True,
                "include_ticks": False,
                "numbers_to_exclude": [0],
            },
        ).shift(LEFT * 12.7)

        # Add ticks at scaled positions (7 represents 1 on x, 4.5 represents 1 on y)
        x_tick = Line(axes.c2p(7, -0.2), axes.c2p(7, 0.2), stroke_width=4, color=WHITE)
        y_tick = Line(axes.c2p(-0.2, 4.5), axes.c2p(0.2, 4.5), stroke_width=4, color=WHITE)

        # Tick labels showing "1" 
        x_tick_label = Tex("1", font_size=36, color=WHITE).next_to(x_tick, DOWN, buff=0.2)
        y_tick_label = Tex("1", font_size=36, color=WHITE).next_to(y_tick, LEFT, buff=0.2)

        # Axis labels
        x1_label = Tex(r"x_1", font_size=48).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        x2_label = Tex(r"x_2", font_size=48).next_to(axes.y_axis.get_end(), UP, buff=0.2)
 
        # OR gate data points with proper scaling
        point_00 = Dot(axes.c2p(0, 0), radius=0.2, color=RED).set_color(RED)        # (0,0) → (0, 0)
        point_01 = Dot(axes.c2p(0, 4.5), radius=0.2, color=GREEN).set_color(GREEN)    # (0,1) → (0, 4.5)
        point_10 = Dot(axes.c2p(7, 0), radius=0.2, color=GREEN).set_color(GREEN)      # (1,0) → (7, 0)
        point_11 = Dot(axes.c2p(7, 4.5), radius=0.2, color=GREEN).set_color(RED)    # (1,1) → (7, 4.5)
        
        # Point labels
        label_00 = Tex("(0,0)", font_size=36, color=RED).next_to(point_00, DOWN+LEFT, buff=0.3)
        label_01 = Tex("(0,1)", font_size=36, color=GREEN).next_to(point_01, UP+LEFT, buff=0.3)
        label_10 = Tex("(1,0)", font_size=36, color=GREEN).next_to(point_10, DOWN+RIGHT, buff=0.3)
        label_11 = Tex("(1,1)", font_size=36, color=GREEN).next_to(point_11, UP+RIGHT, buff=0.3)
        
        # Linear separating line (separates (0,0) from others)
        line = Line(axes.c2p(-0.2, 3.25), axes.c2p(5.5, -0.2), stroke_width=6, color=YELLOW)
         
    
        # Animate creation
        self.play(ShowCreation(axes), self.camera.frame.animate.scale(1.15).shift(LEFT*12.1+DOWN*0.23))
        self.play(ShowCreation(x_tick), ShowCreation(y_tick))
        self.play(Write(x_tick_label), Write(y_tick_label))
        self.play(Write(x1_label), Write(x2_label))
        self.wait(1)
        
        # Add data points
        self.play(
            ShowCreation(point_00), Write(label_00),
            ShowCreation(point_01), Write(label_01),
            ShowCreation(point_10), Write(label_10),
            ShowCreation(point_11), Write(label_11)
        )
        self.wait(2)
        
        # Show separating line
        self.play(ShowCreation(line))
        self.wait(2)


        self.play(Transform(line, Line(axes.c2p(-0.4, 5.25), axes.c2p(3.5, -0.2), stroke_width=6, color=YELLOW) ))
        self.play(Transform(line, Line(axes.c2p(-0.4, 2.25), axes.c2p(7.5, 2.25), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(3.5, -0.4), axes.c2p(3.5, 5.2), stroke_width=6, color=YELLOW)))        
        self.play(Transform(line, Line(axes.c2p(1, -0.4), axes.c2p(6, 5.2), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(6, -0.4), axes.c2p(1, 5.2), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(-0.4, 3.5), axes.c2p(7.5, 3.5), stroke_width=6, color=YELLOW)))
        self.play(Transform(line, Line(axes.c2p(-0.4, 1), axes.c2p(7.5, 1), stroke_width=6, color=YELLOW)))

        # Final frustrated attempt - make line blink/flash
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        self.play(line.animate.set_color(RED), run_time=0.3)
        self.play(line.animate.set_color(YELLOW), run_time=0.3)
        


        # Two diagonal lines with extended ranges
        diag_line1 = Line(axes.c2p(-1, 5.5), axes.c2p(9, -0.8), stroke_width=6, color=YELLOW).shift(UP*0.34)
        diag_line2 = Line(axes.c2p(-0.8, 3.5), axes.c2p(7.5, -1.4), stroke_width=6, color=YELLOW)
        
        # Transform existing line into first diagonal line
        self.play(Transform(line, diag_line1), ShowCreation(diag_line2), run_time=1.5)
        self.wait(2)

        self.play(self.camera.frame.animate.restore())

        # Animate creation
        self.play(FadeOut(axes),run_time=0.02 )
        self.play(FadeOut(x_tick), FadeOut(y_tick),run_time=0.02 )
        self.play(FadeOut(x_tick_label), FadeOut(y_tick_label),run_time=0.02 )
        self.play(FadeOut(x1_label), FadeOut(x2_label),run_time=0.02 )        
        # Add data points
        self.play(
            FadeOut(point_00), FadeOut(label_00),
            FadeOut(point_01), FadeOut(label_01),
            FadeOut(point_10), FadeOut(label_10),
            FadeOut(point_11), FadeOut(label_11),run_time=0.02 
        ) 
        # Show separating line
        self.play(FadeOut(line))      
        self.wait(2)




        # Group all current neuron-related elements for shifting
        current_neuron_group = VGroup(
            neuron, phi_in_neuron, 
            output_arrow, y, 
            bias_arrow, bias
        )
        
        # Shift the entire group to the right
        self.play(
            Uncreate(line1), Uncreate(line2),
            Uncreate(weight_1), Uncreate(weight_2),
            run_time=1
        )

        self.play(current_neuron_group.animate.shift(RIGHT * 3), self.camera.frame.animate.shift(RIGHT))

        self.wait(1)
        
        # Create two hidden layer neurons with ReLU text
        hidden1 = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=6, stroke_color=BLUE_B)
        hidden2 = Circle(radius=0.6, color=BLUE, fill_opacity=1, stroke_width=6, stroke_color=BLUE_B)
        hidden1.move_to(LEFT * 0.5 + UP * 1.2)
        hidden2.move_to(LEFT * 0.5 + DOWN * 1.2)
        
        # ReLU text inside hidden neurons (black color)
        relu1_text = Tex("ReLU", font_size=34, color=BLACK).move_to(hidden1.get_center()).set_color(BLACK)
        relu2_text = Tex("ReLU", font_size=34, color=BLACK).move_to(hidden2.get_center()).set_color(BLACK)
        
        # Change output neuron text to ReLU
        relu_output_text = Tex("ReLU", font_size=42, color=BLACK).move_to(neuron.get_center()).set_color(BLACK)
        
        self.play(
            GrowFromCenter(hidden1), GrowFromCenter(hidden2),
        )
        self.play(GrowFromCenter(relu1_text), GrowFromCenter(relu2_text), Transform(phi_in_neuron, relu_output_text))

        
        # Create connections from inputs to hidden layer
        line_x1_h1 = Line(input1.get_center(), hidden1.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x1_h2 = Line(input1.get_center(), hidden2.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x2_h1 = Line(input2.get_center(), hidden1.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_x2_h2 = Line(input2.get_center(), hidden2.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        
        # Create connections from hidden layer to output
        line_h1_out = Line(hidden1.get_center(), neuron.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        line_h2_out = Line(hidden2.get_center(), neuron.get_center(), stroke_width=4, z_index=-1, color=WHITE)
        
        self.play(
            ShowCreation(line_x1_h1), ShowCreation(line_x1_h2),
            ShowCreation(line_x2_h1), ShowCreation(line_x2_h2),
            ShowCreation(line_h1_out), ShowCreation(line_h2_out)
        )
        
        # Add bias arrows for hidden layer
        bias_arrow_h1 = Arrow(UP * 3 + LEFT * 0.5, hidden1.get_top() + UP * 0.1, stroke_width=3, color=PURPLE).set_color(PURPLE)
        bias_arrow_h2 = Arrow(DOWN * 3 + LEFT * 0.5, hidden2.get_bottom() + DOWN * 0.1, stroke_width=3, color=PURPLE).set_color(PURPLE)
        
        self.play(ShowCreation(bias_arrow_h1), ShowCreation(bias_arrow_h2), self.camera.frame.animate.shift(DOWN*0.25).scale(1.02))
        
        # XOR solution weights and biases
        # Hidden layer 1: w1=1, w2=1, b=-0.5 (OR gate)
        # Hidden layer 2: w1=1, w2=1, b=-1.5 (AND gate with high threshold)
        # Output layer: w1=1, w2=-2, b=0 (h1 - 2*h2)
        
        # Weight labels for input to hidden layer 1
        w11_label = Text("1", font_size=32, color=RED).move_to(line_x1_h1.get_center() + UP * 0.3 + LEFT * 0.2)
        w21_label = Text("1", font_size=32, color=RED).move_to(line_x2_h1.get_center() + DOWN * 0.3 + LEFT * 0.2).shift(DOWN*0.13+RIGHT*0.1)
        
        # Weight labels for input to hidden layer 2  
        w12_label = Text("1", font_size=32, color=RED).move_to(line_x1_h2.get_center() + DOWN * 0.3 + LEFT * 0.2).shift(LEFT*0.13+UP*0.26)
        w22_label = Text("1", font_size=32, color=RED).move_to(line_x2_h2.get_center() + UP * 0.3 + LEFT * 0.2)
        
        # Weight labels for hidden to output
        w_h1_out = Text("1", font_size=32, color=RED).move_to(line_h1_out.get_center() + UP * 0.3)
        w_h2_out = Text("-2", font_size=32, color=RED).move_to(line_h2_out.get_center() + DOWN * 0.3)
        
        # Bias labels
        b1_label = Text("0", font_size=52, color=PURPLE).next_to(bias_arrow_h1.get_start(), UP, buff=0.2)
        b2_label = Text("-1", font_size=52, color=PURPLE).next_to(bias_arrow_h2.get_start(), DOWN, buff=0.2)
        
        # Transform output bias to number
        output_bias_label = Text("0", font_size=52, color=PURPLE).move_to(bias.get_center())
        
        self.play(
            Write(w11_label), Write(w21_label),
            Write(w12_label), Write(w22_label),
            Write(w_h1_out), Write(w_h2_out),
            Write(b1_label), Write(b2_label),
            Transform(bias, output_bias_label)
        )

        self.wait(2)

        self.camera.frame.save_state()
        
        self.play(
            Transform(x1, Text("1", font_size=60).move_to(x1)),
            Transform(x2, Text("1", font_size=60).move_to(x2)),
            )
        
        self.wait(2)

        # Data flow animation for multi-layer perceptron
        def create_pulse(start_point, end_point, color=YELLOW, duration=1.5):
            pulse = Dot(radius=0.15, color=color, fill_opacity=0.9)
            pulse.move_to(start_point)
            glow = Circle(radius=0.3, color=color, fill_opacity=0.3, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        # Create pulses from inputs to hidden layer
        pulse_x1_h1, glow_x1_h1 = create_pulse(input1.get_center(), hidden1.get_center(), color=YELLOW)
        pulse_x1_h2, glow_x1_h2 = create_pulse(input1.get_center(), hidden2.get_center(), color=YELLOW)
        pulse_x2_h1, glow_x2_h1 = create_pulse(input2.get_center(), hidden1.get_center(), color=ORANGE)
        pulse_x2_h2, glow_x2_h2 = create_pulse(input2.get_center(), hidden2.get_center(), color=ORANGE)
        
        # Create bias pulses for hidden layer
        pulse_bias_h1, glow_bias_h1 = create_pulse(bias_arrow_h1.get_start(), hidden1.get_center(), color=PURPLE)
        pulse_bias_h2, glow_bias_h2 = create_pulse(bias_arrow_h2.get_start(), hidden2.get_center(), color=PURPLE)
        
        # Add all input pulses
        self.add(pulse_x1_h1, glow_x1_h1, pulse_x1_h2, glow_x1_h2,
                 pulse_x2_h1, glow_x2_h1, pulse_x2_h2, glow_x2_h2,
                 pulse_bias_h1, glow_bias_h1, pulse_bias_h2, glow_bias_h2)
        
        # Animate pulses moving to hidden layer
        self.play(
            pulse_x1_h1.animate.move_to(hidden1.get_center()),
            glow_x1_h1.animate.move_to(hidden1.get_center()),
            pulse_x2_h1.animate.move_to(hidden1.get_center()),
            glow_x2_h1.animate.move_to(hidden1.get_center()),
            pulse_bias_h1.animate.move_to(hidden1.get_center()),
            glow_bias_h1.animate.move_to(hidden1.get_center()),
            
            pulse_x1_h2.animate.move_to(hidden2.get_center()),
            glow_x1_h2.animate.move_to(hidden2.get_center()),
            pulse_x2_h2.animate.move_to(hidden2.get_center()),
            glow_x2_h2.animate.move_to(hidden2.get_center()),
            pulse_bias_h2.animate.move_to(hidden2.get_center()),
            glow_bias_h2.animate.move_to(hidden2.get_center()),
            run_time=1.2
        )
        
        # Hidden layer neurons activate
        self.play(
            hidden1.animate.set_fill(YELLOW, opacity=1),
            hidden2.animate.set_fill(YELLOW, opacity=1),
            FadeOut(pulse_x1_h1), FadeOut(glow_x1_h1),
            FadeOut(pulse_x2_h1), FadeOut(glow_x2_h1),
            FadeOut(pulse_bias_h1), FadeOut(glow_bias_h1),
            FadeOut(pulse_x1_h2), FadeOut(glow_x1_h2),
            FadeOut(pulse_x2_h2), FadeOut(glow_x2_h2),
            FadeOut(pulse_bias_h2), FadeOut(glow_bias_h2),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Create pulses from hidden layer to output
        pulse_h1_out, glow_h1_out = create_pulse(hidden1.get_center(), neuron.get_center(), color=GREEN)
        pulse_h2_out, glow_h2_out = create_pulse(hidden2.get_center(), neuron.get_center(), color=GREEN)
        
        # Create output bias pulse
        pulse_bias_out, glow_bias_out = create_pulse(bias_arrow.get_start(), neuron.get_center(), color=PURPLE)
        
        # Add output pulses
        self.add(pulse_h1_out, glow_h1_out, pulse_h2_out, glow_h2_out,
                 pulse_bias_out, glow_bias_out)
        
        # Animate pulses moving to output
        self.play(
            pulse_h1_out.animate.move_to(neuron.get_center()),
            glow_h1_out.animate.move_to(neuron.get_center()),
            pulse_h2_out.animate.move_to(neuron.get_center()),
            glow_h2_out.animate.move_to(neuron.get_center()),
            pulse_bias_out.animate.move_to(neuron.get_center()),
            glow_bias_out.animate.move_to(neuron.get_center()),
            run_time=1.2
        )
        
        # Output neuron activates and hidden layers return to blue
        self.play(
            neuron.animate.set_fill(YELLOW, opacity=1),
            hidden1.animate.set_fill(BLUE, opacity=1),
            hidden2.animate.set_fill(BLUE, opacity=1),
            FadeOut(pulse_h1_out), FadeOut(glow_h1_out),
            FadeOut(pulse_h2_out), FadeOut(glow_h2_out),
            FadeOut(pulse_bias_out), FadeOut(glow_bias_out),
            run_time=0.8
        )
        
        # Show final output value
        self.play(Transform(y, Text("0", font_size=60, color=GREEN).move_to(y)))
        
        # Reset neuron back to blue
        self.play(neuron.animate.set_fill(BLUE, opacity=1))
        

        h1_eq = Tex(r"h_1 \ = \ ReLU(1 \cdot x_1 + 1 \cdot x_2 + 0)", font_size=54).shift(RIGHT*12.33+UP*0.8)
        
        # Hidden layer 2 equation  
        h2_eq = Tex(r"h_2 \  =  ReLU(1 \cdot x_1 + 1 \cdot x_2 + (-1))", font_size=54)
        h2_eq.next_to(h1_eq, DOWN, buff=0.8)

        self.play(
          Write(h1_eq),
          Write(h2_eq), 
          self.camera.frame.animate.shift(RIGHT*12)
                      )
        
        self.wait(2)

        self.play(
            Transform(h1_eq,  Tex(r"h_1 \ = \ ReLU(1 \cdot 1 + 1 \cdot 1 + 0)", font_size=54).move_to(h1_eq)),
            Transform(h2_eq, Tex(r"h_2 \  =  ReLU(1 \cdot 1 + 1 \cdot 1 + (-1))", font_size=54).move_to(h2_eq)),
        )

        self.wait(2)

        self.play(
            Transform(h1_eq,  Tex(r"h_1 \ = \ 2", font_size=74).move_to(h1_eq)),
            Transform(h2_eq, Tex(r"h_2 \  = \ 1", font_size=74).move_to(h2_eq)),
        )

        self.play()

        hhh = Tex(r"y \ = \ ReLU(1 \cdot h_1 + (-2) \cdot h_2 + 0)", font_size=54).move_to(Group(h1_eq, h2_eq))

        self.play(ReplacementTransform(VGroup(h1_eq, h2_eq), hhh))

        self.wait(2)

        self.play(Transform(hhh, Tex(r"y \ = \ ReLU(1 \cdot 2 + (-2) \cdot 1 + 0)", font_size=74).move_to(hhh)))

        self.wait(2)

        self.play(Transform(hhh, Tex(r"y \ = \ 0", font_size=94).move_to(hhh)))
        self.wait(2)
        

        self.play(FadeOut(hhh), self.camera.frame.animate.restore())

        self.wait(2)

        self.play(
            Transform(x1, Text("1", font_size=60).move_to(x1)),
            Transform(x2, Text("0", font_size=60).move_to(x2)),
            Transform(y, Text("1", font_size=60).move_to(y)),
            
            )
        self.wait()
    
        self.play(
            Transform(x1, Text("0", font_size=60).move_to(x1)),
            Transform(x2, Text("0", font_size=60).move_to(x2)),
            Transform(y, Text("0", font_size=60).move_to(y)),
            
            )
        

        self.wait(2)



class NeuralNetworkFlow(Scene):
    def construct(self):
        self.camera.frame.scale(1.18)
        
        # Create 5 input layer nodes (GREEN, radius=0.36)
        input_layer = []
        input_labels = []
        for i in range(5):
            node = Circle(radius=0.36, color=GREEN, fill_opacity=1, stroke_width=6, stroke_color=GREEN_B)
            node.move_to(LEFT * 6 + UP * (2.5 - i * 1.2))
            input_layer.append(node)
            
            # Add input labels with black color
            label = Tex(f"x_{{{i+1}}}").set_color(BLACK).scale(0.7)
            label.move_to(node.get_center())
            input_labels.append(label)
        
        # Create hidden layer 1 with 4 neurons
        hidden_layer1 = []
        hidden_labels1 = []
        for i in range(4):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(LEFT * 3 + UP * (2.4 - i * 1.6))
            hidden_layer1.append(node)
            
            # Standard notation: A(Z^[1]_i)
            label = Tex(f"A(Z^{{[1]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels1.append(label)
        
        # Create hidden layer 2 with 5 neurons (reduced from 6)
        hidden_layer2 = []
        hidden_labels2 = []
        for i in range(5):  # Changed from 6 to 5
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(ORIGIN + UP * (3.2 - i * 1.6))  # Adjusted positioning for 5 neurons
            hidden_layer2.append(node)
            
            # Standard notation: A(Z^[2]_i)
            label = Tex(f"A(Z^{{[2]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels2.append(label)
        
        # Create hidden layer 3 with 3 neurons
        hidden_layer3 = []
        hidden_labels3 = []
        for i in range(3):
            node = Circle(radius=0.5, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
            node.move_to(RIGHT * 3 + UP * (1.6 - i * 1.6))
            hidden_layer3.append(node)
            
            # Standard notation: A(Z^[3]_i)
            label = Tex(f"A(Z^{{[3]}}_{{{i+1}}})").set_color(BLACK).scale(0.45)
            label.move_to(node.get_center())
            hidden_labels3.append(label)
        
        # Create output layer
        output_node = Circle(radius=0.72, color=BLUE_C, fill_opacity=1, stroke_width=8, stroke_color=BLUE_B)
        output_node.move_to(RIGHT * 6)
        
        # Add output label scaled by 1.8
        output_label = Tex("\\hat{y}").set_color(BLACK).scale(1.8)
        output_label.move_to(output_node.get_center())
        
        # Create all connections
        connections = []
        
        # Input to Hidden Layer 1
        for input_node in input_layer:
            for hidden_node in hidden_layer1:
                line = Line(input_node.get_center(), hidden_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 1 to Hidden Layer 2
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                line = Line(h1_node.get_center(), h2_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 2 to Hidden Layer 3
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                line = Line(h2_node.get_center(), h3_node.get_center(), 
                          stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
                connections.append(line)
        
        # Hidden Layer 3 to Output
        for h3_node in hidden_layer3:
            line = Line(h3_node.get_center(), output_node.get_center(), 
                      stroke_width=2, color=GREY_A, z_index=-1, stroke_opacity=0.6)
            connections.append(line)
        
        # Store original line properties (ADD THIS RIGHT AFTER CREATING CONNECTIONS)
        original_stroke_widths = [line.stroke_width for line in connections]
        original_colors = [line.get_color() for line in connections]
        
        # Show the network structure
        all_nodes = input_layer + hidden_layer1 + hidden_layer2 + hidden_layer3 + [output_node]
        
        self.play(*[ShowCreation(node) for node in all_nodes])
        self.play(*[ShowCreation(line) for line in connections])
        self.wait(1.5)

        # Write input labels first
        self.play(*[Write(label) for label in input_labels])
        self.wait(1)
        
        # Enhanced pulse creation function
        def create_pulse(start_point, color):
            pulse = Dot(radius=0.12, color=color, fill_opacity=1)
            pulse.move_to(start_point)
            glow = Circle(radius=0.25, color=color, fill_opacity=0.3, stroke_opacity=0)
            glow.move_to(start_point)
            return pulse, glow
        
        # SINGLE ITERATION WITH ONE PULSE PER WEIGHT CONNECTION
        
        # Stage 1: Input to Hidden Layer 1 (5×4 = 20 pulses)
        input_pulses = []
        input_glows = []

        # Get the specific connections for this stage
        input_to_h1_connections = []
        for input_node in input_layer:
            for h1_node in hidden_layer1:
                for line in connections:
                    start_pos = line.get_start()
                    input_pos = input_node.get_center()
                    h1_pos = h1_node.get_center()
                    if (abs(start_pos[0] - input_pos[0]) < 0.1 and abs(start_pos[1] - input_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h1_pos[0]) < 0.1 and abs(end_pos[1] - h1_pos[1]) < 0.1):
                            input_to_h1_connections.append(line)

        for input_node in input_layer:
            for h1_node in hidden_layer1:
                pulse, glow = create_pulse(input_node.get_center(), "#ff0000")
                input_pulses.append(pulse)
                input_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its specific weight connection AND color the connections
        h1_animations = []
        for i, (pulse, glow) in enumerate(zip(input_pulses, input_glows)):
            input_idx = i // len(hidden_layer1)
            h1_idx = i % len(hidden_layer1)
            target_pos = hidden_layer1[h1_idx].get_center()
            
            h1_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in input_to_h1_connections:
            h1_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h1_animations, run_time=1.5)
        
        # Fade out and write h1 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in input_pulses])
        reset_animations.extend([FadeOut(glow) for glow in input_glows])
        reset_animations.extend([Write(label) for label in hidden_labels1])

        # Reset connection colors and widths
        for line in input_to_h1_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 2: Hidden Layer 1 to Hidden Layer 2 (4×5 = 20 pulses)
        h1_pulses = []
        h1_glows = []

        # Get the specific connections for this stage
        h1_to_h2_connections = []
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                for line in connections:
                    start_pos = line.get_start()
                    h1_pos = h1_node.get_center()
                    h2_pos = h2_node.get_center()
                    if (abs(start_pos[0] - h1_pos[0]) < 0.1 and abs(start_pos[1] - h1_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h2_pos[0]) < 0.1 and abs(end_pos[1] - h2_pos[1]) < 0.1):
                            h1_to_h2_connections.append(line)
        
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                pulse, glow = create_pulse(h1_node.get_center(), "#ff0000")
                h1_pulses.append(pulse)
                h1_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its weight connection AND color the connections
        h2_animations = []
        for i, (pulse, glow) in enumerate(zip(h1_pulses, h1_glows)):
            h1_idx = i // len(hidden_layer2)
            h2_idx = i % len(hidden_layer2)
            target_pos = hidden_layer2[h2_idx].get_center()
            
            h2_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in h1_to_h2_connections:
            h2_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h2_animations, run_time=1.5)
        
        # Fade out and write h2 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h1_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h1_glows])
        reset_animations.extend([Write(label) for label in hidden_labels2])

        # Reset connection colors and widths
        for line in h1_to_h2_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 3: Hidden Layer 2 to Hidden Layer 3 (5×3 = 15 pulses)
        h2_pulses = []
        h2_glows = []

        # Get the specific connections for this stage
        h2_to_h3_connections = []
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                for line in connections:
                    start_pos = line.get_start()
                    h2_pos = h2_node.get_center()
                    h3_pos = h3_node.get_center()
                    if (abs(start_pos[0] - h2_pos[0]) < 0.1 and abs(start_pos[1] - h2_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h3_pos[0]) < 0.1 and abs(end_pos[1] - h3_pos[1]) < 0.1):
                            h2_to_h3_connections.append(line)
        
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                pulse, glow = create_pulse(h2_node.get_center(), "#ff0000")
                h2_pulses.append(pulse)
                h2_glows.append(glow)
                self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move each pulse along its weight connection AND color the connections
        h3_animations = []
        for i, (pulse, glow) in enumerate(zip(h2_pulses, h2_glows)):
            h2_idx = i // len(hidden_layer3)
            h3_idx = i % len(hidden_layer3)
            target_pos = hidden_layer3[h3_idx].get_center()
            
            h3_animations.extend([
                pulse.animate.move_to(target_pos),
                glow.animate.move_to(target_pos)
            ])

        # Add connection coloring animations
        for line in h2_to_h3_connections:
            h3_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*h3_animations, run_time=1.5)
        
        # Fade out and write h3 labels AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h2_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h2_glows])
        reset_animations.extend([Write(label) for label in hidden_labels3])

        # Reset connection colors and widths
        for line in h2_to_h3_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        # Stage 4: Hidden Layer 3 to Output (3×1 = 3 pulses)
        h3_pulses = []
        h3_glows = []

        # Get the specific connections for this stage
        h3_to_output_connections = []
        for h3_node in hidden_layer3:
            for line in connections:
                start_pos = line.get_start()
                h3_pos = h3_node.get_center()
                output_pos = output_node.get_center()
                if (abs(start_pos[0] - h3_pos[0]) < 0.1 and abs(start_pos[1] - h3_pos[1]) < 0.1):
                    end_pos = line.get_end()
                    if (abs(end_pos[0] - output_pos[0]) < 0.1 and abs(end_pos[1] - output_pos[1]) < 0.1):
                        h3_to_output_connections.append(line)
        
        for h3_node in hidden_layer3:
            pulse, glow = create_pulse(h3_node.get_center(), "#ff0000")
            h3_pulses.append(pulse)
            h3_glows.append(glow)
            self.add(pulse, glow)
        
        self.wait(0.3)
        
        # Move to output AND color the connections
        output_animations = []
        for pulse, glow in zip(h3_pulses, h3_glows):
            output_animations.extend([
                pulse.animate.move_to(output_node.get_center()),
                glow.animate.move_to(output_node.get_center())
            ])

        # Add connection coloring animations
        for line in h3_to_output_connections:
            output_animations.append(line.animate.set_stroke(width=5, color="#ff0000"))
        
        self.play(*output_animations, run_time=1.5)
        
        # Fade out and write output label AND reset connection colors
        reset_animations = []
        reset_animations.extend([FadeOut(pulse) for pulse in h3_pulses])
        reset_animations.extend([FadeOut(glow) for glow in h3_glows])
        reset_animations.append(Write(output_label))

        # Reset connection colors and widths
        for line in h3_to_output_connections:
            line_idx = connections.index(line)
            reset_animations.append(
                line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                      color=original_colors[line_idx])
            )

        self.play(*reset_animations, run_time=1.0)
        
        self.wait(3)

        self.camera.frame.save_state()
        self.camera.frame.restore()

        self.play(self.camera.frame.animate.scale(0.5).shift(LEFT*4))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT+UP*1.33).scale(0.8))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*3), run_time=3.6)

        self.wait()

        self.play(self.camera.frame.animate.shift(RIGHT*3+UP*3.8), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate.shift(DOWN*4.44), run_time=5)
        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*3.7+UP*2.77))
        self.wait()
        self.play(self.camera.frame.animate.shift(DOWN), run_time=2)
        self.wait()

        self.play(self.camera.frame.animate.shift(RIGHT+UP*0.55))
        self.wait(2)

        self.play(self.camera.frame.animate.restore().scale(1.14).shift(DOWN*0.8))
        
        a = Text("Input layer", weight=BOLD).next_to(input_layer[4], DOWN).scale(1.2).shift(DOWN*0.45)
        b = Text("Hidden layers", weight=BOLD).next_to(hidden_layer2[4], DOWN).scale(1.3).shift(DOWN*0.55)
        c = Text("Output layer", weight=BOLD).next_to(output_node, DOWN).scale(1.15).shift(DOWN*0.44)

        self.play(ShowCreation(a), Write(b), Write(c))

        self.wait(2)

        self.play(self.camera.frame.animate.restore() , FadeOut(a), FadeOut(b), FadeOut(c))
        self.wait(2)

        import random

        # After self.play(*[ShowCreation(line) for line in connections])
        # Add random flickering effect
        flicker_colors = [YELLOW, GREEN, PURPLE, ORANGE, PINK, BLUE, RED, TEAL, DARK_BROWN, GREY_B]
        
        # Start random flickering
        for line in connections:
            line.add_updater(lambda mob: mob.set_color(random.choice(flicker_colors)))
        
        self.wait(10)  # Flicker for 10 seconds
        
        # Stop flickering and restore original colors
        for line, original in zip(connections, original_colors):
            line.clear_updaters()
            line.set_color(original)

        self.wait(2)

        # Add this code directly inside your construct() method after the forward propagation animation
        PURPLE_HEX = "#ff0000"
        PURE_GREEN_HEX = "#8A2BE2"
        
        # Organize connections by layer pairs for sequential animation
        layer_connections = []
        
        # Input to Hidden Layer 1 connections
        input_to_h1 = []
        for input_node in input_layer:
            for h1_node in hidden_layer1:
                for line in connections:
                    start_pos = line.get_start()
                    input_pos = input_node.get_center()
                    h1_pos = h1_node.get_center()
                    if (abs(start_pos[0] - input_pos[0]) < 0.1 and abs(start_pos[1] - input_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h1_pos[0]) < 0.1 and abs(end_pos[1] - h1_pos[1]) < 0.1):
                            input_to_h1.append(line)
        
        # Hidden Layer 1 to Hidden Layer 2 connections
        h1_to_h2 = []
        for h1_node in hidden_layer1:
            for h2_node in hidden_layer2:
                for line in connections:
                    start_pos = line.get_start()
                    h1_pos = h1_node.get_center()
                    h2_pos = h2_node.get_center()
                    if (abs(start_pos[0] - h1_pos[0]) < 0.1 and abs(start_pos[1] - h1_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h2_pos[0]) < 0.1 and abs(end_pos[1] - h2_pos[1]) < 0.1):
                            h1_to_h2.append(line)
        
        # Hidden Layer 2 to Hidden Layer 3 connections
        h2_to_h3 = []
        for h2_node in hidden_layer2:
            for h3_node in hidden_layer3:
                for line in connections:
                    start_pos = line.get_start()
                    h2_pos = h2_node.get_center()
                    h3_pos = h3_node.get_center()
                    if (abs(start_pos[0] - h2_pos[0]) < 0.1 and abs(start_pos[1] - h2_pos[1]) < 0.1):
                        end_pos = line.get_end()
                        if (abs(end_pos[0] - h3_pos[0]) < 0.1 and abs(end_pos[1] - h3_pos[1]) < 0.1):
                            h2_to_h3.append(line)
        
        # Hidden Layer 3 to Output connections
        h3_to_output = []
        for h3_node in hidden_layer3:
            for line in connections:
                start_pos = line.get_start()
                h3_pos = h3_node.get_center()
                output_pos = output_node.get_center()
                if (abs(start_pos[0] - h3_pos[0]) < 0.1 and abs(start_pos[1] - h3_pos[1]) < 0.1):
                    end_pos = line.get_end()
                    if (abs(end_pos[0] - output_pos[0]) < 0.1 and abs(end_pos[1] - output_pos[1]) < 0.1):
                        h3_to_output.append(line)
        
        # Repeat forward-backward cycle 3 times
        for cycle in range(3):
            
            # FORWARD PROPAGATION - Layer by layer
            layer_groups = [input_to_h1, h1_to_h2, h2_to_h3, h3_to_output]
            
            for layer_lines in layer_groups:
                # Create pulses for this layer's connections
                layer_pulses = []
                layer_glows = []
                
                for line in layer_lines:
                    pulse, glow = create_pulse(line.get_start(), PURPLE_HEX)
                    layer_pulses.append(pulse)
                    layer_glows.append(glow)
                    self.add(pulse, glow)
                
                # Move pulses and change line properties simultaneously
                forward_animations = []
                for i, (pulse, glow, line) in enumerate(zip(layer_pulses, layer_glows, layer_lines)):
                    forward_animations.extend([
                        pulse.animate.move_to(line.get_end()),
                        glow.animate.move_to(line.get_end()),
                        line.animate.set_stroke(width=5, color=PURPLE_HEX)
                    ])
                
                self.play(*forward_animations, run_time=1.0)
                
                # Fade out pulses and reset line properties
                fadeout_animations = []
                for pulse, glow in zip(layer_pulses, layer_glows):
                    fadeout_animations.extend([FadeOut(pulse), FadeOut(glow)])
                
                for line in layer_lines:
                    line_idx = connections.index(line)
                    fadeout_animations.append(
                        line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                              color=original_colors[line_idx])
                    )
                
                self.play(*fadeout_animations, run_time=0.3)
            
            self.wait(0.5)
            
            # BACKPROPAGATION - Layer by layer (reverse order)
            reverse_layer_groups = [h3_to_output, h2_to_h3, h1_to_h2, input_to_h1]
            
            for layer_lines in reverse_layer_groups:
                # Create pulses for this layer's connections (starting from end)
                layer_pulses = []
                layer_glows = []
                
                for line in layer_lines:
                    pulse, glow = create_pulse(line.get_end(), PURE_GREEN_HEX)
                    layer_pulses.append(pulse)
                    layer_glows.append(glow)
                    self.add(pulse, glow)
                
                # Move pulses backward and change line properties
                backward_animations = []
                for pulse, glow, line in zip(layer_pulses, layer_glows, layer_lines):
                    backward_animations.extend([
                        pulse.animate.move_to(line.get_start()),
                        glow.animate.move_to(line.get_start()),
                        line.animate.set_stroke(width=6, color=PURE_GREEN_HEX)
                    ])
                
                self.play(*backward_animations, run_time=1.0)
                
                # Fade out pulses and reset line properties
                fadeout_animations = []
                for pulse, glow in zip(layer_pulses, layer_glows):
                    fadeout_animations.extend([FadeOut(pulse), FadeOut(glow)])
                
                for line in layer_lines:
                    line_idx = connections.index(line)
                    fadeout_animations.append(
                        line.animate.set_stroke(width=original_stroke_widths[line_idx], 
                                              color=original_colors[line_idx])
                    )
                
                self.play(*fadeout_animations, run_time=0.3)
            
            self.wait(0.5)
        
        self.wait(3)

class Brain(Scene):

    def construct(self):

        brain = ImageMobject("brain.png")

        self.play(GrowFromCenter(brain))

        self.wait(1)

        a = Text("Decision Making", weight=BOLD).next_to(brain, LEFT).shift(UP*2.5+RIGHT*0.45)
        self.play(Write(a))
        b = Text("Consciousness", weight=BOLD).next_to(brain, RIGHT).shift(UP*2.5+RIGHT*0.45)
        self.play(Write(b))    

        c = Text("Intelligence", weight=BOLD).next_to(a, DOWN).shift(DOWN*0.65+LEFT*0.14)
        self.play(Write(c))  

        d = Text("Empathy", weight=BOLD).next_to(b, DOWN).shift(DOWN*0.75)
        self.play(Write(d))  

        self.wait(3)

        self.play(self.camera.frame.animate.shift(DOWN*0.86), FadeOut(VGroup(a,b,c,d)))
        
        text = Text("Can We Mimic It ?", weight=BOLD).next_to(brain, DOWN).scale(2).shift(DOWN*0.86)
        self.play(GrowFromCenter(text))

        self.wait(2)

