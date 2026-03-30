import streamlit as st
import random
import uuid  # L'outil pour générer nos jetons uniques

# 1. Initialisation de la mémoire
if 'spheres' not in st.session_state:
    st.session_state.spheres = {
        "Blague": ["Pourquoi les plongeurs plongent-ils en arrière ? Parce que sinon ils tombent dans le bateau."],
        "Amour et positivisme": ["Voici un gros câlin virtuel juste pour toi. 🤗"],
        "Gaffes inavouées": ["J'ai ruiné le mariage de mon frère en faisant trébucher le serveur avec le gâteau."]
    }

# NOUVEAU : Mémoire pour notre jeton d'accès
if 'mon_jeton' not in st.session_state:
    st.session_state.mon_jeton = None

# 2. En-tête de l'application
st.title("🤫 L'Application Éphémère")
st.write("Le réseau où tout finit par disparaître. Lisez un secret, ou confiez le vôtre (1$).")

# 3. Les onglets
onglet_lire, onglet_ecrire = st.tabs(["📖 Lire un secret", "✍️ Confier un secret (Payant)"])

# --- ONGLET 1 : LIRE (Inchangé) ---
with onglet_lire:
    st.header("Découvrir un secret (Gratuit)")
    categorie_choisie = st.selectbox("Choisissez une sphère :", list(st.session_state.spheres.keys()), key="choix_lecture")
    
    if st.button("Lire et détruire"):
        tiroir = st.session_state.spheres[categorie_choisie]
        if not tiroir:
            st.warning(f"📭 La sphère '{categorie_choisie}' est vide.")
        else:
            secret_choisi = random.choice(tiroir)
            tiroir.remove(secret_choisi)
            st.success(f"🔮 Voici ce que quelqu'un a laissé pour vous :\n\n**{secret_choisi}**")
            st.error("🔥 Ce message vient de s'autodétruire.")

# --- ONGLET 2 : ÉCRIRE (Nouveau système de paiement) ---
with onglet_ecrire:
    st.header("Libérez-vous d'un poids")
    
    # ÉTAPE A : LE PAIEMENT
    st.subheader("1. Obtenir un jeton d'accès")
    if st.session_state.mon_jeton is None:
        st.info("L'envoi d'un secret coûte 1$. C'est le prix de l'anonymat absolu !")
        if st.button("💳 Simuler un paiement de 1$"):
            # On génère un ticket unique et on le sauvegarde
            st.session_state.mon_jeton = str(uuid.uuid4())
            st.success(f"Paiement réussi ! Voici votre jeton unique : {st.session_state.mon_jeton}")
            st.rerun() # Force la page à se rafraîchir pour débloquer la suite
    else:
        st.success("✅ Paiement validé. Vous possédez un jeton d'accès actif.")

    st.divider()

    # ÉTAPE B : L'ENVOI DU SECRET (Bloqué si pas de jeton)
    st.subheader("2. Écrire votre secret")
    if st.session_state.mon_jeton is None:
        st.error("🔒 Veuillez effectuer le paiement ci-dessus pour débloquer cette section.")
    else:
        nouvelle_categorie = st.selectbox("Dans quelle sphère ?", list(st.session_state.spheres.keys()), key="choix_ecriture")
        nouveau_secret = st.text_area("Écrivez votre secret ici :")
        
        if st.button("Envoyer mon secret"):
            if nouveau_secret.strip() == "":
                st.warning("⚠️ Vous ne pouvez pas envoyer un secret vide !")
            else:
                # 1. On sauvegarde le secret
                st.session_state.spheres[nouvelle_categorie].append(nouveau_secret)
                
                # 2. ON DÉTRUIT LE JETON (Pour obliger à repayer la prochaine fois)
                st.session_state.mon_jeton = None 
                
                st.success("✅ Votre secret a été envoyé dans le cosmos !")
                st.rerun() # Rafraîchit la page pour rebloquer la section