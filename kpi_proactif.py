"""
kpi_proactif.py – Indice d'Anticipation (KPI Proactif)
Mesure l'écart entre le signal faible et l'action corrective.
Valide le passage du raisonnement réactif au raisonnement proactif.
"""

from datetime import datetime, timedelta
from typing import Union, Optional
import json

class KPIAnticipation:
    """
    Calcule le score de proactivité de l'apprenant.
    
    Le KPI d'Anticipation évalue la capacité à intervenir 
    avant qu'un seuil critique ne soit atteint, sur la base
    des alertes prédictives générées par la BDI.
    """
    
    def __init__(self):
        self.historique_scores = []
        
    def evaluer(self, 
                t_alerte: Union[datetime, float], 
                t_action: Union[datetime, float], 
                t_critique: Union[datetime, float],
                verbose: bool = False) -> float:
        """
        Calcule le score de proactivité.
        
        Paramètres:
            t_alerte   : Moment de l'alerte prédictive BDI (Signal faible)
            t_action   : Moment de l'intervention de l'apprenant
            t_critique : Moment estimé du seuil critique (crash système)
            verbose    : Affiche les détails du calcul
            
        Retourne:
            Score compris entre 0 et 100
        """
        
        # Convertir en secondes si nécessaire (pour compatibilité avec variantes)
        if isinstance(t_alerte, datetime):
            t_alerte = t_alerte.timestamp()
        if isinstance(t_action, datetime):
            t_action = t_action.timestamp()
        if isinstance(t_critique, datetime):
            t_critique = t_critique.timestamp()
        
        fenetre_decision = t_critique - t_alerte
        delai_reaction = t_action - t_alerte
        
        # Cas d'échec : action trop tardive ou inexistante
        if t_action >= t_critique:
            score = 0.0
            niveau = "Échec – Action hors délai"
        elif delai_reaction <= 0:
            score = 100.0
            niveau = "Parfait – Action avant l'alerte"
        else:
            # Plus l'action est proche de l'alerte (et loin de la crise), plus le score est haut
            score = (1 - (delai_reaction / fenetre_decision)) * 100
            score = round(max(0, min(100, score)), 2)
            
            if score >= 80:
                niveau = "Martinet Confirmé – Anticipation exceptionnelle"
            elif score >= 60:
                niveau = "Martinet en Vol – Anticipation satisfaisante"
            elif score >= 40:
                niveau = "Martinet Apprenti – Anticipation en construction"
            else:
                niveau = "Poussin – Réaction tardive (post-urgence)"
        
        # Enregistrement dans l'historique
        self.historique_scores.append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "delai_reaction": delai_reaction,
            "fenetre_decision": fenetre_decision,
            "niveau": niveau
        })
        
        if verbose:
            print(f"📊 KPI d'Anticipation")
            print(f"   Fenêtre de décision : {fenetre_decision:.0f} secondes")
            print(f"   Délai de réaction   : {delai_reaction:.0f} secondes")
            print(f"   Score               : {score}%")
            print(f"   Niveau              : {niveau}")
        
        return score
    
    def evaluer_serie(self, evenements: list) -> dict:
        """
        Évalue une série d'événements et retourne des statistiques.
        
        Paramètres:
            evenements: Liste de dictionnaires avec clés 't_alerte', 't_action', 't_critique'
        """
        scores = []
        for evt in evenements:
            score = self.evaluer(evt['t_alerte'], evt['t_action'], evt['t_critique'])
            scores.append(score)
        
        score_moyen = sum(scores) / len(scores) if scores else 0
        
        return {
            "scores_individuels": scores,
            "score_moyen": round(score_moyen, 2),
            "nombre_evenements": len(scores),
            "taux_reussite": len([s for s in scores if s >= 60]) / len(scores) if scores else 0
        }
    
    def generer_rapport_longitudinal(self) -> dict:
        """Génère un rapport de progression sur la durée."""
        if not self.historique_scores:
            return {"erreur": "Aucune donnée historique"}
        
        scores = [entry["score"] for entry in self.historique_scores]
        tendance = "Progression" if scores[-1] > scores[0] else "Régression" if scores[-1] < scores[0] else "Stable"
        
        return {
            "score_initial": scores[0],
            "score_actuel": scores[-1],
            "score_max": max(scores),
            "score_min": min(scores),
            "evolution": scores[-1] - scores[0],
            "tendance": tendance
        }


# SIMULATION DE SCÉNARIO POUR L'ORAL
# ----------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATION DU KPI D'ANTICIPATION")
    print("=" * 60)
    
    kpi = KPIAnticipation()
    
    # Paramètres du scénario
    # Alerte à t=0 (10:00), seuil critique à t=60 (11:00)
    alerte = 0
    critique = 60
    
    print("\n📈 Scénario 1 : Le Martinet Confirmé (Action à 10:15)")
    score_a = kpi.evaluer(alerte, 15, critique, verbose=True)
    
    print("\n📉 Scénario 2 : Le Poussin Réactif (Action à 10:55)")
    score_b = kpi.evaluer(alerte, 55, critique, verbose=True)
    
    print("\n📊 Scénario 3 : Série d'événements (Suivi longitudinal)")
    evenements_test = [
        {"t_alerte": 0, "t_action": 50, "t_critique": 60},   # Poussin
        {"t_alerte": 0, "t_action": 35, "t_critique": 60},   # Goéland
        {"t_alerte": 0, "t_action": 20, "t_critique": 60},   # Martinet
        {"t_alerte": 0, "t_action": 12, "t_critique": 60},   # Martinet Confirmé
    ]
    
    for i, evt in enumerate(evenements_test, 1):
        score = kpi.evaluer(evt['t_alerte'], evt['t_action'], evt['t_critique'])
        print(f"   Épisode {i} : Score = {score}%")
    
    print("\n📈 Rapport longitudinal :")
    rapport = kpi.generer_rapport_longitudinal()
    print(f"   Évolution : {rapport['evolution']:.2f} points")
    print(f"   Tendance : {rapport['tendance']}")
    
    print("\n" + "=" * 60)
    print("✅ Fin de la simulation")
