from manimlib import *

class TCPIPModelAnimation(Scene):
    def construct(self):
        # Define colors for each layer
        colors = [
            "#E74C3C",  # Application - Red
            "#2ECC71",  # Transport - Green
            "#3498DB",  # Internet - Blue
            "#95A5A6",  # Network Interface - Gray
        ]
        
        # Layer names and descriptions
        layer_names = [
            "Application Layer (4)",
            "Transport Layer (3)",
            "Internet Layer (2)",
            "Network Interface Layer (1)"
        ]
        
        # Shorter, more vertically-oriented descriptions with frequent line breaks
        layer_descriptions = [
            "Function:\nCombines functionality of\nOSI Application, Presentation,\nand Session layers.\nProvides interface between\nuser applications and\nthe network stack.",
            "Function:\nEnsures complete data\ntransfer with error recovery.\nResponsible for segmentation,\nflow control, and\nend-to-end error correction.",
            "Function:\nHandles routing of packets\nacross different networks.\nManages logical addressing,\npacket forwarding, and\nfragmentation/reassembly.",
            "Function:\nCombines OSI Physical and\nData Link layers.\nManages physical connections,\nframes data for transmission,\nand handles physical addressing."
        ]
        
        # Protocol examples with more line breaks
        protocol_examples = [
            "Common Protocols:\n• HTTP/HTTPS (Web)\n• FTP (File transfers)\n• SMTP/POP3/IMAP (Email)\n• DNS (Name resolution)\n• Telnet, SSH (Remote access)",
            "Common Protocols:\n• TCP\n  (Connection-oriented)\n• UDP (Connectionless)\n• SCTP (Combined features)\n• QUIC (Quick UDP\n  Internet Connections)",
            "Common Protocols:\n• IPv4 and IPv6\n  (Internet addressing)\n• ICMP (Error reporting)\n• IGMP (Multicast)\n• IPsec (Security)\n• ARP (Address Resolution)",
            "Common Standards:\n• Ethernet (LAN)\n• Wi-Fi (802.11)\n• PPP (Point-to-point)\n• DSL, DOCSIS (Broadband)\n• Bluetooth, NFC\n• Fiber standards"
        ]
        
        # Create rectangles for layers
        layer_height = 1.2  # Increased height for fewer layers
        layer_width = 6
        layers = []
        layer_labels = []
        
        # Create the stack of layers
        for i in range(4):  # 4 layers for TCP/IP
            rect = Rectangle(
                height=layer_height,
                width=layer_width,
                fill_opacity=1.0,
                fill_color=colors[i],
                stroke_color=WHITE
            )
            rect.shift(DOWN * (i - 1.5) * layer_height)  # Center the 4 layers
            
            label = Text(layer_names[i], font="Arial")
            label.scale(0.6)
            label.move_to(rect)
            
            layers.append(rect)
            layer_labels.append(label)
        
        # Group all layers together
        all_layers = VGroup(*layers)
        # Position the TCP/IP model stack on the left side
        all_layers.shift(LEFT * 2.5)
        
        # Shift all layer labels too
        for label in layer_labels:
            label.shift(LEFT * 2.5)
        
        # Create layer explanations and protocol examples (to be shown later)
        explanations = []
        protocols = []
        
        # Create a fixed position for explanations on the right side
        explanation_area = RIGHT * 4 + UP * 1.5
        
        for i in range(4):  # 4 layers for TCP/IP
            # Create multi-line text for explanations
            explanation_lines = layer_descriptions[i].split('\n')
            explanation_group = VGroup()
            
            for j, line in enumerate(explanation_lines):
                line_text = Text(line, font="Arial")
                line_text.scale(0.5)
                if j > 0:
                    line_text.next_to(explanation_group[-1], DOWN, buff=0.15)
                    line_text.align_to(explanation_group[0], LEFT)
                explanation_group.add(line_text)
            
            # Position all explanations at the same fixed location on right side
            explanation_group.move_to(explanation_area).shift(RIGHT*0.1+UP*0.16)
            explanations.append(explanation_group)
            
            # Create multi-line protocol text
            protocol_lines = protocol_examples[i].split('\n')
            protocol_group = VGroup()
            
            for j, line in enumerate(protocol_lines):
                line_text = Text(line, font="Arial")
                line_text.scale(0.5)
                if j > 0:
                    line_text.next_to(protocol_group[-1], DOWN, buff=0.15)
                    line_text.align_to(protocol_group[0], LEFT)
                protocol_group.add(line_text)
            
            # Position all protocol descriptions below the explanations at fixed location
            protocol_group.next_to(explanation_area, DOWN, buff=1.67)
            protocol_group.align_to(explanations[i], LEFT)
            protocols.append(protocol_group)
        
        # Create arrow for highlighting
        highlight_arrow = Arrow(
            LEFT, ORIGIN,
            buff=0.2,
            color=YELLOW,
            stroke_width=6,
            fill_color=YELLOW,
            fill_opacity=1.0
        )
        highlight_arrow.next_to(layers[0], LEFT, buff=0.3)
        
        # First, create all layer rectangles with full opacity
        self.play(ShowCreation(all_layers), run_time=2)
        
        # Then add all labels
        for layer, label in zip(layers, layer_labels):
            self.play(Write(label), run_time=0.3)
        
        self.wait(1)
        
        # Now go through each layer one by one
        for i in range(4):  # 4 layers for TCP/IP
            # Position arrow to point at current layer
            self.play(
                highlight_arrow.animate.next_to(layers[i], LEFT, buff=0.3)
            )
            self.wait(0.5)
            
            # Show explanation and protocols for this layer
            self.play(
                *[Write(text) for text in explanations[i]],
                run_time=1.5
            )
            self.wait(1)
            
            self.play(
                *[Write(text) for text in protocols[i]],
                run_time=1.5
            )
            self.wait(2)
            
            # Fade out explanation and protocol text
            self.play(
                *[FadeOut(text) for text in explanations[i]],
                *[FadeOut(text) for text in protocols[i]],
            )

        self.play(FadeOut(highlight_arrow))
        
        # Add OSI to TCP/IP comparison at the end
        title = Text("OSI vs TCP/IP Layer Mapping", font="Arial").scale(0.8)
        title.to_edge(UP)
        
        # Create comparison table
        osi_colors = [
            "#E74C3C",  # Application - Red
            "#9B59B6",  # Presentation - Purple
            "#3498DB",  # Session - Blue
            "#2ECC71",  # Transport - Green
            "#F1C40F",  # Network - Yellow
            "#E67E22",  # Data Link - Orange
            "#95A5A6",  # Physical - Gray
        ]
        
        osi_names = [
            "7. Application",
            "6. Presentation",
            "5. Session",
            "4. Transport",
            "3. Network",
            "2. Data Link",
            "1. Physical"
        ]
        
        tcpip_names = [
            "4. Application",
            "",
            "",
            "3. Transport",
            "2. Internet",
            "1. Network Interface",
            ""
        ]
        
        # Set up the comparison diagram
        comparison_rect_height = 0.5
        comparison_rect_width = 3
        
        osi_rects = []
        osi_labels = []
        tcpip_rects = []
        tcpip_labels = []
        
        # Create OSI model rectangles for comparison
        for i in range(7):
            rect = Rectangle(
                height=comparison_rect_height,
                width=comparison_rect_width,
                fill_opacity=0.8,
                fill_color=osi_colors[i],
                stroke_color=WHITE
            )
            rect.shift(DOWN * (i - 3) * comparison_rect_height + LEFT * 2)
            
            label = Text(osi_names[i], font="Arial")
            label.scale(0.4)
            label.move_to(rect)
            
            osi_rects.append(rect)
            osi_labels.append(label)
        
        # Create TCP/IP model rectangles for comparison
        tcpip_comparison_colors = [colors[0], colors[0], colors[0], colors[1], colors[2], colors[3], colors[3]]
        
        for i in range(7):
            rect = Rectangle(
                height=comparison_rect_height,
                width=comparison_rect_width,
                fill_opacity=0.8 if tcpip_names[i] != "" else 0,  # No opacity for empty layers
                fill_color=tcpip_comparison_colors[i],
                stroke_color=WHITE if tcpip_names[i] != "" else GREY
            )
            rect.shift(DOWN * (i - 3) * comparison_rect_height + RIGHT * 2)
            
            label = Text(tcpip_names[i], font="Arial")
            label.scale(0.4)
            label.move_to(rect)
            
            tcpip_rects.append(rect)
            tcpip_labels.append(label)
        
        # Create arrows to show mapping
        arrows = []
        
        # Application, Presentation, Session -> Application
        for i in range(3):
            start_point = osi_rects[i].get_right()
            end_point = tcpip_rects[0].get_left()
            arrow = Arrow(start_point, end_point, buff=0.1, color=WHITE)
            arrows.append(arrow)
        
        # Transport -> Transport
        transport_arrow = Arrow(osi_rects[3].get_right(), tcpip_rects[3].get_left(), buff=0.1, color=WHITE)
        arrows.append(transport_arrow)
        
        # Network -> Internet
        network_arrow = Arrow(osi_rects[4].get_right(), tcpip_rects[4].get_left(), buff=0.1, color=WHITE)
        arrows.append(network_arrow)
        
        # Data Link, Physical -> Network Interface
        for i in range(5, 7):
            start_point = osi_rects[i].get_right()
            end_point = tcpip_rects[5].get_left()
            arrow = Arrow(start_point, end_point, buff=0.1, color=WHITE)
            arrows.append(arrow)
        
        # Create labels for the two models
        osi_title = Text("OSI Model", font="Arial").scale(0.6)
        osi_title.next_to(VGroup(*osi_rects), UP, buff=0.3)
        
        tcpip_title = Text("TCP/IP Model", font="Arial").scale(0.6)
        tcpip_title.next_to(VGroup(*tcpip_rects), UP, buff=0.3)
        
        # Show comparison at the end
        comparison_elements = [
            title, 
            *osi_rects, *osi_labels, 
            *tcpip_rects, *tcpip_labels, 
            *arrows, 
            osi_title, tcpip_title
        ]
        
        # Fade out layers to make room for comparison
        self.play(FadeOut(all_layers), *[FadeOut(label) for label in layer_labels])
        
        # Add comparison
        self.play(*[FadeIn(elem) for elem in comparison_elements],
                  self.camera.frame.animate.scale(0.8).shift(UP*0.7779))
        
        self.wait(10)
        
        # Fade everything out at the end
        self.play(*[FadeOut(elem) for elem in comparison_elements])
        
        self.wait(2)
