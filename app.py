import streamlit as st
import pandas as pd

# Seiteneinstellungen
st.set_page_config(page_title="Interaktiver Wirtschaftskreislauf", layout="wide")

st.title("🎓 Interaktiver Erweiterter Wirtschaftskreislauf")
st.markdown("""
Nutzen Sie die Regler in der Seitenleiste, um die Geldströme zu verändern. 
Beobachten Sie, wie sich die Einnahmen und Ausgaben der Sektoren verschieben.
""")

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

# Annahmen für die anderen Sektoren (vereinfacht)
staatsausgaben = steuern_hh * 0.9 # Staat gibt fast alles wieder aus
subventionen = staatsausgaben * 0.3
transfers = staatsausgaben * 0.4
exporte = importe * 1.1 # Handelsbilanzüberschuss angenommen

# --- VISUALISIERUNG: Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Der Geldfluss im Überblick")
    
 # Graphviz Diagramm (Die stabilere Alternative)
    dot_code = f"""
    digraph G {{
        rankdir=LR;
        node [shape=box, style="filled,rounded", fontname="Arial", fontsize="12"];
        
        HH [label="Private Haushalte", fillcolor="#FFCC99"];
        UN [label="Unternehmen", fillcolor="#FFCC99"];
        ST [label="Staat", fillcolor="#99CCFF"];
        BK [label="Banken", fillcolor="#99FF99"];
        AU [label="Ausland", fillcolor="#FFFF99"];

        HH -> UN [label=" Konsum ({konsum_inland:.0f}€)", color="#333333"];
        UN -> HH [label=" Einkommen ({einkommen:.0f}€)", color="#333333"];
        
        HH -> ST [label=" Steuern ({steuern_hh:.0f}€)", color="red"];
        ST -> HH [label=" Transfers ({transfers:.0f}€)", color="blue"];
        
        UN -> ST [label=" Steuern (200€)", color="red"];
        ST -> UN [label=" Subventionen ({subventionen:.0f}€)", color="blue"];
        
        HH -> BK [label=" Sparen ({sparen:.0f}€)", color="green"];
        BK -> UN [label=" Investitionen", color="green"];
        
        HH -> AU [label=" Importe ({importe:.0f}€)", color="#666666"];
        AU -> UN [label=" Exporte ({exporte:.0f}€)", color="#666666"];
    }}
    """
    st.graphviz_chart(dot_code)  

with col2:
    st.subheader("Sektoren-Bilanzen")
    st.write(f"**Haushalte Netto:** {netto:.2f} €")
    st.write(f"**Staatskasse:** {steuern_hh - (transfers + subventionen):.2f} € (Saldo)")
    
    # Kleine Tabelle für den Unterricht
    data = {
        "Strom": ["Konsum Inland", "Steuern HH", "Ersparnis", "Importe"],
        "Wert (€)": [konsum_inland, steuern_hh, sparen, importe]
    }
    st.table(pd.DataFrame(data))


st.info("**Unterrichts-Tipp:** Erhöhen Sie die Sparquote. Was passiert mit dem Konsum bei den Unternehmen? Diskutieren Sie den 'Sparparadoxon'.")
