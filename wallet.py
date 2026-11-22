from PIL import Image, ImageDraw, ImageFont

class User:
    def __init__(self, name: str, money: float):
        self.name = name
        self.money = money
        self.starting_money = money
        self.stuff_done = []

    def working(self, hours: str, earnings: float):
        self.money += earnings
        self.stuff_done.append(f"Working ({hours}) -> +{earnings}")

    def buying(self, item: str, cost: float):
        self.money -= cost
        self.stuff_done.append(f"Bought ({item}) -> -{cost}")

    def check_valid(self, amount):
        return amount > 0

    def deposit(self, amount: float):
        if self.check_valid(amount):
            self.money += amount
            self.stuff_done.append(f"Deposit -> +{amount}")

    def withdraw(self, amount: float):
        if self.check_valid(amount):
            self.money -= amount
            self.stuff_done.append(f"Withdraw -> -{amount}")

    def generate_receipt(self, filename: str = "Summary.png"):
        # Colors
        bg_color = (241, 245, 249)  # Soft slate background
        card_color = (255, 255, 255)  # Pure white card
        header_color = (30, 41, 59)  # Dark navy header
        text_dark = (30, 41, 59)
        text_muted = (100, 116, 139)
        green = (22, 163, 74)  # Earnings / Deposits
        red = (220, 38, 38)  # Expenses / Withdrawals
        border_color = (203, 213, 225)

        try:
            font_title = ImageFont.load_default(size=22)
            font_sub = ImageFont.load_default(size=14)
            font_body = ImageFont.load_default(size=15)
            font_total = ImageFont.load_default(size=18)
        except TypeError:
            font_title = font_sub = font_body = font_total = ImageFont.load_default()

        # Calculate dynamic height based on number of transactions
        width = 460
        row_height = 32
        base_height = 295
        height = base_height + (len(self.stuff_done) * row_height)

        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)

        # 1. Draw Main Card with rounded corners
        margin = 20
        draw.rounded_rectangle(
            [margin, margin, width - margin, height - margin],
            radius=16,
            fill=card_color,
            outline=border_color,
            width=2,
        )

        # 2. Draw Top Header Banner
        header_height = 95
        draw.rounded_rectangle(
            [margin, margin, width - margin, margin + header_height],
            radius=16,
            fill=header_color,
        )
        draw.rectangle(
            [margin, margin + 75, width - margin, margin + header_height],
            fill=header_color,
        )

        # Header Text
        draw.text(
            (margin + 20, margin + 18),
            "ACCOUNT SUMMARY",
            fill=(148, 163, 184),
            font=font_sub,
        )
        draw.text(
            (margin + 20, margin + 42),
            self.name,
            fill=(255, 255, 255),
            font=font_title,
        )

        # 3. Starting Balance Section
        y = margin + header_height + 20
        draw.text(
            (margin + 20, y), "Starting Balance:", fill=text_muted, font=font_body
        )
        draw.text(
            (width - margin - 20, y),
            f"${self.starting_money:,.2f}",
            fill=text_dark,
            font=font_body,
            anchor="ra",
        )

        # Divider Line
        y += 30
        draw.line(
            [(margin + 20, y), (width - margin - 20, y)], fill=border_color, width=1
        )

        # 4. Transaction History
        y += 15
        draw.text((margin + 20, y), "Activity Log:", fill=text_muted, font=font_sub)
        y += 28

        for action in self.stuff_done:
            separator = "->" if "->" in action else (":" if ":" in action else None)

            if separator and not action.startswith("Failed"):
                desc, amt = action.split(separator, 1)
                desc = desc.strip()
                amt = amt.strip()
                amt_color = green if "+" in amt else red
            else:
                desc = action
                amt = ""
                amt_color = text_muted

            draw.text((margin + 20, y), f"- {desc}", fill=text_dark, font=font_body)
            if amt:
                draw.text(
                    (width - margin - 20, y),
                    amt,
                    fill=amt_color,
                    font=font_body,
                    anchor="ra",
                )
            y += row_height

        # Bottom Divider Line
        y += 8
        draw.line(
            [(margin + 20, y), (width - margin - 20, y)], fill=border_color, width=2
         )

        # 5. Ending Balance Footer
        y += 18
        draw.text((margin + 20, y), "Ending Balance", fill=text_dark, font=font_total)
        draw.text(
            (width - margin - 20, y),
            f"${self.money:,.2f}",
            fill=header_color,
            font=font_total,
            anchor="ra",
        )

        image.save(filename)
        print(f"Image '{filename}' generated successfully!")