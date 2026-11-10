"""Tests des sensors Python du plugin `medical-assistant`.

Exécution : `python3 -m unittest discover -s plugins/medical-assistant/sensors/tests`
(Python ≥ 3.9, bibliothèque standard uniquement, aucun accès réseau).
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts" / "sensors"
sys.path.insert(0, str(SCRIPTS))

import fichiers_repas_conformes as conformes  # noqa: E402
import historique_repas_30j as historique  # noqa: E402
import repas_calendrier_agenda as agenda  # noqa: E402
from _communs import GAP, OK, UNAVAILABLE  # noqa: E402


def ecrire(dossier: Path, nom: str, contenu: str) -> None:
    (dossier / nom).write_text(contenu, encoding="utf-8")


def fixtures(dossier: Path, *, count: int = 1, dates: tuple[str, ...] = ("2026-11-12",)) -> None:
    lignes = "\n".join(
        f"| {jour} | Plat {i} | Companion de Moulinex | Companion XL — Recipebook FR, p. 4{i} |"
        for i, jour in enumerate(dates, start=1)
    )
    ecrire(dossier, "repas-retenus.md", f"""---
type: repas-retenus
updated: 2026-11-10
rolling_window_days: 30
count: {count}
oldest: {min(dates)}
newest: {max(dates)}
---

# Repas retenus

| Date       | Repas   | Appareil              | Emplacement de la recette           |
|------------|---------|-----------------------|-------------------------------------|
{lignes}
""")
    ecrire(dossier, "repas-exclus.md", """---
type: repas-exclus
updated: 2026-11-10
count: 1
---

# Repas exclus (refus définitifs — ne JAMAIS proposer)

- Blanquette de saumon
""")
    ecrire(dossier, "ingredients-refuses.md", """---
type: ingredients-refuses
updated: 2026-11-10
count: 1
---

# Ingrédients refusés (ne JAMAIS proposer un plat en contenant)

