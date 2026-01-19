# 🚀 Guide de Déploiement sur Streamlit Cloud

Ce guide vous aidera à déployer l'application Tours Bike Count Predictor sur Streamlit Cloud.

## 📋 Prérequis

1. **Compte Streamlit Cloud** : https://streamlit.io/cloud
2. **Compte GitHub** : https://github.com
3. **Git** installé sur votre ordinateur
4. Le code de cette application prêt à être pushé

## 🔧 Étapes de Déploiement

### 1. Initialiser le dépôt Git (première fois uniquement)

```bash
cd my-streamlit-app
git init
git add .
git commit -m "Initial commit: Streamlit bike count predictor app"
```

### 2. Créer un nouveau dépôt sur GitHub

1. Allez sur https://github.com/new
2. Créez un nouveau dépôt nommé `tours-bike-predictor` (ou le nom que vous préférez)
3. **Ne pas initialiser avec README.md** (vous l'avez déjà)
4. Copiez l'URL du dépôt (HTTPS)

### 3. Pousser le code vers GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/tours-bike-predictor.git
git branch -M main
git push -u origin main
```

### 4. Connecter Streamlit Cloud

1. Allez sur https://share.streamlit.io/
2. Cliquez sur **"New app"**
3. Sélectionnez votre repository GitHub : `YOUR_USERNAME/tours-bike-predictor`
4. Branche : `main`
5. Main file path : `streamlit_app.py`
6. Cliquez sur **"Deploy"**

### 5. Configuration de Streamlit Cloud (optionnel)

Après le déploiement, vous pouvez ajouter des secrets ou des configurations via :

**Dashboard Streamlit Cloud → Settings → Secrets management**

Pour les secrets (API keys, etc.), créez un fichier `.streamlit/secrets.toml` :

```toml
# .streamlit/secrets.toml
# Exemple pour des API keys
cdsapi_uid = "votre_uid"
cdsapi_key = "votre_key"
```

⚠️ **Ne jamais committer les secrets sur GitHub** ! Utilisez le gestionnaire de secrets de Streamlit Cloud.

## 📁 Structure attendue sur GitHub

```
tours-bike-predictor/
├── streamlit_app.py
├── predictor.py
├── requirements.txt
├── README.md
├── DEPLOYMENT.md
├── sample_data.csv
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml (géré par Streamlit Cloud)
├── data/
│   └── bike_count_model.pkl
├── launch_app.sh
└── launch_app.bat
```

## 🎯 Mises à jour futures

Pour mettre à jour l'application déployée :

```bash
# Faire vos modifications locales
# ...

# Committer et pousser les changements
git add .
git commit -m "Description de vos changements"
git push origin main
```

Streamlit Cloud détectera automatiquement les changements et redéploiera l'application.

## ✅ Checklist avant le déploiement

- [ ] Vérifier que `requirements.txt` contient toutes les dépendances
- [ ] S'assurer que `bike_count_model.pkl` est dans `data/` (à exclure du .gitignore)
- [ ] Vérifier que le chemin du modèle est correct dans `streamlit_app.py`
- [ ] Tester localement : `streamlit run streamlit_app.py`
- [ ] Ajouter un `.gitignore` avec les fichiers à exclure
- [ ] Créer le dépôt GitHub et pousser le code
- [ ] Déployer via Streamlit Cloud

## 🚨 Problèmes courants

### "Module not found"
→ Assurez-vous que tous les packages sont dans `requirements.txt`

### "File not found"
→ Vérifiez les chemins relatifs, utilisez toujours des chemins relatifs à `__file__`

### "Application takes too long to load"
→ Le modèle ML peut être volumineux. Streamlit Cloud a des ressources limitées (1GB RAM)

### "Out of memory"
→ Optimisez la taille du modèle ou envisagez une solution cloud plus robuste

## 🔗 Ressources utiles

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud/get-started)
- [GitHub & Git Tutorial](https://docs.github.com/en/get-started)

## 📞 Support

Pour les problèmes :
1. Vérifiez les logs de Streamlit Cloud (icône "Manage app" → "View logs")
2. Consultez la [FAQ Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud/get-started/troubleshooting)

---

**Bonne chance avec votre déploiement !** 🚴
