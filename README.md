# Daily Light

Za sada dodano:

## Liturgija Dana API

FastAPI web servis koji dohvaća **Evanđelje dana** s [HILP.hr](https://hilp.hr/liturgija-dana/) i vraća ga u JSON formatu.

---

## 🚀 Funkcionalnosti

- Dohvat Evanđelja i referenci za zadani datum.
- Vraća JSON s poljima:
  - `date` – datum
  - `url` – izvorni HILP URL
  - `reference` – biblijske reference
  - `title` – naslov Evanđelja
  - `intro` – uvodna linija
  - `text` – glavni tekst Evanđelja

---

## 🛠 Tehnologije

- Python 3.11
- FastAPI
- BeautifulSoup4
- httpx
- Pydantic
- Docker

---

## ⚡ Pokretanje lokalno

1. Clone repozitorij:
```bash
git clone https://github.com/username/liturgija-api.git
cd liturgija-api
