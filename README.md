# obstacle-detection – Algorithmes d'identification des obstacles cognitifs

## Trois obstacles ciblés

| Obstacle | Description |
|----------|-------------|
| Linéarité | Pensée cause → effet simple |
| Temporalité | Ignorance des effets différés |
| Proportionnalité | Erreurs sur les ratios |

## Structure
- `detect_linearite.py`
- `detect_temporalite.py`
- `detect_proportionnalite.py`
- `training_data/` (données anonymisées)

## Utilisation
```python
from detect_linearite import analyse_raisonnement
resultat = analyse_raisonnement(trace_apprenant)
