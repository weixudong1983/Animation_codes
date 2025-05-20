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
        
        # First, create all layer rectangles with full opacity
        self.play(ShowCreation(all_layers), run_time=2)
        
        # Then add all labels
        for layer, label in zip(layers, layer_labels):
            self.play(Write(label), run_time=0.3)
        
        self.wait(1)
        
        # Define consistent height for all data components
        data_height = 0.5
        
        # Create data packet representation (Application Layer)
        data_packet = Rectangle(
            height=data_height,
            width=1.5,
            fill_opacity=0.9,
            fill_color="#E74C3C",
            stroke_color=BLACK
        )
        
        # Position data at application layer on the right side (far from layer)
        data_packet.next_to(layers[0], RIGHT, buff=2.0)
        
        # Show data packet creation
        self.play(ShowCreation(data_packet))
        self.wait(0.5)
        
        # Move data to application layer (still keeping distance)
        self.play(data_packet.animate.next_to(layers[0], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Move to presentation layer
        self.play(data_packet.animate.next_to(layers[1], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Change color at presentation layer (encryption)
        self.play(data_packet.animate.set_fill(color=colors[1], opacity=0.7))
        self.wait(0.5)
        
        # Move to session layer
        self.play(data_packet.animate.next_to(layers[2], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Create session header (small)
        session_header = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[2],
            stroke_color=BLACK
        )
        session_header.next_to(data_packet, LEFT, buff=0)
        
        # Show session header being added
        self.play(ShowCreation(session_header))
        session_data = VGroup(session_header, data_packet)
        self.wait(0.5)
        
        # Move to transport layer
        self.play(session_data.animate.next_to(layers[3], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Create transport headers (source and destination ports)
        src_port = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[3],
            stroke_color=BLACK
        )
        src_port.next_to(session_data, LEFT, buff=0)
        
        dst_port = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[3],
            stroke_color=BLACK
        )
        dst_port.next_to(session_data, RIGHT, buff=0)
        
        # Show transport headers being added
        self.play(ShowCreation(src_port), ShowCreation(dst_port))
        transport_data = VGroup(src_port, session_data, dst_port)
        self.wait(0.5)
        
        # Move to network layer
        self.play(transport_data.animate.next_to(layers[4], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Create network headers (source and destination IPs)
        src_ip = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[4],
            stroke_color=BLACK
        )
        src_ip.next_to(transport_data, LEFT, buff=0)
        
        dst_ip = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[4],
            stroke_color=BLACK
        )
        dst_ip.next_to(transport_data, RIGHT, buff=0)
        
        # Show network headers being added
        self.play(ShowCreation(src_ip), ShowCreation(dst_ip))
        network_data = VGroup(src_ip, transport_data, dst_ip)
        self.wait(0.5)
        
        # Move to data link layer
        self.play(network_data.animate.next_to(layers[5], RIGHT, buff=1.0))
        self.wait(0.5)
        
        # Create data link headers (source and destination MACs)
        src_mac = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[5],
            stroke_color=BLACK
        )
        src_mac.next_to(network_data, LEFT, buff=0)
        
        dst_mac = Rectangle(
            height=data_height,
            width=0.3,
            fill_opacity=0.9,
            fill_color=colors[5],
            stroke_color=BLACK
        )
        dst_mac.next_to(network_data, RIGHT, buff=0)
        
        # Show data link headers being added
        self.play(ShowCreation(src_mac), ShowCreation(dst_mac))
        datalink_data = VGroup(src_mac, network_data, dst_mac)
        self.wait(0.5)
        
        # Move to physical layer (do nothing to the data)
        self.play(datalink_data.animate.next_to(layers[6], RIGHT, buff=1.0))
        self.wait(1)
        

        self.wait(2)



        # Code to add after the last self.wait(1) line and before self.wait(2)
        
        # Convert to raw bits (0s and 1s) at physical layer
        bits = []
        num_bits = 20  # Number of bits to show
        bit_width = 0.15
        bit_spacing = 0.02
        bits_group = VGroup()
        
        for i in range(num_bits):
            bit = Text("1" if i % 2 == 0 else "0", font="Monospace").scale(1.3)
            bit.scale(0.4)
            bit.move_to(datalink_data.get_center())
            bit.shift(RIGHT * i * (bit_width + bit_spacing))
            bits.append(bit)
            bits_group.add(bit)
        
        # Position the bits correctly
        bits_group.move_to(datalink_data.get_center())
        
        # Transform data into bits
        self.play(
            FadeOut(datalink_data),
            FadeIn(bits_group),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Create receiving side OSI model
        receiver_layers = []
        receiver_labels = []
        
        # Create the receiver stack of layers
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
            
            receiver_layers.append(rect)
            receiver_labels.append(label)
        
        # Group all receiver layers together
        all_receiver_layers = VGroup(*receiver_layers)
        # Position the receiver OSI model stack on the right side
        all_receiver_layers.shift(RIGHT * 15)
        
        # Shift all receiver layer labels too
        for label in receiver_labels:
            label.shift(RIGHT * 15)
        
        # Create all receiver layer rectangles with full opacity
        self.play(ShowCreation(all_receiver_layers), run_time=2)
        
        # Then add all labels
        for layer, label in zip(receiver_layers, receiver_labels):
            self.play(Write(label), run_time=0.2)
        
        self.wait(0.5)
        
        # Transmit the bits to the physical layer of the receiver
        self.play(
            bits_group.animate.next_to(receiver_layers[6], LEFT, buff=1.0),
            self.camera.frame.animate.shift(RIGHT*12),
            run_time=1.5
        )
        self.wait(1.5)

        datalink_data.move_to(bits_group)

        self.play(FadeOut(bits_group), FadeIn(datalink_data), run_time=1.5)

        self.wait(2)

        # RECEIVING SIDE - PROCESS DATA UP THE STACK
        
        # Move from physical to data link layer
        self.play(datalink_data.animate.next_to(receiver_layers[5], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Remove data link headers (MAC addresses)
        network_data = VGroup(*[datalink_data[1]])  # Extract the network data part
        
        # Create animations to move the MAC headers away
        src_mac_fade = FadeOut(datalink_data[0], shift=LEFT)  # Source MAC header
        dst_mac_fade = FadeOut(datalink_data[2], shift=RIGHT)  # Destination MAC header
        
        # Play the removal animations
        self.play(src_mac_fade, dst_mac_fade)
        self.wait(0.5)
        
        # Move to network layer
        self.play(network_data.animate.next_to(receiver_layers[4], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Remove network headers (IP addresses)
        transport_data = VGroup(*[network_data[0][1]])  # Extract transport data
        
        # Create animations to move the IP headers away
        src_ip_fade = FadeOut(network_data[0][0], shift=LEFT)  # Source IP header
        dst_ip_fade = FadeOut(network_data[0][2], shift=RIGHT)  # Destination IP header
        
        # Play the removal animations
        self.play(src_ip_fade, dst_ip_fade)
        self.wait(0.5)
        
        # Move to transport layer
        self.play(transport_data.animate.next_to(receiver_layers[3], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Remove transport headers (ports)
        session_data = VGroup(*[transport_data[0][1]])  # Extract session data
        
        # Create animations to move the port headers away
        src_port_fade = FadeOut(transport_data[0][0], shift=LEFT)  # Source port header
        dst_port_fade = FadeOut(transport_data[0][2], shift=RIGHT)  # Destination port header
        
        # Play the removal animations
        self.play(src_port_fade, dst_port_fade)
        self.wait(0.5)
        
        # Move to session layer
        self.play(session_data.animate.next_to(receiver_layers[2], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Remove session header
        data_packet = session_data[0][1]  # Extract the data packet
        
        # Create animation to move the session header away
        session_header_fade = FadeOut(session_data[0][0], shift=LEFT)
        
        # Play the removal animation
        self.play(session_header_fade)
        self.wait(0.5)
        
        # Move to presentation layer
        self.play(data_packet.animate.next_to(receiver_layers[1], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Change color back at presentation layer (decryption)
        self.play(data_packet.animate.set_fill(color=colors[0], opacity=0.9))
        self.wait(0.5)
        
        # Move to application layer
        self.play(data_packet.animate.next_to(receiver_layers[0], LEFT, buff=1.0))
        self.wait(0.5)
        
        # Data arrives at application layer
        success_text = Text("Received!", font="Arial")
        success_text.scale(1.55)
        success_text.next_to(receiver_layers[3], LEFT, buff=1.6)
        
        self.play(Write(success_text))
        self.wait(2)


        self.embed()
