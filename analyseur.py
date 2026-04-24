"""
analyseur.py – Orchestrateur pour la détection d'obstacles cognitifs
"""

from typing import Dict, Any, List
from detect_linearite import analyser_raisonnement as detect_linearite
from detect_temporalite import analyser_temporalite as detect_temporalite
from detect_proportionnalite import analyser_proportionnalite as detect_proportionnalite

def analyser_trace_complete(trace_apprenant: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyse complète d'une trace d'apprenant.
    
    Returns:
        Dictionnaire contenant les obstacles détectés et leurs scores
    """
    resultats = {
        "linearite": detect_linearite(trace_apprenant),
        "temporalite": detect_temporalite(trace_apprenant),
        "proportionnalite": detect_proportionnalite(trace_apprenant)
    }
    
    # Obstacle principal (confiance maximale)
    principal = max(resultats.values(), key=lambda x: x.confiance)
    
    return {
        "obstacle_principal": principal.obstacle,
        "confiance_principale": principal.confiance,
        "tous_obstacles": {
            k: {"confiance": v.confiance, "details": v.details}
            for k, v in resultats.items()
        }
    }
