# Quachess
The rules are simple:
- Every piece can be moved to max 2 squares in every move
- Probabilities add when re-entering your previous branch
- Probabilities multiply when phasing through pieces. You can't phase through a 100% piece
- Only terminal branches can be moved from
- During an attempted capture, first both pieces' probabilities are collapsed to give it's actual position. Capture occurs with respect to their actual position. 
  Pawns are unique in this, being able to move diagonally even if the capture didn't actually occur
- The king can not superpose


## Suggestions
- Use a monospace font to ensure everything renders correctly
- Currently only posix shells are supported
