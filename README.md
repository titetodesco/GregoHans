# GregoHans - Offshore Safety Analysis Dashboard

Interactive Streamlit dashboard for offshore safety data analysis.

🔗 **Live Demo:** https://gregohans.streamlit.app/

## Features

### 📊 Interactive Visualizations
All visualizations have been upgraded to **Plotly** for full interactivity:
- **Hover tooltips** - See detailed data on hover
- **Zoom & Pan** - Explore data with mouse interactions
- **Dynamic filtering** - Filter data in real-time
- **Export capabilities** - Download filtered data as CSV

### 📑 Dashboard Tabs

1. **🔥 Heatmap por Location** - Interactive heatmap showing risk areas by location with location filtering
2. **📌 Tipo de Evento** - Event type distribution with color-coded horizontal bar chart
3. **🧯 Severidade (RAM Potential)** - RAM potential analysis with dual view (pie chart + bar chart)
4. **🛠️ Tarefas / Atividades** - Top activities with adjustable slider (5-20 items)
5. **⚠️ Consequências** - Consequences distribution with dual visualization
6. **💥 Severidade vs Risk Area** - Correlation heatmap between severity and risk areas
7. **🎯 Análise Interativa** - Advanced interactive analysis with:
   - Dynamic multi-select filters (Event Type, RAM Potential, Risk Area)
   - Scatter plot showing event intensity by risk area
   - Treemap with hierarchical view (Location > Risk Area > Severity)
   - Violin plot for severity distribution
   - Sunburst chart for circular analysis
   - Combined dashboard with 4 subplots
   - Data preview table
   - CSV export functionality

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run gregohans2.py
```

Then upload an Excel file (.xlsx) with the required columns:
- Location
- Risk Area
- Event Type
- RAM Potential
- Task / Activity
- Consequences

## Requirements

- streamlit>=1.25.0
- pandas>=1.3.0
- openpyxl>=3.0.0
- seaborn>=0.11.0
- matplotlib>=3.3.0
- plotly>=5.0.0

## What's New

✨ **Interactive Graphics Update**
- Replaced static matplotlib/seaborn charts with interactive Plotly visualizations
- Added new "Análise Interativa" tab with advanced filtering and multiple chart types
- All charts now support zoom, pan, hover tooltips, and dynamic interactions
- Added data export capability for filtered datasets
- Enhanced user experience with adjustable parameters and real-time updates
