import tkinter as tk

class ReviewWindow(tk.Toplevel):
    def __init__(self, parent, questions, on_send_callback=None):
        super().__init__(parent)      
        self.questions = questions    
        self.on_send_callback = on_send_callback # Function from your main app to save to DB
        self.title("Visual Data Review") 
        
        self.geometry("750x650")
        self.build_ui()               

    def build_ui(self):
        # 1. FIXED BOTTOM ACTION BAR
        # Creating this first and packing it at the bottom ensures it stays fixed on screen
        action_bar = tk.Frame(self, bg="#ffffff", padx=20, pady=15, bd=0, highlightbackground="#e2e8f0", highlightthickness=1)
        action_bar.pack(side="bottom", fill="x")
        
        # Cancel Button (Closes the window without doing anything)
        cancel_btn = tk.Button(
            action_bar,
            text="Cancel",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444", # Crisp red
            fg="#ffffff",
            activebackground="#dc2626",
            activeforeground="#ffffff",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.destroy
        )
        cancel_btn.pack(side="left")
        
        # Send to DB Button
        send_btn = tk.Button(
            action_bar,
            text="Send to DB",
            font=("Segoe UI", 10, "bold"),
            bg="#2563eb", # Modern blue
            fg="#ffffff",
            activebackground="#1d4ed8",
            activeforeground="#ffffff",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.send_to_database
        )
        send_btn.pack(side="right")

        # 2. SCROLLABLE CANVAS SYSTEM (For the cards)
        # Pack this with fill="both" and expand=True so it claims all remaining space above the action bar
        canvas = tk.Canvas(self, bg="#f0f2f5", borderwidth=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#f0f2f5", padx=20, pady=20)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=700)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 3. Build the Visual Cards (Iterating over data)
        for q in self.questions:
            card = tk.Frame(
                scrollable_frame, 
                bg="#ffffff", 
                padx=20, 
                pady=20, 
                highlightbackground="#e2e8f0", 
                highlightthickness=1,
                bd=0
            )
            card.pack(fill="x", pady=12, anchor="w")
            
            region = q.get('region_id', 'N/A')
            correct = q.get('correct', 'N/A')
            
            meta_text = f"REGION ID: {region}   |   CORRECT INDEX: {correct}"
            meta_label = tk.Label(card, text=meta_text, font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#ffffff")
            meta_label.pack(anchor="w", pady=(0, 10))
            
            question_label = tk.Label(
                card, text=q["question"], font=("Segoe UI", 11, "bold"), fg="#1e293b", bg="#ffffff",
                wraplength=640, justify="left"
            )
            question_label.pack(anchor="w", pady=(0, 15))
            
            options_frame = tk.Frame(card, bg="#ffffff")
            options_frame.pack(fill="x")
            
            for index, option in enumerate(q["options"]):
                is_correct = (index == q["correct"])
                bg_color = "#dcfce7" if is_correct else "#f8fafc"
                fg_color = "#15803d" if is_correct else "#475569"
                border_color = "#bbf7d0" if is_correct else "#e2e8f0"
                prefix = "✓ " if is_correct else "  "
                
                option_backplate = tk.Frame(options_frame, bg=bg_color, highlightbackground=border_color, highlightthickness=1, bd=0)
                option_backplate.pack(fill="x", pady=4)
                
                opt_label = tk.Label(
                    option_backplate, text=f"{prefix}{chr(65 + index)})  {option}", 
                    font=("Segoe UI", 10, "bold" if is_correct else "normal"),
                    fg=fg_color, bg=bg_color, padx=12, pady=10, anchor="w", justify="left", wraplength=600
                )
                opt_label.pack(fill="x")

    def send_to_database(self):
        """Triggers your saving mechanism and automatically shuts the review window."""
        if self.on_send_callback:
            # Pass the current valid list back to your database logic function
            self.on_send_callback(self.questions)
        else:
            print("Database save triggered, but no callback function was hooked up!")
            
        self.destroy() # Close the window smoothly after sending