# MyPortfolio

pybabel extract -F babel.cfg -k _ -o messages.pot .
pybabel init -i messages.pot -d translations -l fr
pybabel init -i messages.pot -d translations -l en

Ce que tu fais maintenant (pas à pas)
	1.	Ouvre les fichiers de traduction et traduis les msgstr

	•	Français : translations/fr/LC_MESSAGES/messages.po
	•	Anglais : translations/en/LC_MESSAGES/messages.po

	2.	Enregistre tes traductions, puis recompile :

pybabel compile -d translations


	3.	Teste le switch de langue

	•	Si tu as ajouté la route /set-lang/<lang> avec la session :
	•	http://localhost:5000/set-lang/en?next=/ → bascule en anglais
	•	http://localhost:5000/set-lang/fr?next=/ → bascule en français
	•	Ou clique sur tes liens FR/EN dans le header (si tu les as ajoutés dans base.html).


Rappels importants
	•	Quand tu ajoutes/modifies des textes dans tes templates Python/Jinja, refais le cycle :

pybabel extract -F babel.cfg -k _ -o messages.pot .
pybabel update -i messages.pot -d translations
# (édite les .po si de nouvelles chaînes sont apparues)
pybabel compile -d translations

2) Compile (ou recompile) les traductions

À faire à chaque fois que tu modifies les .po:

# depuis la racine du projet
pybabel extract -F babel.cfg -k _ -o messages.pot .
pybabel update -i messages.pot -d translations
# (édite translations/fr/.../messages.po et translations/en/.../messages.po si nécessaire)
pybabel compile -d translations

# comment installer PostGres
# Étape 2 — Installe PostgreSQ
brew install postgresql@16

# Étape 3 — Démarre PostgreSQL automatiquement
brew services start postgresql@16

# u peux vérifier que le service tourne avec 
brew services list

#  Étape 1 — Ajouter Postgres au PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Étape 2 — Vérifie que psql fonctionne
psql --version

# Étape 3 — Accède à PostgreSQL
psql postgres

#  Étape 4 — Crée ta base et ton utilisateur
CREATE DATABASE portfolio;
CREATE USER portfolio_user WITH PASSWORD 'portfolio_pwd';
GRANT ALL PRIVILEGES ON DATABASE portfolio TO portfolio_user;

# Lister toutes les bases de données 
\l

# Changer de base de données :
\c nom_de_la_base

# Quitter PostgreSQL :
\q

# consulter mes tables : 
\dt

# Verifier le contenu de la base de donnée depuis Render :
PGPASSWORD="nMJZHaVkKtzDYBo1dgdSeqTvOEzGlpa0" psql -h dpg-d43qhjmmcj7s73bcpd30-a.oregon-postgres.render.com -U datacraft_portfolio_db_user datacraft_portfolio_db

https://datacraft-portfolio.onrender.com/admin/login