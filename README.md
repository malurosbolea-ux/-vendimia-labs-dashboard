# 🍷 Vendimia Labs — Dashboard de predicción vinícola

Dashboard interactivo para la predicción de producción vinícola (campaña 2021).

**Equipo:** María Luisa Ros · Camilo González · Álvaro Verdasco · Jorge Aldavero  
**Asignatura:** Aprendizaje automático y aprendizaje profundo · Marzo 2026

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologías

- **Modelo:** Voting Ensemble (XGBoost + LightGBM + Extra Trees) · RMSE: 5.516 kg · R²: 0.82
- **Dashboard:** Streamlit + Plotly
- **Despliegue:** Streamlit Community Cloud (gratuito)
