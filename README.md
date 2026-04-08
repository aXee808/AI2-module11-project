# \#AI2-module11-project

\## Examen blanc pour titre RNCP 

Projet complet de data science sur problematique industrielle, a savoir

ameliorer la maintenance predictive sur 3 sites de production.



\### Analyse fonctionnelle \& technique (rapport\_analyse/BC01\_BC02.pdf)



* Analyse des systèmes OT et IT
* Analyse des besoins metiers
* Analyse des besoins fonctionnels
* Cartographie des processus (BPMN,Data Flow Diagram)
* Risques et integrite des donnees
* Fonctionnalites et priorisation
* Conformite (RGPD)
* Architecture fonctionnelle (User Case Diagram, Sequence Diagram)
* Architecture technique (target infrastructure schema)
* Analyse des risques cybernetiques



\### Projet ML (ml\_project/BC03\_BC04.ipynb)



Jupyter Notebook (Python, Pandas, Scikit Learn, XGboost



* Exploration des donnees (matplotlib, seaborn)
* Recherche de corrélations (heatmap)
* Transformation / Enrichissement des données (recalcul de l'age, moyennes glissantes)
* Preprocessing / Gestion du désequilibre des classes (sous echantillonage)
* Modelisation (GridSearchCV sur les modeles Random Forest et XGBoost)
* Estimation des performances des modèles (Accuracy/Precision/Recall/F1 Score/Matrice de confusion)
* Sauvegarde du meilleur modele XGBoost (joblib)



\### IHM Monitoring d'alerte défaillance (api/\* , ihm/\*)



* module python pour generer aleatoirement des mesures capteurs
* API (FastAPI) pour servir les inferences du meilleur modele
* interface IHM via page streamlit 



\### Dashboard pour la direction (dashboard/\*)



Rapport PowerBI











