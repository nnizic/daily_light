from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import httpx
from bs4 import BeautifulSoup

app = FastAPI(title="Liturgija Dana API")

BASE_URL = "https://hilp.hr/liturgija-dana/"
DAY_MAP = {
    "monday": "ponedjeljak",
    "tuesday": "utorak",
    "wednesday": "srijeda",
    "thursday": "cetvrtak",
    "friday": "petak",
    "saturday": "subota",
    "sunday": "nedjelja",
}


class GospelResponse(BaseModel):
    date: str
    url: str
    reference: str
    title: str
    intro: str
    text: str


async def fetch_gospel_by_date(date_str: str):
    dt = datetime.strptime(date_str, "%Y-%m-%d").date()
    weekday_hr = DAY_MAP.get(dt.strftime("%A").lower(), dt.strftime("%A").lower())
    formatted = f"{weekday_hr}-{dt.day}-{dt.month}-{dt.year}"
    url = f"{BASE_URL}{formatted}/"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " "AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/115.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=20.0,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Stranica za taj datum nije pronađena.\n Status: {resp.status_code}")
        soup = BeautifulSoup(resp.text, "html.parser")

    blurbs = soup.find_all("div", class_="et_pb_blurb_content")
    reference = title = intro = text = ""

    for i, blurb in enumerate(blurbs):
        desc_tag = blurb.find("div", class_="et_pb_blurb_description")
        if not desc_tag:
            continue
        text_content = desc_tag.get_text(" ", strip=True)
        if any(x in text_content for x in ["Mt", "Mk", "Lk", "Iv"]):
            reference = text_content.strip()
            for j in range(i + 1, len(blurbs)):
                next_blurb = blurbs[j]
                p_tag = next_blurb.find("div", class_="et_pb_blurb_description")
                if not p_tag:
                    continue
                p = p_tag.find("p")
                if p and "Čitanje svetog Evanđelja" in p.get_text():
                    title_tag = next_blurb.find("h4", class_="et_pb_module_header")
                    title = title_tag.get_text(strip=True) if title_tag else ""
                    full_text = p.get_text("\n", strip=True)
                    lines = full_text.split("\n")
                    intro = lines[0].strip() if lines else ""
                    text = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
                    break
            break

    if not reference or not text:
        raise HTTPException(status_code=404, detail="Evanđelje nije pronađeno")

    return GospelResponse(
        date=dt.isoformat(),
        url=url,
        reference=reference,
        title=title,
        intro=intro,
        text=text,
    )


@app.get("/gospel/{date_str}", response_model=GospelResponse)
async def get_gospel(date_str: str):
    """
    Dohvati Evanđelje za zadani datum (format YYYY-MM-DD)
    """
    return await fetch_gospel_by_date(date_str)
