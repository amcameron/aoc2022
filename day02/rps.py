"""Calculate Rock, Paper, Scissors scores."""


_moves = _r, _p, _s = 'Rock', 'Paper', 'Scissors'
_move_scores = _rs, _ps, _ss = 1, 2, 3
_opponent_moves = dict(zip('ABC', _moves))
_own_moves = dict(zip('XYZ', _moves))
_move_scores = dict(zip(_moves, _move_scores))


def calculate_rps_outcome(opp_move, your_move):
    om = _opponent_moves[opp_move]
    ym = _own_moves[your_move]
    opp_score = _move_scores[om]
    your_score = _move_scores[ym]
    you_win = False

    match (om, ym):
        case (o, y) if (o, y) in ((_r, _p), (_p, _s), (_s, _r)):
            # win
            your_score += 6
            you_win = True
        case (o, y) if _move_scores[o] == _move_scores[y]:
            #tie
            opp_score += 3
            your_score += 3
        case (o, y) if (o, y) in ((_p, _r), (_s, _p), (_r, _s)):
            # loss
            opp_score += 6
        case _:
            raise ValueError(f"received invalid moves: {opp_move} {your_move}")

    return you_win, opp_score, your_score


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('filename')
    args = p.parse_args()

    opp_total = 0
    you_total = 0
    opp_wins = 0
    you_wins = 0
    matches = 0
    with open(args.filename, 'r') as f:
        for line in f:
            opp_move, you_move = line.strip().split()
            win, os, ys = calculate_rps_outcome(opp_move, you_move)
            opp_total += os
            you_total += ys
            matches += 1
            if win:
                you_wins += 1
            else:
                opp_wins += 1
    print(f'{matches=}\nYour wins:\t{you_wins}\nOpponent wins:\t{opp_wins}')
    print(f'Your score:\t{you_total}\nOpponent score:\t{opp_total}')
