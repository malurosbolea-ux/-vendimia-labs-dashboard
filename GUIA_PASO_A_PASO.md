# 🍷 Guía paso a paso: desplegar el dashboard de Vendimia Labs

## Qué vas a conseguir
Una web pública tipo `https://vendimia-labs.streamlit.app` con tu dashboard interactivo.
Cualquiera con el enlace puede verlo (el profesor, el tribunal, tu madre).

---

## PASO 1: Crear cuenta en GitHub (si no la tienes)
1. Ve a https://github.com
2. Click en "Sign up"
3. Usa tu email (malurosbolea@gmail.com o el que quieras)
4. Elige un username (por ejemplo: `vendimia-labs-team`)

## PASO 2: Crear un repositorio nuevo
1. En GitHub, click en el botón verde **"New"** (arriba a la izquierda) o ve a https://github.com/new
2. Rellena:
   - **Repository name:** `vendimia-labs-dashboard`
   - **Description:** Dashboard de predicción vinícola - Vendimia Labs
   - Marca **Public** (tiene que ser público para que Streamlit lo vea gratis)
   - Marca **Add a README file**
3. Click en **"Create repository"**

## PASO 3: Subir los archivos del dashboard
1. En la página de tu repositorio, click en **"Add file" → "Upload files"**
2. Arrastra estos 4 archivos (los que te he dado en el ZIP):
   - `app.py` (el dashboard)
   - `requirements.txt` (las librerías)
   - `logo.png` (vuestro logo)
   - `README.md` (descripción del proyecto)
3. Click en **"Commit changes"**

### IMPORTANTE: Crear la carpeta .streamlit
4. Vuelve al repositorio, click en **"Add file" → "Create new file"**
5. En el nombre del archivo escribe exactamente: `.streamlit/config.toml`
   (al escribir la barra / se crea la carpeta automáticamente)
6. Pega este contenido:

```toml
[theme]
primaryColor = "#C9A84C"
backgroundColor = "#1A0508"
secondaryBackgroundColor = "#2D0E14"
textColor = "#F5EDD6"
font = "sans serif"

[server]
headless = true
```

7. Click en **"Commit changes"**

### Tu repositorio debería tener esta estructura:
```
vendimia-labs-dashboard/
├── .streamlit/
│   └── config.toml
├── app.py
├── logo.png
├── requirements.txt
└── README.md
```

## PASO 4: Desplegar en Streamlit Community Cloud
1. Ve a https://share.streamlit.io
2. Click en **"Sign in with GitHub"** (usa la misma cuenta de GitHub)
3. Acepta los permisos
4. Click en **"New app"**
5. Rellena:
   - **Repository:** elige `vendimia-labs-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. En **"App URL"** puedes personalizar la dirección, por ejemplo:
   - `vendimia-labs` → quedará como `vendimia-labs.streamlit.app`
7. Click en **"Deploy!"**

## PASO 5: Esperar ~2-3 minutos
Streamlit va a:
- Leer tu repositorio
- Instalar las librerías del requirements.txt
- Arrancar la app

Cuando termine, verás tu dashboard en vivo. La URL será algo como:
**https://vendimia-labs.streamlit.app**

---

## FAQ: Problemas comunes

**P: Me da error de "ModuleNotFoundError"**
R: Asegúrate de que requirements.txt está en la raíz del repositorio (no dentro de una carpeta).

**P: No se ve el logo**
R: Comprueba que logo.png está en la raíz del repositorio (al mismo nivel que app.py).

**P: El tema sale con colores blancos**
R: La carpeta .streamlit tiene que tener el punto delante. Revisa que se llama exactamente `.streamlit/config.toml`.

**P: ¿Puedo cambiarlo después?**
R: Sí. Cada vez que hagas un cambio en GitHub, Streamlit se actualiza automáticamente en ~1 minuto.

**P: ¿Cuesta dinero?**
R: No. Streamlit Community Cloud es gratis para siempre para apps públicas.

**P: ¿Se puede hacer privado?**
R: En el plan gratis no. Pero para la defensa quieres que sea público precisamente.

---

## Para la defensa
1. Abre el enlace en el navegador
2. Muestra cómo los filtros del sidebar cambian los datos en tiempo real
3. Enseña las 4 pestañas: visión general, análisis por variedad, evolución del modelo, descarga
4. Di algo como: "Esto es lo que el cliente vería realmente. No un notebook de 9 horas, sino un panel interactivo donde en 2 clicks tiene sus predicciones por variedad, modo de cultivo y tipo."

¡A por esa matrícula! 🍷
