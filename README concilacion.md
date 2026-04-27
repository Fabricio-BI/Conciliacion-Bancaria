# 🏦 Conciliación Bancaria Automatizada con Python

> Herramienta de conciliación bancaria en Python que combina **matching exacto** y **fuzzy matching** para identificar y cruzar automáticamente registros entre el mayor contable y el estado de cuenta bancario.

---

## 📋 Descripción

Este proyecto automatiza el proceso de conciliación bancaria, comparando el mayor contable de la empresa contra el estado de cuenta bancario. Utiliza dos capas de matching para maximizar las coincidencias:

- **Capa 1 — Merge exacto:** Cruza registros donde la referencia y el importe coinciden perfectamente.
- **Capa 2 — Fuzzy Matching:** Detecta coincidencias donde las referencias tienen pequeñas diferencias de formato (espacios, guiones, ceros, mayúsculas/minúsculas), pero corresponden al mismo movimiento.

El resultado final es un archivo Excel con 6 pestañas que resume todo el estado de la conciliación.

---

## 🗂️ Estructura del proyecto

```
conciliacion-bancaria/
│
├── conciliacion.ipynb        # Notebook principal con todo el flujo
├── README.md                 # Este archivo
│
└── data/
    ├── mayor_contable.xlsx   # Mayor contable de la empresa
    └── estado_cuenta.xlsx    # Estado de cuenta bancario (2 pestañas: Guayaquil, Pacifico)
```

---

## ⚙️ Requisitos

```bash
pip install pandas openpyxl rapidfuzz
```

| Librería | Uso |
|----------|-----|
| `pandas` | Manipulación de datos y merge |
| `openpyxl` | Exportar y dar formato al Excel de resultados |
| `rapidfuzz` | Fuzzy matching de referencias (~10x más rápido que fuzzywuzzy) |

---

## 🔄 Flujo del proceso

```
ENTRADA
  mayor_contable.xlsx  +  estado_cuenta.xlsx (Guayaquil + Pacifico)
          │
          ▼
  Normalizar importes (.abs())
          │
          ▼
  ┌──────────────────────────┐
  │  CAPA 1: Merge exacto    │  Referencia + Importe iguales
  └────────────┬─────────────┘
               │
       ┌───────┴────────┐
       ✓ Conciliados    ✗ Sin match
                        │
                        ▼
          ┌─────────────────────────┐
          │  CAPA 2: Fuzzy Matching │  Importe exacto +
          │                         │  Referencia parecida ≥ 80%
          └─────────────┬───────────┘
                        │
               ┌────────┴────────┐
               ✓ Conciliados     ✗ Sin match
               (marcados fuzzy)  (requieren revisión manual)
                        │
                        ▼
              SALIDA: Excel con 6 pestañas
```

---

## 📊 Estructura del Excel de salida

| Pestaña | Contenido |
|---------|-----------|
| `Resumen` | Totales de registros e importes por categoría + % conciliado |
| `Mayor vs Banco` | Todos los registros del mayor (filas fuzzy en 🟡 amarillo) |
| `Banco vs Mayor` | Todos los registros del banco (filas fuzzy en 🟡 amarillo) |
| `Partidas Pendientes` | Registros del mayor sin match |
| `Depósitos Sobrantes` | Registros del banco sin match |
| `Fuzzy Matches` | Detalle de todas las coincidencias aproximadas con su score |

---

## 📁 Formato de los archivos de entrada

### `mayor_contable.xlsx`

| Columna | Descripción |
|---------|-------------|
| `Ref_transaccion` | Referencia del movimiento en el mayor |
| `Importe en moneda local` | Importe del movimiento (puede ser negativo) |
| `Fecha de documento` | Fecha del registro contable |
| `Clave_2` | Clave interna del registro |

### `estado_cuenta.xlsx` (pestañas: Guayaquil / Pacifico)

| Columna | Descripción |
|---------|-------------|
| `Referencia` | Referencia del movimiento bancario |
| `Importe` | Importe del depósito |
| `Banco` | Nombre del banco |
| `Cuenta bancaria` | Número de cuenta acreditada |
| `Fecha valor` | Fecha de acreditación |
| `Descripción de la operación` | Descripción del movimiento |

---

## 🧠 Lógica del Fuzzy Matching

El fuzzy matching usa `fuzz.partial_ratio` de `rapidfuzz`, que es ideal para referencias bancarias porque:

- Detecta si una cadena está **contenida dentro de otra**
- Maneja bien **prefijos o sufijos distintos**
- Tolera **guiones, espacios y ceros** que el banco y el mayor registran diferente

**Ejemplo:**
```
Mayor:  "TRF-2024-001"
Banco:  "TRF2024001"
Score:  91  ✓  (supera umbral de 80)

Mayor:  "TRF-2024-001"
Banco:  "ABC-9999"
Score:  23  ✗  (no supera umbral)
```

El umbral por defecto es **80**. Puedes ajustarlo en el notebook según la calidad de tus datos:

```python
UMBRAL = 80  # Aumentar para mayor precisión, bajar para mayor cobertura
```

---

## 🚀 Cómo usar

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/conciliacion-bancaria.git
```

2. Instala las dependencias:
```bash
pip install pandas openpyxl rapidfuzz
```

3. Coloca tus archivos en la carpeta `data/`:
   - `mayor_contable.xlsx`
   - `estado_cuenta.xlsx` (con pestañas Guayaquil y Pacifico)

4. Abre y ejecuta `conciliacion.ipynb` en Google Colab o Jupyter Notebook.

5. El archivo `conciliacion_resultado.xlsx` se guardará automáticamente en tu Google Drive.

---

## 📈 Ejemplo de resumen de resultados

| Categoría | Registros Mayor | Importe Mayor | Registros Banco | Importe Banco |
|-----------|:--------------:|:-------------:|:--------------:|:-------------:|
| Total registros | 500 | $1,250,000 | 480 | $1,248,500 |
| Coincidencias exactas | 420 | $1,100,000 | 415 | $1,095,000 |
| Coincidencias fuzzy | 45 | $115,000 | 42 | $112,500 |
| **Total conciliado** | **465** | **$1,215,000** | **457** | **$1,207,500** |
| **% Conciliado** | **93%** | **97.2%** | **95.2%** | **96.7%** |
| Partidas pendientes | 35 | $35,000 | — | — |
| Depósitos sobrantes | — | — | 23 | $41,000 |
| Diferencia | 12 | -$6,000 | — | — |

---

## 🛠️ Personalización

Puedes adaptar el código para tu caso de uso:

- **Cambiar el umbral de fuzzy:** Modifica `UMBRAL = 80` en el notebook.
- **Agregar más bancos:** Añade más pestañas al `estado_cuenta.xlsx` y agrégalas al `pd.concat`.
- **Tolerancia en importe:** Reemplaza la igualdad exacta de importe por un rango `±0.01` para manejar redondeos.
- **Normalizar referencias:** Agrega `.str.strip().str.upper()` antes del merge para reducir falsos negativos.

---

## 📄 Licencia

MIT License — libre para uso personal y comercial.

---

## 👤 Autor

Desarrollado por **[Tu Nombre]**
📧 contacto@tudominio.com
🌐 [tu-sitio-web.com](https://tu-sitio-web.com)

> ¿Necesitas este proceso implementado para tu empresa? Contáctame para una consultoría personalizada.
