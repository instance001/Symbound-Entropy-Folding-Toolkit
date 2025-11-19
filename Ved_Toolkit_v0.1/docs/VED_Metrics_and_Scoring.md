# VED Metrics and Scoring

Key metrics:
- Load vector L
- Routing cost R(i) and R_total
- Resolution efficiency E_o
- Routing efficiency E_r
- Failure rate F
- Composite VED score S_VED

S_VED = α E_o + β E_r + γ (1 - F)

All scoring logic is implemented in `src/ved_core.py`.
