import streamlit as st
from logic import extract_card_block, replace_card_block

st.title("TTC Configuration Copier")

st.subheader(" Carte à copier (dans le fichier source)")
source_name = st.text_input("Source CARD Name")
source_type = st.text_input("Source CARD Type")
source_slot = st.text_input("Source CARD Slot")

st.subheader(" Carte à remplacer (dans le fichier destination)")
dest_name = st.text_input("Destination CARD Name")
dest_type = st.text_input("Destination CARD Type")
dest_slot = st.text_input("Destination CARD Slot")

uploaded_source = st.file_uploader("Upload Source XML", type="xml")
uploaded_dest = st.file_uploader("Upload Destination XML", type="xml")

if st.button("Copy the configuration"):
    if uploaded_source and uploaded_dest and source_name and source_type and source_slot and dest_name and dest_type and dest_slot:
        source_lines = uploaded_source.read().decode("utf-8").splitlines()
        dest_lines = uploaded_dest.read().decode("utf-8").splitlines()


        block = extract_card_block(source_lines, source_name, source_type, source_slot)
        if not block:
            st.error("Carte source non trouvée.")
        else:

            modified = replace_card_block(dest_lines, dest_name, dest_type, dest_slot, block)
            if not modified:
                st.error("Carte destination non trouvée.")
            else:
                st.success("Bloc copié avec succès.")
                st.download_button("Télécharger le fichier modifié",
                                   data="\n".join(modified),
                                   file_name="destination_modified.xml",
                                   mime="text/xml")
    else:
        st.warning("Veuillez remplir tous les champs et uploader les fichiers.")
