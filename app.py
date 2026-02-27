import streamlit as st
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Interaktiver Wirtschaftskreislauf", layout="wide")

st.title("🎓 Interaktiver Erweiterter Wirtschaftskreislauf")
st.markdown("### Optimiert für Beamer-Präsentationen")

# --- SIDEBAR: Parameter ---
st.sidebar.header("Parameter anpassen")
einkommen = st.sidebar.slider("Haushaltseinkommen (Löhne/Gehälter)", 500, 5000, 3000, step=100)
steuer_satz = st.sidebar.slider("Steuersatz (in %)", 0, 50, 25) / 100
spar_quote = st.sidebar.slider("Sparquote (in % vom Netto)", 0, 30, 10) / 100
import_quote = st.sidebar.slider("Importquote (Konsum im Ausland in %)", 0, 40, 15) / 100

# --- LOGIK: Berechnung der Ströme ---
steuern_hh = einkommen * steuer_satz
netto = einkommen - steuern_hh
sparen = netto * spar_quote
verfuegbarer_konsum = netto - sparen
importe = verfuegbarer_konsum * import_quote
konsum_inland = verfuegbarer_konsum - importe

# Vereinfachte Annahmen für Ströme
staatsausgaben = steuern_hh * 0.9
subventionen = staatsausgaben * 0.3
transfers = staatsausgaben * 0.4
exporte = importe * 1.1

# Hilfsfunktion für die Linienbreite (Skalierung)
def get_w(val):
    return max(1.0, val / 400) # Mindestens Breite 1, skaliert pro 400€

# --- VISUALISIERUNG ---
col1, col2 = st.columns([3, 1])

with col1:
    # Graphviz Diagramm
    dot_code = f"""
    digraph G {{
        rankdir=LR;
        node [shape=box, style="filled,rounded", fontname="Arial Bold", fontsize="24", margin="0.3"];
        edge [fontname="Arial", fontsize="18"];
        
        // Sektoren
        HH [label="Private\\nHaushalte", fillcolor="#FFCC99"];
        UN [label="Unternehmen", fillcolor="#FFCC99"];
        ST [label="Staat", fillcolor="#99CCFF"];
        BK [label="Banken", fillcolor="#99FF99"];
        AU [label="Ausland", fillcolor="#FFFF99"];

        // GELDSTRÖME (Durchgehende Linien)
        UN -> HH [label=" Einkommen ({einkommen:.0f}€)", penwidth={get_w(einkommen)}, color="#2E7D32"];
        HH -> UN [label=" Konsum Inland ({konsum_inland:.0f}€)", penwidth={get_w(konsum_inland)}, color="#1565C0"];
        
        HH -> ST [label=" Steuern ({steuern_hh:.0f}€)", penwidth={get_w(steuern_hh)}, color="#C62828"];
        ST -> HH [label=" Transfers ({transfers:.0f}€)", penwidth={get_w(transfers)}, color="#1565C0"];
        
        UN -> ST [label=" Steuern (200€)", penwidth=1.5, color="#C62828"];
        ST -> UN [label=" Subventionen ({subventionen:.0f}€)", penwidth={get_w(subventionen)}, color="#1565C0"];
        
        HH -> BK [label=" Sparen ({sparen:.0f}€)", penwidth={get_w(sparen)}, color="#2E7D32"];
        BK -> UN [label=" Investitionen", penwidth=2, color="#2E7D32"];
        
        HH -> AU [label=" Importe ({importe:.0f}€)", penwidth={get_w(importe)}, color="#546E7A"];
        AU -> UN [label=" Exporte ({exporte:.0f}€)", penwidth={get_w(exporte)}, color="#546E7A"];

        // GÜTERSTROM (Gestrichelte Linien - Gegenströme)
        edge [style=dashed, color="#9E9E9E", fontcolor="#757575", fontsize="14"];
        HH -> UN [label=" Produktionsfaktoren\\n(Arbeit, Boden, Kapital)"];
        UN -> HH [label=" Waren & Dienstleistungen"];
    }}
    """
    st.graphviz_chart(dot_code)

with col2:
    st.write("### 📊 Details")
    st.metric("Haushalte Netto", f"{netto:.0f} €")
    st.metric("Staats-Saldo", f"{steuern_hh - (transfers + subventionen):.0f} €")
    
    st.write("**Legende:**")
    st.caption("🟢 Geldzufluss (Einkommen/Sparen)")
    st.caption("🔵 Geldabfluss (Konsum/Transfers)")
    st.caption("🔴 Steuern")
    st.caption("⚪ Gestrichelt: Güterstrom")

st.info("**Tipp:** Bewegen Sie die Regler links. Achten Sie darauf, wie die Pfeile dicker werden, wenn die Beträge steigen!")
