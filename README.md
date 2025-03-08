# minUI4
Minimalist UI kit for PyQt4

## structure du projet

```
/minUI4/
│── /minui4/
│   │── __init__.py
│   │── widgets/
│   │   │── __init__.py
│   │   │── base_widget.py  # Classe de base pour les widgets personnalisés
│   │   │── table_widget.py  # Widget pour afficher et manipuler des tables de données
│   │   │── form_widget.py   # Widget pour la saisie et validation de données
│   │   │── chart_widget.py  # Widget pour visualiser les données sous forme de graphiques
│   │── utils/
│   │   │── __init__.py
│   │   │── data_loader.py  # Chargement et transformation des données
│   │   │── validators.py   # Fonctions de validation des données
│── /tests/
│   │── conftest.py  # Configuration de pytest-qt et fixtures
│   │── test_table_widget.py  # Tests unitaires du TableWidget
│   │── test_form_widget.py  # Tests unitaires du FormWidget
│   │── test_chart_widget.py  # Tests unitaires du ChartWidget
│   │── test_utils.py  # Tests des fonctions utilitaires
│── setup.py  # Script d’installation de la bibliothèque
│── README.md  # Documentation de la bibliothèque
```

### Explication :
1. **`widgets/`** : Contient les widgets principaux pour la manipulation des données.
2. **`utils/`** : Contient des fonctions d’aide pour le chargement, la validation et la manipulation des données.
3. **`tests/`** : Contient les tests unitaires et d’intégration avec **pytest-qt**.
4. **`conftest.py`** : Configure les fixtures de **pytest-qt** pour tester les widgets avec Qt.
5. **`setup.py`** : Permet d’installer la bibliothèque avec `pip install .`.