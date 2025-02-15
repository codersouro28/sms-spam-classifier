mkdir -p ~/.streamlit/
mkdir -p ~/.nltk_data
python -c "import nltk; nltk.download('punkt', download_dir='~/.nltk_data')"
python -c "import nltk; nltk.download('stopwords', download_dir='~/.nltk_data')"
echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml