import sys

input = list(
    map(lambda line : line.rstrip(),
    sys.stdin.readlines()
    ))

print("Hello world!")

numbers = list(
    map(
        lambda column : int(column),
        input[0].split(',')
    )
)

print(numbers)

boards=[]
bingo_cards = []
for i in range(2, len(input), 6):
    current_board = []
    current_bingo_card = []
    for j in range(0, 5):
        current_board.append(
            list(
                map(
                    lambda column : int(column),
                    filter(
                        lambda column : column != '',
                        input[i+j].split(' ')
                    )
                )
            )
        )
        current_bingo_card.append([False, False, False, False, False])
    boards.append(current_board)
    bingo_cards.append(current_bingo_card)

print(boards)
print(bingo_cards)

def mark_board(drawn_number, board, bingo_card):
    for i in range (0, 5):
        for j in range (0, 5):
            if board[i][j] == drawn_number:
                bingo_card[i][j] = True

def check_winner(bingo_card):
    # check rows
    for i in range(0, 5):
        result = True
        for j in range(0, 5):
            result = result and bingo_card[i][j]
        if result:
            return result
        
    # check cols
    for i in range(0, 5):
        result = True
        for j in range(0, 5):
            result = result and bingo_card[j][i]
        if result:
            return result

    return False

def sum_unmarked(board, bingo_card):
    sum = 0
    for i in range (0, 5):
        for j in range (0, 5):
            if not bingo_card[i][j]:
                sum += board[i][j]
    return sum

def play_bingo(numbers, boards, bingo_cards):
    for drawn_number in numbers:
        # mark all the boards
        for i in range(0, len(boards)) :
            mark_board(drawn_number, boards[i], bingo_cards[i])
        
        # check for winner
        for i in range(0, len(boards)):
            if check_winner(bingo_cards[i]):
                return [drawn_number, sum_unmarked(boards[i], bingo_cards[i])]
        
        print(bingo_cards)

drawn_number, sum=play_bingo(numbers, boards, bingo_cards)
print(f"drawn_number={drawn_number} sum={sum} score={drawn_number*sum}")

# reset bingo cards
for i in range(0, len(boards)):
    for j in range(0, 5):
        for k in range(0, 5):
            bingo_cards[i][j][k] = False

def play_until_one(numbers, boards, bingo_cards):

    # put everything into a dictionary for efficiency
    remaining_players = set()
    for i in range(0, len(boards)):
        remaining_players.add(i)

    for drawn_number in numbers:
        # mark all the boards
        for i in remaining_players:
            mark_board(drawn_number, boards[i], bingo_cards[i])
        
        # check for winner
        players_to_remove = []
        for i in remaining_players:
            if check_winner(bingo_cards[i]):
                players_to_remove.append(i)
        for i in players_to_remove:
            if len(remaining_players) == 1:
                return [drawn_number, sum_unmarked(boards[i], bingo_cards[i])]
            remaining_players.remove(i)


drawn_number, sum=play_until_one(numbers, boards, bingo_cards)
print(f"drawn_number={drawn_number} sum={sum} score={drawn_number*sum}")