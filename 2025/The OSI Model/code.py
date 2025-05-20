from manimlib import *

class OSIModelAnimation(Scene):
    def construct(self):
        # Define colors for each layer
        colors = [
            "#E74C3C",  # Application - Red
            "#9B59B6",  # Presentation - Purple
            "#3498DB",  # Session - Blue
            "#2ECC71",  # Transport - Green
            "#F1C40F",  # Network - Yellow
            "#E67E22",  # Data Link - Orange
            "#95A5A6",  # Physical - Gray
        ]
        
        # Layer names and descriptions
        layer_names = [
            "Application Layer (7)",
            "Presentation Layer (6)",
            "Session Layer (5)",
            "Transport Layer (4)",
            "Network Layer (3)",
            "Data Link Layer (2)",
            "Physical Layer (1)"
        ]
        
        # Shorter, more vertically-oriented descriptions with frequent line breaks
        layer_descriptions = [
            "Function:\nProvides network services\ndirectly to end-users.\nFacilitates communication\nbetween applications\nand lower network layers.",
            "Function:\nTranslates data between\napplication and network formats.\nHandles encryption,\ncompression, and\nprotocol conversion.",
            "Function:\nEstablishes, manages,\nand terminates connections.\nControls dialogues\nbetween computers and\nmanages synchronization.",
            "Function:\nEnsures complete data\ntransfer with error recovery.\nResponsible for segmentation,\nflow control, and\nend-to-end error correction.",
            "Function:\nRoutes packets across\nnetworks to their destination.\nHandles logical addressing\nand determines best path\nfor data to travel.",
            "Function:\nTransfers data frames\nbetween adjacent nodes.\nResponsible for physical\naddressing, error detection,\nand media access control.",
            "Function:\nTransmits raw bit streams\nover physical medium.\nDefines electrical, mechanical,\nand functional specifications\nfor physical links."
        ]
        
        # Protocol examples with more line breaks
        protocol_examples = [
            "Common Protocols:\n• HTTP (Web browsing)\n• FTP (File transfers)\n• SMTP/POP3 (Email)\n• DNS (Name resolution)",
            "Common Protocols:\n• SSL/TLS (Encryption)\n• JPEG, PNG, GIF\n  (Image formats)\n• MIME (Email encoding)",
            "Common Protocols:\n• NetBIOS\n  (Windows networking)\n• RPC\n  (Remote procedure calls)\n• SDP (Session description)",
            "Common Protocols:\n• TCP\n  (Connection-oriented)\n• UDP (Connectionless)\n• SCTP (Combined features)",
            "Common Protocols:\n• IPv4 and IPv6\n  (Internet addressing)\n• ICMP (Error reporting)\n• OSPF, BGP (Routing)",
            "Common Protocols:\n• Ethernet (LAN)\n• PPP (Point-to-point)\n• 802.11 (Wi-Fi)\n• HDLC (WAN)",
            "Common Standards:\n• RS-232 (Serial)\n• Ethernet physical layer\n• Bluetooth\n• USB, SONET"
        ]
        
        # Create rectangles for layers
        layer_height = 0.8
        layer_width = 6
        layers = []
        layer_labels = []
        
        # Create the stack of layers
        for i in range(7):
            rect = Rectangle(
                height=layer_height,
                width=layer_width,
                fill_opacity=1.0,
                fill_color=colors[i],
                stroke_color=WHITE
            )
            rect.shift(DOWN * (i - 3) * layer_height)
            
            label = Text(layer_names[i], font="Arial")
            label.scale(0.6)
            label.move_to(rect)
            
            layers.append(rect)
            layer_labels.append(label)
        
        # Group all layers together
        all_layers = VGroup(*layers)
        # Position the OSI model stack on the left side
        all_layers.shift(LEFT * 2.5)
        
        # Shift all layer labels too
        for label in layer_labels:
            label.shift(LEFT * 2.5)
        
        # Create layer explanations and protocol examples (to be shown later)
        explanations = []
        protocols = []
        
        # Create a fixed position for explanations on the right side - moved further right
        explanation_area = RIGHT * 4 + UP * 1.5  # Changed from RIGHT * 3 to RIGHT * 4.5
        
        for i in range(7):
            # Create multi-line text for explanations
            explanation_lines = layer_descriptions[i].split('\n')
            explanation_group = VGroup()
            
            for j, line in enumerate(explanation_lines):
                line_text = Text(line, font="Arial")
                line_text.scale(0.5)  # Larger text size (was 0.4)
                if j > 0:
                    line_text.next_to(explanation_group[-1], DOWN, buff=0.15)
                    line_text.align_to(explanation_group[0], LEFT)
                explanation_group.add(line_text)
            
            # Position all explanations at the same fixed location on right side
            explanation_group.move_to(explanation_area).shift(RIGHT*0.1)
            explanations.append(explanation_group)
            
            # Create multi-line protocol text
            protocol_lines = protocol_examples[i].split('\n')
            protocol_group = VGroup()
            
            for j, line in enumerate(protocol_lines):
                line_text = Text(line, font="Arial")
                line_text.scale(0.5)  # Larger text size (was 0.4)
                if j > 0:
                    line_text.next_to(protocol_group[-1], DOWN, buff=0.15)
                    line_text.align_to(protocol_group[0], LEFT)
                protocol_group.add(line_text)
            
            # Position all protocol descriptions below the explanations at fixed location
            protocol_group.next_to(explanation_area, DOWN, buff=2.2)
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
        for i in range(7):
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
        

        self.wait(2)