- Noix de coco
""")


def evenement(nom: str, debut: datetime, fin: datetime, description: str = "") -> dict:
    return {
        "summary": nom,
        "description": description,
        "start": {"dateTime": debut.isoformat()},
        "end": {"dateTime": fin.isoformat()},
    }


class TestCalendrierAgenda(unittest.TestCase):
    def setUp(self) -> None:
        self.repas = [{"date": date(2026, 11, 12), "repas": "Dahl de lentilles"}]
        self.events = [
            evenement("Dahl de lentilles", datetime(2026, 11, 12, 19, 0), datetime(2026, 11, 12, 20, 0),
                      "- 250g lentilles corail\n- 2 oignons\n- 200g riz basmati"),
            evenement("Dahl de lentilles", datetime(2026, 11, 13, 12, 0), datetime(2026, 11, 13, 13, 0)),
        ]

    def test_conforme(self) -> None:
        self.assertEqual(agenda.correler(self.repas, agenda.normaliser_evenements(self.events)), [])

    def test_repas_absent(self) -> None:
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events[1:]))
        self.assertTrue(any("aucun évènement repas 19h–20h" in e for e in ecarts))

    def test_ingredients_non_consignes(self) -> None:
        self.events[0]["description"] = ""
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events))
        self.assertTrue(any("ingrédients non consignés" in e for e in ecarts))

    def test_ingredients_hors_format(self) -> None:
        self.events[0]["description"] = "lentilles, oignons, riz"
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events))
        self.assertTrue(any("description sans puce" in e for e in ecarts))

    def test_creneau_lendemain_absent(self) -> None:
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events[:1]))
        self.assertTrue(any("aucun créneau du lendemain 2026-11-13 12h–13h" in e for e in ecarts))

    def test_creneau_lendemain_avec_description(self) -> None:
        self.events[1]["description"] = "- reste du plat"
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events))
        self.assertTrue(any("ne doit pas porter de description" in e for e in ecarts))

    def test_ancien_creneau_10h_rejete(self) -> None:
        self.events[1]["start"] = {"dateTime": datetime(2026, 11, 13, 10, 0).isoformat()}
        self.events[1]["end"] = {"dateTime": datetime(2026, 11, 13, 13, 0).isoformat()}
        ecarts = agenda.correler(self.repas, agenda.normaliser_evenements(self.events))
        self.assertTrue(any("12h–13h" in e for e in ecarts))


class TestHistorique30Jours(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dossier = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_historique_dans_la_fenetre(self) -> None:
        date_ok = (date(2026, 11, 10) - timedelta(days=20)).isoformat()
        fixtures(self.dossier, dates=(date_ok,))
        resultats = historique.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual([r.verdict for r in resultats], [OK])

    def test_repas_plus_ancien_que_30_jours(self) -> None:
        date_ko = (date(2026, 11, 10) - timedelta(days=31)).isoformat()
        fixtures(self.dossier, dates=(date_ko,))
        resultats = historique.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual([r.verdict for r in resultats], [GAP])
        self.assertIn("FAILED", resultats[0].message)

    def test_bloquant_code_retour_1(self) -> None:
        date_ko = (date(2026, 11, 10) - timedelta(days=31)).isoformat()
        fixtures(self.dossier, dates=(date_ko,))
        self.assertEqual(historique.main(["--data-dir", str(self.dossier), "--date", "2026-11-10"]), 1)

    def test_fichier_absent_indisponible(self) -> None:
        resultats = historique.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual([r.verdict for r in resultats], [UNAVAILABLE])
        self.assertEqual(historique.main(["--data-dir", str(self.dossier), "--date", "2026-11-10"]), 1)


class TestFichiersConformes(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dossier = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_trois_fichiers_conformes(self) -> None:
        fixtures(self.dossier)
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual([r.verdict for r in resultats], [OK, OK, OK])

    def test_count_incoherent(self) -> None:
        fixtures(self.dossier, count=3)
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual(resultats[0].verdict, GAP)
        self.assertTrue(any("count = 3" in e for e in resultats[0].details))

    def test_bornes_incoherentes(self) -> None:
        fixtures(self.dossier)
        chemin = self.dossier / "repas-retenus.md"
        chemin.write_text(chemin.read_text(encoding="utf-8").replace("oldest: 2026-11-12", "oldest: 2026-10-01"),
                          encoding="utf-8")
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual(resultats[0].verdict, GAP)
        self.assertTrue(any("oldest" in e for e in resultats[0].details))

    def test_en_tete_tableau_non_conforme(self) -> None:
        fixtures(self.dossier)
        chemin = self.dossier / "repas-retenus.md"
        chemin.write_text(chemin.read_text(encoding="utf-8").replace("| Appareil ", "| Appareils "),
                          encoding="utf-8")
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual(resultats[0].verdict, GAP)
        self.assertTrue(any("en-tête" in e for e in resultats[0].details))

    def test_updated_dans_le_futur(self) -> None:
        fixtures(self.dossier)
        resultats = conformes.controler(self.dossier, date(2026, 11, 1))
        self.assertEqual(resultats[0].verdict, GAP)
        self.assertTrue(any("postérieur" in e for e in resultats[0].details))

    def test_doublon_liste(self) -> None:
        fixtures(self.dossier)
        chemin = self.dossier / "ingredients-refuses.md"
        chemin.write_text(chemin.read_text(encoding="utf-8").replace("count: 1", "count: 2")
                          .replace("- Noix de coco", "- Noix de coco\n- noix de coco"), encoding="utf-8")
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual(resultats[2].verdict, GAP)
        self.assertTrue(any("doublon" in e for e in resultats[2].details))

    def test_fichier_absent_indisponible(self) -> None:
        fixtures(self.dossier)
        (self.dossier / "repas-exclus.md").unlink()
        resultats = conformes.controler(self.dossier, date(2026, 11, 10))
        self.assertEqual(resultats[1].verdict, UNAVAILABLE)

    def test_advisory_code_retour_0_sauf_strict(self) -> None:
        fixtures(self.dossier, count=9)
        argv = ["--data-dir", str(self.dossier), "--date", "2026-11-10"]
        self.assertEqual(conformes.main(argv), 0)
        self.assertEqual(conformes.main(argv + ["--strict"]), 1)


if __name__ == "__main__":
    unittest.main()
