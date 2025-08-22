# 🃏 Blackjack Python CLI

A fully-featured, text-based Blackjack CLI game written in Python, designed to be beautiful, functional, and clean. The game is extremely well-documented and commented, making it an excellent resource for anyone learning Python or exploring CLI game development.

It features a complete Blackjack system including betting, splitting, doubling down, surrendering, and fully customizable settings, all presented with polished ASCII card graphics.

---

## ⚙️ Features

### 🃏 Full Blackjack Rules
- Player and dealer turns, betting system, doubling down, splitting, and surrendering.
- Automatic handling of **Ace values** for optimal scoring:
```python
def hand_value(cards: list[str]) -> int:
    value = 0
    aces = 0
    for card in cards:
        rank = card[:-1]
        if rank in "JQK": value += 10
        elif rank == "A": aces += 1; value += 11
        else: value += int(rank)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value
````

* Supports multiple hands for **splits** and dynamic gameplay.

### 🔀 Splitting & Multiple Hands

```python
def split_hand(hand: dict, hands: list[dict]):
    if len(hand["cards"]) == 2 and hand["cards"][0][:-1] == hand["cards"][1][:-1]:
        new_hand = {"cards": [hand["cards"].pop()], "bet": hand["bet"], "active": True}
        hands.append(new_hand)
```

### 🖼️ ASCII Card Graphics

* Clean, visually appealing ASCII art for each card:

```python
def render_card(card: str, hidden: bool=False) -> str:
    if hidden:
        return "┌─────┐\n│░░░░░│\n│░░░░░│\n└─────┘"
    rank, suit = card[:-1], card[-1]
    return f"┌─────┐\n│{rank:<2}   │\n│  {suit}  │\n│   {rank:>2}│\n└─────┘"
```

* Displays multiple player hands and dealer hand neatly:

```python
def print_hands(player_hands: list[dict], dealer_hand: dict, hide_dealer=True):
    for hand in player_hands:
        print("Your Hand:")
        for card in hand["cards"]:
            print(render_card(card))
        print(f"Value: {hand_value(hand['cards'])}\n")
    print("Dealer Hand:")
    for i, card in enumerate(dealer_hand["cards"]):
        print(render_card(card, hidden=(i == 0 and hide_dealer)))
```

### ⚙️ Customizable Settings

* Adjust deck count, enable/disable doubling, splitting, surrendering, and soft-17 rules.
* Changes are applied in real time, including shuffling:

```python
def generate_deck(num_decks=1) -> list[str]:
    deck = [f"{rank}{suit}" for rank in ranks for suit in SUITS] * num_decks
    random.shuffle(deck)
    return deck
```

### 🎯 Educational & Open Source

* Well-documented functions and classes for easy learning.
* Perfect for beginners learning Python, CLI game logic, or card game development.
* Demonstrates that terminal-based games can be polished, functional, and visually engaging.

---

## 🖼️ Screenshots

_Welcome Screen and Main Menu_

![](https://ik.imagekit.io/somewhatmay/project-outline-images/blackjack/WindowsTerminal_1kvCUsVfZH.png)

_Tutorial Preview_

![](https://ik.imagekit.io/somewhatmay/project-outline-images/blackjack/WindowsTerminal_W0O0sdPine.png)

_Sample Game Preview_

![](https://ik.imagekit.io/somewhatmay/project-outline-images/blackjack/WindowsTerminal_7ADQ4I64Tj.png)

_Settings Menu_

![](https://ik.imagekit.io/somewhatmay/project-outline-images/blackjack/WindowsTerminal_4nOM2SaG6B.png)

---

## 🛠️ Technologies Used

* Python
* CLI
* ASCII Art

---

## 🏷️ Tags

* Python
* CLI Game
* Open Source
* Game Development
* ASCII Art

---

## 📥 Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/blackjack-cli.git
cd blackjack-cli
```

2. Run the game:

```bash
python3 main.py
```

3. Follow the on-screen prompts to play.

---

## 📖 Contributing

Feel free to fork, submit issues, or make pull requests. Contributions are welcome!

---

## 📄 License

This project is open source and available under the MIT License.

