# Blackjack
Welcome to my blackjack project! To start, download the code.

After you have to download some modules. You can do this by opening a terminal in this folder and pasting this command.

windows:
`py -m pip install -r requirements.txt`

linux and mac:
`python3 -m pip install -r requirements.txt`

Then open blackjack_GUI.py to have some fun!
## Features
### Keybinds
```
's', 'space' and 'f1' to stand
'h' and 'f3' to hit
'd 'and 'f2' to double
'enter' and 'f4 'to enter a bet and to press continue
```

### Everything saves!
Your settings, money and all previous games are saved in json files, so you can continue anytime!

### Never run out of money!
Did you lose all your money? Don't worry, just use your credit card! You will get more money to play with, but the profit will still be in the negatives.

### customizable settings
change exactly how you want to play:

#### general cooldown
default value: `500`

The exact cooldown when the AI grabs a new card, and how long until blackjack is revealed.

#### Total number of decks used
default value: `6`

min value: `1`

Total number of decks used in the game if you want to use card counting. Shuffles if all cards are used.

#### Shuffles after this many rounds
default value: `5`

min value: `1`

shuffles the entire deck after this many rounds.

#### Dealer stops at this score
default value: `17`

min value: `1`

Experimental, but this dictates at what score value the dealer automatically stops grabbing cards. This however does not change the first two cards he has automatically, of which the first one is always hidden (might make this a settings option later).

#### How much money you'll take from your credit card
default value: `1000.0`

min value: `1.0`

When you run out of money, a button pops up where you can use your credit card. This setting dictates how much debt you'll be in.

#### Maximum score you can win:
default value: `21`

min value: `1`

Experimental. This dictates what the maximum score of everyone is. If your score is over this value, you or the dealer will bust.

#### Automatically stand at max score
default value: `True`

This dictates if you automatically stand at the maximum score. If the maximum score is 21, you'll automatically stand on 21.

#### Enable blackjack
default value: `True`

This enables or disables blackjack for both parties. So if you have blackjack, you can still hit, stand or double down. But the blackjack payout is not given.