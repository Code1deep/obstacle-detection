"""
detect_linearite.py – Détection des raisonnements linéaires (cause → effet simple)
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ResultatDetection:
    obstacle: str
    confiance: float
    details: str

def analyser_raisonnement(trace_apprenant: List[Dict[str, Any]]) -> ResultatDetection:
    """
    Analyse une trace d'apprenant pour détecter un raisonnement linéaire.
    
    Args:
        trace_apprenant: Liste de dictionnaires contenant les actions/réponses
        
    Returns:
        ResultatDetection avec le type d'obstacle, confiance et détails
    """
    # Version simplifiée – à enrichir avec des modèles ML
    score_linearite = 0.0
    details = []
    
    for action in trace_apprenant:
        # Détection de motifs de linéarité
        if action.get("type") == "ajustement_unidirectionnel":
            score_linearite += 0.3
            details.append("Ajustement sans vérification rétroaction")
        
        if action.get("type") == "ignorer_interaction":
            score_linearite += 0.4
            details.append("Interaction entre variables ignorée")
    
    score_linearite = min(score_linearite, 1.0)
    
    return ResultatDetection(
        obstacle="linearite",
        confiance=score_linearite,
        details=" | ".join(details) if details else "Aucun motif détecté"
    )
