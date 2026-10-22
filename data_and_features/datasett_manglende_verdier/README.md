# Datasett til oppgaven: Håndtering av manglende verdier

Denne mappen inneholder tre datasett med manglende verdier. Dataene er simulert (laget for denne oppgaven), men er laget for å ligne på ekte data.

Alle filene er CSV med komma som skilletegn og punktum som desimaltegn. En manglende verdi er som regel en tom celle. Sjekk også at verdiene som finnes, er rimelige.

Eksempel på innlesing:

```python
import pandas as pd
df = pd.read_csv("vaerdata.csv")
print(df.isna().sum())
```

---

## 1. `vaerdata.csv`: daglige målinger fra en værstasjon

731 rader, én rad per dag fra 1. januar 2024 til 31. desember 2025.

| Kolonne | Beskrivelse | Enhet |
|---|---|---|
| `dato` | Dato for målingen | ÅÅÅÅ-MM-DD |
| `temperatur_c` | Gjennomsnittstemperatur for døgnet | °C |
| `lufttrykk_hpa` | Gjennomsnittlig lufttrykk | hPa |
| `vind_ms` | Gjennomsnittlig vindstyrke | m/s |
| `nedbor_mm` | Total nedbør i døgnet | mm |

---

## 2. `studentdata.csv`: spørreundersøkelse blant studenter

400 rader, én rad per student. Noen tall kommer fra studentenes egne svar, andre fra registrerte data.

| Kolonne | Beskrivelse | Enhet |
|---|---|---|
| `student_id` | Løpenummer | |
| `alder` | Alder | år |
| `studieprogram` | Dataingeniør, Elektroingeniør, Bygg eller Økonomi | kategori |
| `bor_paa_campus` | Om studenten bor på campus | ja / nei |
| `timer_jobb_per_uke` | Timer i deltidsjobb per uke (eget svar) | timer |
| `timer_studier_per_uke` | Timer brukt på studier per uke (eget svar) | timer |
| `oppmote_prosent` | Registrert oppmøte på undervisning | % |
| `studiepoeng_siste_aar` | Studiepoeng bestått siste studieår | studiepoeng |

---

## 3. `boligdata.csv`: boliger lagt ut for salg

500 rader, én rad per bolig.

| Kolonne | Beskrivelse | Enhet |
|---|---|---|
| `bolig_id` | Løpenummer | |
| `areal_m2` | Bruksareal | m² |
| `antall_rom` | Antall rom (utenom kjøkken og bad) | |
| `byggeaar` | Byggeår | år |
| `avstand_sentrum_km` | Avstand til sentrum | km |
| `garasje` | Om boligen har garasje | ja / nei |
| `energimerke` | Energikarakter fra A (best) til G (dårligst) | kategori |
| `pris_kr` | Prisantydning | kr |
