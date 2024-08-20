# ChessVariation

## Description

This program consists of a class ChessVar, where a given instance is a playable variant of Chess. Users call only on the make_move method, passing in a proposed move. A variety of tests are performed to check the validity of the move. If valid, the proposed move takes place, the game updates accordingly, and it returns True. Otherwise, it returns False.

## Game Play

Includes all pieces except pawns and queens. Each player starts at the same end of the board, and the first player whose king reaches the other end (row 8) wins. 

Note: A valid move cannot put either king in check.
