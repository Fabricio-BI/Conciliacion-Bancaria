# Conciliación Bancaria Automatizada con Python

> Herramienta de conciliación bancaria en Python que combina **matching exacto** y **fuzzy matching** para identificar y cruzar automáticamente registros entre el mayor contable y el estado de cuenta bancario.

---

## Descripción

Este proyecto automatiza el proceso de conciliación bancaria, comparando el mayor contable de la empresa contra el estado de cuenta bancario. Utiliza dos capas de matching para maximizar las coincidencias:

- **Capa 1 — Merge exacto:** Cruza registros donde la referencia y el importe coinciden perfectamente.
- **Capa 2 — Fuzzy Matching:** Detecta coincidencias donde las referencias tienen pequeñas diferencias de formato (espacios, guiones, ceros, mayúsculas/minúsculas), pero corresponden al mismo movimiento.

El resultado final es un archivo Excel con 6 pestañas que resume todo el estado de la conciliación.

---

## 🗂️ Estructura del proyecto

```
conciliacion-bancaria/
│
└── 01_Datos_Entrada/
│   ├── mayor_contable.xlsx          # Mayor contable de la empresa
│   └── estado_cuenta.xlsx           # Estado de cuenta bancario (2 pestañas: Guayaquil, Pacifico)
│ 
└── 02_Resultado/
│   └── concilaicon_resultado.xlsx   # Archivo final de la conciliacion(incluye informe final)
│
└── conciliacion.py                  # Script que contiene todas las funciones usadas en el proyecto
│
└── main.py                          # Script principal con todo el flujo
│
└── README.md                        # Este archivo

```

---



## Requisitos

```bash
pip install pandas openpyxl rapidfuzz
```

 Librería 
| Librería | Objetivo de uso |
|---------|-----------|
| `pandas` | Manipulación de datos y merge |
| `openpyxl` | Exportar y dar formato al Excel de resultados |
| `rapidfuzz` | Fuzzy matching de referencias (~10x más rápido que fuzzywuzzy) |

---

## Flujo del proceso

