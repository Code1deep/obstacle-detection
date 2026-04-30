# -*- coding: utf-8 -*-
"""
kpi_proactif.py - Indice d'Anticipation (KPI Proactif)
Mesure l'ecart entre le signal faible et l'action corrective.
Valide le passage du raisonnement reactif au raisonnement proactif.
"""

from datetime import datetime, timedelta
from typing import Union, Optional
import json

class KPIAnticipation:
    """
    Calcule le score de proactivite de l'apprenant.
    
    Le KPI d'Anticipation evalue la capacite a intervenir 
    avant qu'un seuil critique ne soit atteint, sur la base
    des alertes predictives generees par la BDI.
    """
    
    def __init__(self):
        self.historique_scores = []
        
    def evaluer(self, 
                t_alerte: Union[datetime, float], 
                t_action: Union[datetime, float], 
                t_critique: Union[datetime, float],
                verbose: bool = False) -> float:
        """
        Calcule le score de proactivite.
        
        Parametres:
            t_alerte   : Moment de l'alerte predictive BDI (Signal faible)
            t_action   : Moment de l'intervention de l'apprenant
            t_critique : Moment estime du seuil critique (crash systeme)
            verbose    : Affiche les details du calcul
            
        Retourne:
            Score compris entre 0 et 100
        """
        
        # Convertir en secondes si necessaire (pour compatibilite avec variantes)
        if isinstance(t_alerte, datetime):
            t_alerte = t_alerte.timestamp()
        if isinstance(t_action, datetime):
            t_action = t_action.timestamp()
        if isinstance(t_critique, datetime):
            t_critique = t_critique.timestamp()
        
        fenetre_decision = t_critique - t_alerte
        delai_reaction = t_action - t_alerte
        
        # Cas d'echec : action trop tardive ou inexistante
        if t_action >= t_critique:
            score = 0.0
            niveau = "Echec - Action hors delai"
        elif delai_reaction <= 0:
            score = 100.0
            niveau = "Parfait - Action avant l'alerte"
        else:
            # Plus l'action est proche de l'alerte (et loin de la crise), plus le score est haut
            score = (1 - (delai_reaction / fenetre_decision)) * 100
            score = round(max(0, min(100, score)), 2)
            
            if score >= 80:
                niveau = "Martinet Confirme - Anticipation exceptionnelle"
            elif score >= 60:
                niveau = "Martinet en Vol - Anticipation satisfaisante"
            elif score >= 40:
                niveau = "Martinet Apprenti - Anticipation en construction"
            else:
                niveau = "Poussin - Reaction tardive (post-urgence)"
        
        # Enregistrement dans l'historique
        self.historique_scores.append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "delai_reaction": delai_reaction,
            "fenetre_decision": fenetre_decision,
            "niveau": niveau
        })
        
        if verbose:
            print("KPI d'Anticipation")
            print("   Fenetre de decision : {:.0f} secondes".format(fenetre_decision))
            print("   Delai de reaction   : {:.0f} secondes".format(delai_reaction))
            print("   Score               : {}%".format(score))
            print("   Niveau              : {}".format(niveau))
        
        return score
    
    def evaluer_serie(self, evenements: list) -> dict:
        """
        Evalue une serie d'evenements et retourne des statistiques.
        
        Parametres:
            evenements: Liste de dictionnaires avec cles 't_alerte', 't_action', 't_critique'
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
        """Genere un rapport de progression sur la duree."""
        if not self.historique_scores:
            return {"erreur": "Aucune donnee historique"}
        
        scores = [entry["score"] for entry in self.historique_scores]
        tendance = "Progression" if scores[-1] > scores[0] else "Regression" if scores[-1] < scores[0] else "Stable"
        
        return {
            "score_initial": scores[0],
            "score_actuel": scores[-1],
            "score_max": max(scores),
            "score_min": min(scores),
            "evolution": scores[-1] - scores[0],
            "tendance": tendance
        }


# SIMULATION DE SCENARIO POUR L'ORAL
# ------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("SIMULATION DU KPI D'ANTICIPATION")
    print("=" * 60)
    
    kpi = KPIAnticipation()
    
    # Parametres du scenario
    # Alerte a t=0 (10:00), seuil critique a t=60 (11:00)
    alerte = 0
    critique = 60
    
    print("\nScenario 1 : Le Martinet Confirme (Action a 10:15)")
    score_a = kpi.evaluer(alerte, 15, critique, verbose=True)
    
    print("\nScenario 2 : Le Poussin Reactif (Action a 10:55)")
    score_b = kpi.evaluer(alerte, 55, critique, verbose=True)
    
    print("\nScenario 3 : Serie d'evenements (Suivi longitudinal)")
    evenements_test = [
        {"t_alerte": 0, "t_action": 50, "t_critique": 60},   # Poussin
        {"t_alerte": 0, "t_action": 35, "t_critique": 60},   # Goeland
        {"t_alerte": 0, "t_action": 20, "t_critique": 60},   # Martinet
        {"t_alerte": 0, "t_action": 12, "t_critique": 60},   # Martinet Confirme
    ]
    
    for i, evt in enumerate(evenements_test, 1):
        score = kpi.evaluer(evt['t_alerte'], evt['t_action'], evt['t_critique'])
        print("   Episode {} : Score = {}%".format(i, score))
    
    print("\nRapport longitudinal :")
    rapport = kpi.generer_rapport_longitudinal()
    print("   Evolution : {:.2f} points".format(rapport['evolution']))
    print("   Tendance : {}".format(rapport['tendance']))
    
    print("\n" + "=" * 60)
    print("Fin de la simulation")
