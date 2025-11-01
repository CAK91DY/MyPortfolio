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