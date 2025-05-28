import streamlit as st
from logic import extract_card_block, replace_card_block

st.title("TTC Configuration Copier")

name = st.text_input("CARD Name")
type_ = st.text_input("CARD Type")
slot = st.text_input("CARD Slot")

uploaded_source = st.file_uploader("Upload Source XML", type="xml")
uploaded_dest = st.file_uploader("Upload Destination XML", type="xml")

if st.button("Copy the configuration"):
    if uploaded_source and uploaded_dest and name and type_ and slot:
        source_lines = uploaded_source.read().decode("utf-8").splitlines()
        dest_lines = uploaded_dest.read().decode("utf-8").splitlines()

        block = extract_card_block(source_lines, name, type_, slot)
        if not block:
            st.error("Bloc non trouvé dans le fichier source")
        else:
            modified = replace_card_block(dest_lines, name, type_, slot, block)
            if not modified:
                st.error("Bloc non trouvé dans le fichier destination")
            else:
                st.success("Bloc copié avec succès")
                st.download_button("Télécharger le fichier modifié",
                                   data="\n".join(modified),
                                   file_name="destination_modified.xml",
                                   mime="text/xml")
    else:
        st.warning("Veuillez remplir tous les champs et uploader les fichiers.")
