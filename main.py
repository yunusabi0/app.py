def set_bg():
    url = "https://images.pexels.com/photos/14433882/pexels-photo-14433882.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    response = requests.get(url)
    encoded = base64.b64encode(response.content).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .block-container {{
            background-color: rgba(255,255,255,0.85);
            padding: 2rem;
            border-radius: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
