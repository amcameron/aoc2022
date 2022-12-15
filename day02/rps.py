"""Calculate Rock, Paper, Scissors scores."""

from enum import auto, Enum


class ValidMoves(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


_r, _p, _s = ValidMoves
OpponentMoveCodes = Enum('OpponentMoveCodes', 'A B C')
YourMoveCodes = Enum('YourMoveCodes', 'X Y Z')
OpponentDecoder = dict(zip(OpponentMoveCodes, ValidMoves))
YourMoveDecoder = dict(zip(YourMoveCodes, ValidMoves))
Outcomes = Enum('Outcomes', 'Loss Draw Win')
_l, _d, _w = Outcomes
InstructionDecoder = dict(zip(YourMoveCodes, Outcomes))
OppMoveAndOutcomeDecoder = {
        _r: {_l: _s, _d: _r, _w: _p},
        _p: {_l: _r, _d: _p, _w: _s},
        _s: {_l: _p, _d: _s, _w: _r}}


def _rps(opp_move, your_move):
    opp_score = opp_move.value
    your_score = your_move.value
    you_win = False

    match (opp_move, your_move):
        case (ValidMoves.Rock, ValidMoves.Paper) | \
                (ValidMoves.Paper, ValidMoves.Scissors) | \
                (ValidMoves.Scissors, ValidMoves.Rock):
            # win
            your_score += 6
            you_win = True
        case (o, y) if o == y:
            #tie
            opp_score += 3
            your_score += 3
        case (ValidMoves.Paper, ValidMoves.Rock) | \
                (ValidMoves.Scissors, ValidMoves.Paper) | \
                (ValidMoves.Rock, ValidMoves.Scissors):
            # loss
            opp_score += 6
        case _:
            raise ValueError(f"received invalid moves: {opp_move} {your_move}")

    return you_win, opp_score, your_score


def calculate_rps_outcome_pt1(opp_code, your_code):
    opp_move = OpponentDecoder[opp_code]
    your_move = YourMoveDecoder[your_code]

    return _rps(opp_move, your_move)


def calculate_rps_outcome_pt2(opp_code, instr):
    opp_move = OpponentDecoder[opp_code]
    opp_score = opp_move.value
    outcome = InstructionDecoder[instr]
    your_move = OppMoveAndOutcomeDecoder[opp_move][outcome]
    your_score = your_move.value

    return _rps(opp_move, your_move)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    opp_total = {'part1': 0, 'part2': 0}
    you_total = {'part1': 0, 'part2': 0}
    opp_wins = {'part1': 0, 'part2': 0}
    you_wins = {'part1': 0, 'part2': 0}
    matches = 0
    with open(args.filename, 'r') as f:
        for line in f:
            opp_code, you_code = line.strip().split()
            opp_code = OpponentMoveCodes[opp_code]
            you_code = YourMoveCodes[you_code]
            win1, os1, ys1 = calculate_rps_outcome_pt1(opp_code, you_code)
            win2, os2, ys2 = calculate_rps_outcome_pt2(opp_code, you_code)
            opp_total['part1'] += os1
            you_total['part1'] += ys1
            opp_total['part2'] += os2
            you_total['part2'] += ys2
            matches += 1
            if win1:
                you_wins['part1'] += 1
            else:
                opp_wins['part1'] += 1
            if win2:
                you_wins['part2'] += 1
            else:
                opp_wins['part2'] += 1
    print(f'{matches=}\n\nPART 1\nYour wins:\t{you_wins["part1"]}\nOpponent wins:\t{opp_wins["part1"]}')
    print(f'Your score:\t{you_total["part1"]}\nOpponent score:\t{opp_total["part1"]}')
    print(f'\n\nPART 2\nYour wins:\t{you_wins["part2"]}\nOpponent wins:\t{opp_wins["part2"]}')
    print(f'Your score:\t{you_total["part2"]}\nOpponent score:\t{opp_total["part2"]}')
