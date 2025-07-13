# 235 dot py

Komentoriviltä käytettävä Ylen Teksti-TV-selain.

Tämä Python-skripti hakee Teksti-TV-sivun kuvat Ylen JSON-rajapinnasta ja näyttää ne terminaalissa [chafa](https://hpjansson.org/chafa/)-ohjelman avulla.

---

## Ominaisuudet

- Syötä suoraan Teksti-TV-sivu (esim. `100`, `101.2`)
- Navigointi näppäimillä:
  - `v` / `m`: edellinen / seuraava sivu
  - `b` / `n`: edellinen / seuraava alasivu
- Kuvan renderöinti terminaaliin (PNG → Unicode)

---

## Vaatimukset

- Python 3
- Python-kirjastot:
  - `requests`
- Järjestelmäohjelma:
  - `chafa` (asennus esim. `apt install chafa` tai `brew install chafa`)

Asenna Python-riippuvuudet:

```bash
pip install -r requirements.txt
```

---

## Käyttö

```bash
python3 235.py
```

Sen jälkeen:

- Näppäile sivunumero (esim. `101`)
- Käytä näppäimiä:
  - `v` = edellinen sivu
  - `m` = seuraava sivu
  - `b` = edellinen alasivu
  - `n` = seuraava alasivu
  - `q` = lopeta

---

## Lisenssi

MIT-lisenssi.
```

