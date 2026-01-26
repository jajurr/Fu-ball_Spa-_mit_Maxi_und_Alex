import streamlit as st

st.set_page_config(
    page_title="Fußball Datenbank – IuK II",
    layout="wide"
)

st.title("Fußball Datenbank – IuK II")
st.subheader("Projekt von: Arne Jurr, Maxi Kohnke & Alex Stäcker")

st.markdown("---")

st.markdown(
    """
    ### Projektbeschreibung

    Diese Anwendung ist im Rahmen des Moduls **Informations- und Kommunikationstechnik II**
    entstanden. Ziel des Projekts ist es, Daten der Ersten und Zweiten FußBall Bundesliga
    strukturiert in einer Datenbank zu speichern
    und interaktiv auszuwerten.
    """
)

st.markdown(
    """
    Die Daten stammen aus der **OpenLigaDB API** und wurden automatisiert in eine
    SQLite-Datenbank überführt.  
    Anschließend können die Daten hier ausgewertet und eingesehen werden.
    """
)

st.markdown("---")