```
ENTRADA
  mayor_contable.xlsx  +  estado_cuenta.xlsx (Banco 1  + Banco 2 )
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

##  Estructura del Excel de salida

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
| `Fecha de documento` | Fecha de la transaccion |
| `Fe.contabilización` | Fecha del registro contable |
| `Nº documento` | Numero de documento generado en el registro |
| `Referencia_x` | Tipo de transaccion registrada |
| `Moneda local` | Moneda del registro |
| `Importe en moneda local` | Importe del movimiento (puede ser negativo) |
| `Ref_transaccion` | Referencia del movimiento en el mayor |
| `Clave_2` | Nombre del punto de venta donde se realizo la transaccion |

### `estado_cuenta.xlsx` (pestañas: Guayaquil / Pacifico)

| Columna | Descripción |
|---------|-------------|
| `Banco` | Nombre del banco |
| `Cuenta bancaria` | Número de cuenta acreditada |
| `Referencia` | Referencia del movimiento bancario |
| `Descripción de la operación` | Descripción del movimiento |
| `Fecha valor` | Fecha de acreditación |
| `Importe` | Importe del depósito |


##  Lógica de la conciliacion exacta (Capa 1)
La conciliacion se realiza tomando la referencia tanto del archivo del mayor y del estado de cuenta . Esta referencia corresponde a un numero que se le asigna a cada transaccion que se genera en el punto de venta . El segundo parametro que se usa es el Importe . Para mayor precision se usan ambos parametros 


---

##  Lógica del Fuzzy Matching (Capa 2)

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
## 📊 Resultado : Estructura del Excel de salida
 
El archivo `conciliacion_resultado.xlsx` contiene **6 pestañas** diseñadas para cubrir cada etapa del proceso de revisión contable.
 
---
 
### 🟦 Pestaña 1 — `Resumen`
 
**¿Qué contiene?**
Vista ejecutiva con el estado global de la conciliación: total de registros, coincidencias exactas, coincidencias fuzzy, porcentaje conciliado, importes por categoría y diferencia final entre partidas pendientes y depósitos sobrantes.
 
**Formato:** fondo azul en encabezados, verde para conciliados, naranja para pendientes.
 
**¿Para qué sirve?**
Es la primera hoja que debe ver el CFO o gerente financiero. En 30 segundos permite saber si la conciliación cerró bien, cuánto importe quedó sin cruzar y si hay diferencias que requieren atención. Elimina la necesidad de revisar hoja por hoja para tener una foto del estado general.

![Resumen](Docs/Informe%20Final.JPG)
 
---
 
### 🟩 Pestaña 2 — `Mayor vs Banco`
 
**¿Qué contiene?**
Todos los registros del mayor contable con las columnas del banco añadidas donde hubo coincidencia — banco, cuenta acreditada, fecha de acreditación e importe acreditado. Las filas conciliadas por fuzzy matching aparecen resaltadas en 🟡 amarillo.
 
**¿Para qué sirve?**
Permite al contador verificar, registro por registro del mayor, si cada movimiento contable tiene su correspondiente acreditación bancaria. El color amarillo indica qué coincidencias fueron aproximadas y merecen una revisión rápida antes de cerrar el mes. Los registros sin color y sin datos del banco son los que quedaron sin match.
 
---
 
### 🟩 Pestaña 3 — `Banco vs Mayor`
 
**¿Qué contiene?**
Todos los movimientos del estado de cuenta bancario con las columnas del mayor añadidas donde hubo coincidencia — referencia contable, clave interna e importe en moneda local. Las filas fuzzy aparecen en 🟡 amarillo.
 
**¿Para qué sirve?**
Es el cruce en dirección contraria: confirma que cada depósito que entró al banco tiene su registro contable correspondiente. Útil para detectar depósitos que el banco registró pero que aún no han sido contabilizados en el mayor — un caso frecuente en cierres de mes.
 
---
 
### 🟧 Pestaña 4 — `Partidas Pendientes`
 
**¿Qué contiene?**
Registros del mayor contable que no encontraron coincidencia en el banco después de aplicar ambas capas de matching — ni exacta ni fuzzy.
 
**¿Para qué sirve?**
Esta hoja es la lista de trabajo del contador. Cada registro aquí representa un movimiento contabilizado que no se refleja en el estado de cuenta — puede ser un cheque no cobrado, una transferencia en tránsito, un error de registro o una partida que requiere investigación. Es el insumo directo para las notas de conciliación.
 
---
 
### 🟧 Pestaña 5 — `Depósitos Sobrantes`
 
**¿Qué contiene?**
Movimientos del estado de cuenta bancario que no encontraron coincidencia en el mayor contable después de ambas capas de matching.
 
**¿Para qué sirve?**
Representa dinero que llegó al banco pero que aún no está registrado en la contabilidad. Puede tratarse de depósitos de clientes no identificados, cobros automáticos, intereses bancarios o errores del banco. Esta hoja evita que ingresos reales queden fuera de los libros contables al cierre del período.
 
---
 
### 🔍 Pestaña 6 — `Fuzzy Matches`
 
**¿Qué contiene?**
Detalle completo de todas las coincidencias encontradas por el algoritmo de fuzzy matching — con las columnas del depósito, las columnas de la partida pendiente que cruzó, y la columna `fuzzy_score_referencia` que indica el porcentaje de similitud entre las referencias (0 a 100).
 
**¿Para qué sirve?**
Es la hoja de auditoría del proceso. Permite revisar exactamente qué cruzó el algoritmo y con qué nivel de confianza. Un score de 95 es casi certero; un score de 81 merece revisión visual. Esta transparencia es clave para que el contador pueda validar o rechazar cada match fuzzy con criterio, y para documentar el proceso ante una auditoría externa.

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



---

## 👤 Autor

Desarrollado por **Fabricio Coque**
📧 fabriciocoque@outlook.com
🌐 [Sitio Web](https://fabriciocoque.github.io/)

> ¿Necesitas este proceso implementado para tu empresa? Contáctame para una consultoría personalizada.
