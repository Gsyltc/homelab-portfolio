<!--
Gabarit d'exportation OBLIGATOIRE du dossier médical.
Ce gabarit s'applique UNIQUEMENT à l'export de `synthese.md` (dossier destiné aux professionnels de santé).
Il normalise la mise en forme du document exporté (PDF par défaut ; Word `.docx` uniquement sur demande explicite de l'humain).
Remplir chaque section à partir de `synthese.md` — ne jamais inventer de données ; laisser vide et signaler toute lacune.
Reprendre la structure « SYNTHÈSE PATIENT » de la skill : Démographie, Problèmes actifs, Médicaments, Allergies, Bilans clés, Chronologie, Questions ouvertes.
AVERTISSEMENT : contenu consultatif — la validation d'un médecin diplômé est requise.
-->

# Dossier médical — Synthèse patient (export)

<!--
PAGE DE GARDE
Renseigner les métadonnées d'export à partir de `synthese.md` et du contexte du dossier patient.
La source est TOUJOURS `synthese.md` (source de vérité, destinée aux professionnels de santé).
-->

## Page de garde

| Champ                       | Valeur                                             |
| --------------------------- | -------------------------------------------------- |
| **Patient**                 | [Nom du patient]                                   |
| **Identifiant dossier**     | [Identifiant interne / n° dossier]                 |
| **Date d'export**           | YYYY-MM-DD_hh-mm                                    |
| **Fichier source**          | `synthese.md`                                      |
| **Destinataire**            | Professionnel de santé                             |
| **Provenance / Auteur**     | [Auteur de la synthèse — ex. « Dr Martin, 2024-03-15 »] |
| **Version du dossier**      | [Version / révision de `synthese.md`]              |

**Tableau 1. Métadonnées de l'export**

> ⚕️ **AVERTISSEMENT — Consultatif.** Tous les résultats de ce document sont **consultatifs**. Les décisions cliniques exigent la validation d'un médecin diplômé. Aucun élément ne constitue un diagnostic définitif. L'incertitude est signalée explicitement.

---

## Sommaire

1. Démographie
2. Problèmes actifs
3. Médicaments
4. Allergies
5. Bilans clés
6. Chronologie
7. Questions ouvertes

---

## 1. Démographie

<!-- Âge, sexe, antécédents sociaux pertinents. Reprendre la ligne « Démographie » de la synthèse. -->

| Champ                       | Valeur                          |
| --------------------------- | ------------------------------- |
| **Âge**                     | [âge]                           |
| **Sexe**                    | [sexe]                          |
| **Antécédents sociaux**     | [antécédents sociaux pertinents]|

**Tableau 2. Démographie**

### Données morphologiques

<!--
Reporter les données morphologiques clés du patient. Le DÉTAIL (poids, IMC, IMG, IGC, masses, tours, évolution, objectif) est géré par la skill `suivi-morphologie` : reprendre ici les valeurs de sa synthèse, sans les recalculer. Signaler les points de vigilance (IMC/IGC critique, franchissement de seuil, tendance défavorable).
-->

| Paramètre                        | Valeur         | Signalement / Vigilance |
| -------------------------------- | -------------- | ----------------------- |
| **Taille**                       | [cm]           |                         |
| **Poids**                        | [kg]           |                         |
| **IMC**                          | [kg/m²]        | ↑ / ↓ / —               |
| **IMG (masse grasse)**           | [%]            |                         |
| **IGC (indice de graisse corporelle)** | [%]      | ↑ / ↓ / —               |
| **IGC cible**                    | [%]            |                         |
| **Kilos à perdre (estimation)**  | [kg]           |                         |

**Tableau 3. Données morphologiques**

> Détail complet (masses grasse/maigre, tours, évolution, méthode d'estimation) : voir la synthèse de la skill `suivi-morphologie`. Valeurs consultatives, à valider par le médecin.

---

## 2. Problèmes actifs

<!-- Liste numérotée. Indiquer le code CIM-10 quand disponible. Classer par gravité si connue. -->

| #   | Problème actif           | Code CIM-10 | Depuis      | Statut      |
| --- | ------------------------ | ----------- | ----------- | ----------- |
| 1   | [libellé du problème]    | [CIM-10]    | [date]      | Actif       |
| 2   |                          |             |             |             |

**Tableau 4. Problèmes actifs**

---

## 3. Médicaments

<!-- Nom générique en premier, marque entre parenthèses. Une ligne par médicament. -->

| Médicament (générique / marque) | Dose     | Fréquence   | Voie          |
| ------------------------------- | -------- | ----------- | ------------- |
| [générique (marque)]            | [dose]   | [fréquence] | [voie]        |
|                                 |          |             |               |

**Tableau 5. Médicaments actifs**

---

## 4. Allergies

<!-- Une ligne par allergie. Préciser la substance et le type de réaction. -->

| Substance         | Réaction / Type              | Sévérité              |
| ----------------- | ---------------------------- | --------------------- |
| [substance]       | [type de réaction]           | [Majeure/Modérée/Mineure] |
|                   |                              |                       |

**Tableau 6. Allergies**

---

## 5. Bilans clés

<!--
Ne reporter que les points de suivi notables (valeur critique, anomalie nouvelle/persistante, tendance à surveiller).
Signaler les anomalies avec ↑ (au-dessus) / ↓ (en-dessous) de la référence. Toujours indiquer les unités.
Pour le détail des analyses biologiques, renvoyer à la skill `analyse-laboratoire` ; pour la morphologie, à `suivi-morphologie`.
-->

| Bilan / Paramètre | Valeur     | Référence      | Signalement | Date       |
| ----------------- | ---------- | -------------- | ----------- | ---------- |
| [paramètre]       | [valeur+unité] | [plage réf.] | ↑ / ↓ / —   | [date]     |
|                   |            |                |             |            |

**Tableau 7. Bilans clés**

> 🚨 **Valeurs critiques** : reporter ici toute valeur critique nécessitant une revue urgente — `🚨 CRITIQUE : [valeur] nécessite une revue urgente`.

---

## 6. Chronologie

<!-- Événements clés dans l'ordre chronologique. -->

| Date       | Événement                                      |
| ---------- | ---------------------------------------------- |
| [date]     | [événement clé]                                |
|            |                                                |

**Tableau 8. Chronologie des événements**

---

## 7. Questions ouvertes

<!-- OBLIGATOIRE — aucun dossier n'est complet. Lacunes du dossier, points incertains, examens manquants. -->

| #   | Question ouverte / Lacune                      |
| --- | ---------------------------------------------- |
| 1   | [lacune / point incertain]                     |
| 2   |                                                |

**Tableau 9. Questions ouvertes**

---

<!--
PIED DE PAGE
Reproduire l'avertissement consultatif et la pagination sur chaque page lors du rendu (PDF/Word).
Avec pandoc, la pagination du PDF est gérée par le moteur LaTeX ; l'avertissement peut être placé en pied de page via un en-tête/pied personnalisé.
-->

---

*⚕️ Consultatif — validation médicale requise. — Source : `synthese.md` — Export : YYYY-MM-DD_hh-mm — Page X / Y*
