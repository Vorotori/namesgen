mkdir -p ~/.streamlit/

echo "[general]
email = \'${HEROKU_EMAIL_ADDRESS}\'
" > ~/.streamlit/credentials.toml

echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml