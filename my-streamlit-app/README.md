# 🚴 Tours Bike Count Predictor - Streamlit App

Application interactive Streamlit pour prédire le nombre de vélos comptés à Tours en fonction des conditions météorologiques et des caractéristiques temporelles.

## 🎯 Caractéristiques

- **Prédiction unique** : Entrez les paramètres manuellement et obtenez une prédiction immédiate
- **Prédiction par batch** : Téléchargez un fichier CSV et prédisez pour plusieurs lignes
- **Interface intuitive** : Interface conviviale avec Streamlit
- **Modèle ML** : Utilise un modèle RandomForest pré-entraîné

## 📋 Prérequis

- Python 3.8+
- Fichier du modèle : `../data/bike_count_model.pkl`

## 🚀 Installation

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (optionnel mais recommandé)**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Lancer l'application

```bash
streamlit run streamlit_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## 📊 Fonctionnalités

### 1. Prédiction Unique

Entrez les paramètres manuellement :
- **Température** : Température minimale et maximale en °C
- **Précipitations** : Précipitations totales en mètres
- **Neige** : Profondeur de neige et chutes de neige en mètres
- **Vent** : Rafales de vent maximales en m/s
- **Jour** : Type de jour (weekend, congé, vacances scolaires)

### 2. Prédiction par Batch

Téléchargez un fichier CSV contenant les colonnes suivantes :
- `t2m_min` : Température minimale (°C)
- `t2m_max` : Température maximale (°C)
- `tp_total` : Précipitations totales (m)
- `sd_total` : Profondeur de neige (m)
- `i10fg_max` : Rafales maximales (m/s)
- `sf_max` : Chutes de neige maximales (m)
- `is_weekend` : 0/1 (0 = jour de semaine, 1 = weekend)
- `is_holiday` : 0/1 (0 = pas un congé, 1 = congé)
- `is_school_vacation` : 0/1 (0 = pas de vacances, 1 = vacances)

Les prédictions seront ajoutées à la colonne `predicted_bikes` et vous pourrez télécharger le résultat.

## 📁 Structure du Projet

```
my-streamlit-app/
├── streamlit_app.py    # Application principale Streamlit
├── predictor.py        # Module de prédiction
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

## 🔧 Architecture

- **streamlit_app.py** : Interface utilisateur avec deux onglets (prédiction unique et batch)
- **predictor.py** : Classe `BikeCountPredictor` qui encapsule la logique de prédiction
  - Charge le modèle au démarrage (mis en cache)
  - Prédictions simples et par batch
  - Gestion des erreurs

## 📦 Modèle Utilisé

- **Algorithme** : RandomForestRegressor (100 estimateurs)
- **Données d'entraînement** : 2023-2024
- **Source des données** :
  - Météo : API Copernicus (ERA5)
  - Vélos : Syndicat des Mobilités de Touraine
- **Localisation** : Tours, France

## 🎨 Personnalisation

Vous pouvez modifier l'apparence de l'application en éditant :
- Les couleurs et emojis dans `streamlit_app.py`
- La mise en page avec `st.set_page_config()`
- Les plages de valeurs des sliders/inputs

## ⚠️ Notes Importantes

1. **Fichier du modèle** : Assurez-vous que `bike_count_model.pkl` est présent dans `../data/`
2. **Chemins relatifs** : L'app suppose que le modèle se trouve au niveau parent
3. **Performance** : Le modèle est mis en cache avec `@st.cache_resource` pour les performances

## 🐛 Dépannage

**Erreur : "Model file not found"**
- Vérifiez que `bike_count_model.pkl` existe dans le dossier `../data/`

**Erreur : "Missing columns"**
- Vérifiez que votre CSV contient toutes les colonnes requises

**L'app est lente**
- C'est normal au premier démarrage (chargement du modèle)
- Les appels suivants sont plus rapides grâce au cache

## 📝 Exemple CSV

```csv
t2m_min,t2m_max,tp_total,sd_total,i10fg_max,sf_max,is_weekend,is_holiday,is_school_vacation
-5.0,10.0,0.001,0.0,5.0,0.0,0,0,0
0.0,15.0,0.0,0.0,3.0,0.0,1,0,0
-10.0,5.0,0.01,0.5,8.0,0.1,0,1,0
```

## 📞 Support

Pour les problèmes ou questions, consultez les logs dans la console Streamlit.

## 📄 Licence

Voir le projet parent pour les informations de licence.
