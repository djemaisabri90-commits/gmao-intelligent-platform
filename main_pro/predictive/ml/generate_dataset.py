# predictive/ml/generate_dataset.py

import random
import pandas as pd
import numpy as np
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_pro.settings")
import django
django.setup()

def generate_synthetic_data(n=1000, seed=None, minority_ratio=0.2):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    n_minority = int(n * minority_ratio)
    n_majority = n - n_minority

    def make_sample(is_minority=False):
        if is_minority:
            l_total_int, l_recent_int, l_recent_notif = 15, 7, 8
            p_stock_critique = 0.6
            l_pending = 4  # Plus de tâches en attente en cas de panne
            l_high_prio = 3 # Plus de WO prioritaires
        else:
            l_total_int, l_recent_int, l_recent_notif = 5, 1, 2
            p_stock_critique = 0.05
            l_pending = 1
            l_high_prio = 0

        total_interventions = np.random.poisson(l_total_int)
        recent_interventions = np.random.poisson(l_recent_int)
        recent_notifications = np.random.poisson(l_recent_notif)
        
        total_pieces_used = np.random.poisson(40 if is_minority else 15)
        stock_critique = 1 if (np.random.random() < p_stock_critique) else 0

        workorders_en_cours = np.random.poisson(3 if is_minority else 1)
        workorders_clos = np.random.poisson(l_total_int - 2 if is_minority else 3)
        
        # --- AJOUT DES COLONNES MANQUANTES ---
        pending_interventions = np.random.poisson(l_pending)
        high_priority_workorders = np.random.poisson(l_high_prio)
        total_workorders = workorders_en_cours + workorders_clos + high_priority_workorders
        # -------------------------------------

        validated_interventions = max(0, total_interventions - np.random.poisson(2))
        is_in_failure = 1 if (recent_interventions > 4 or stock_critique == 1) else 0

        return {
            "machine_id": 0, # Pour l'alignement, bien que non prédictif
            "total_interventions": total_interventions,
            "recent_interventions": recent_interventions,
            "validated_interventions": validated_interventions,
            "pending_interventions": pending_interventions, # Sync
            "total_workorders": total_workorders,           # Sync
            "high_priority_workorders": high_priority_workorders, # Sync
            "workorders_en_cours": workorders_en_cours,
            "workorders_clos": workorders_clos,             # Sync
            "total_pieces_used": total_pieces_used,
            "stock_critique": stock_critique,
            "recent_notifications": recent_notifications,
            "is_in_failure": is_in_failure,
            "target": 1 if is_minority else 0
        }

    samples = [make_sample(is_minority=False) for _ in range(n_majority)]
    samples += [make_sample(is_minority=True) for _ in range(n_minority)]

    return pd.DataFrame(samples).sample(frac=1, random_state=seed).reset_index(drop=True)

