# obstacle-detection – Algorithmes d'identification des obstacles cognitifs

[![Licence](https://img.shields.io/badge/Licence-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)

## Objectif

Détecter automatiquement les obstacles cognitifs à partir des traces d'apprentissage, pour permettre un étayage adapté dans ma Base de Données Intelligente (BDI).

## Trois obstacles ciblés

| Obstacle | Description | Exemple |
|----------|-------------|---------|
| **Linéarité** | Pensée cause → effet simple | "Plus d'engrais = plus de plantes" (ignore l'équilibre) |
| **Temporalité** | Ignorance des effets différés | Ajuste un paramètre, attend 5 secondes, ne voit pas de changement |
| **Proportionnalité** | Erreurs sur les ratios et échelles | Double la population de poissons sans doubler la filtration |

## Structure du dépôt
- `detect_linearite.py`
- `detect_temporalite.py`
- `detect_proportionnalite.py`
- `training_data/` (données anonymisées)

## Utilisation
```python
from analyseur import Analyser
from detect_linearite import analyse_raisonnement

# À partir d'une trace d'apprenant (série temporelle)
resultat = analyse_raisonnement(trace_apprenant)

print(f"Obstacle détecté : {resultat.obstacle}")
print(f"Confiance : {resultat.confiance}")
print(f"Détails : {resultat.details}")


## Installation

```bash
git clone https://github.com/Code1deep/obstacle-detection.git
cd obstacle-detection
pip install -r requirements.txt
