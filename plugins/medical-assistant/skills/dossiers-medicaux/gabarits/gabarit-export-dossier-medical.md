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
   2.1 Problèmes résolus
3. Médicaments
4. Allergies
5. Résultats d'analyses et d'examens
   5.1 Analyses de laboratoire (résumé)
   5.2 Examens (résumé)
   5.3 Bilans clés — points de vigilance
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

## 2.1 Problèmes résolus

<!-- Problèmes antérieurs résolus. Ne jamais supprimer : conserver avec une description COURTE de la résolution. Les éléments INVALIDÉS par une analyse/imagerie n'apparaissent PAS ici — ils sont retirés du dossier. -->

| #   | Problème résolu        | Résolution (courte)                 | Date de résolution |
| --- | ---------------------- | ----------------------------------- | ------------------ |
| 1   | [libellé du problème]  | [ex. résolu sous traitement X]      | [YYYY-MM]          |
| 2   |                        |                                     |                    |

**Tableau 5. Problèmes résolus**

---

## 3. Médicaments

<!-- Nom générique en premier, marque entre parenthèses. Une ligne par médicament. -->

| Médicament (générique / marque) | Dose     | Fréquence   | Voie          |
| ------------------------------- | -------- | ----------- | ------------- |
| [générique (marque)]            | [dose]   | [fréquence] | [voie]        |
|                                 |          |             |               |

**Tableau 6. Médicaments actifs**

---

## 4. Allergies

<!-- Une ligne par allergie. Préciser la substance et le type de réaction. -->

| Substance         | Réaction / Type              | Sévérité              |
| ----------------- | ---------------------------- | --------------------- |
| [substance]       | [type de réaction]           | [Majeure/Modérée/Mineure] |
|                   |                              |                       |

**Tableau 7. Allergies**

---

## 5. Résultats d'analyses et d'examens

<!--
Le dossier médical ne contient PAS les résultats détaillés : deux tableaux résumés (labo, examens)
puis un sous-paragraphe de points de vigilance.
Détail complet : `laboratoire/synthese-bilans.md` (skill `analyse-laboratoire`)
et `examens/synthese-examens.md` (skill `analyse-examens`).
-->

### 5.1 Analyses de laboratoire (résumé)

<!-- Résumé uniquement. Détail : laboratoire/synthese-bilans.md (skill analyse-laboratoire). -->

| Date         | Type d'analyse         | Prescripteur | Conclusion sommaire        |
| ------------ | ---------------------- | ------------ | -------------------------- |
| [YYYY-MM-DD] | [NFS / ionogramme / …] | [Dr …]       | [conclusion en une ligne]  |
|              |                        |              |                            |

**Tableau 8. Résumé des analyses de laboratoire**

> Détail complet : `laboratoire/synthese-bilans.md` (skill `analyse-laboratoire`).

### 5.2 Examens (résumé)

<!-- Résumé uniquement. Détail : examens/synthese-examens.md (skill analyse-examens). -->

| Date         | Type d'examen             | Prescripteur | Conclusion sommaire        |
| ------------ | ------------------------- | ------------ | -------------------------- |
| [YYYY-MM-DD] | [IRM cérébrale / ECG / …] | [Dr …]       | [conclusion en une ligne]  |
|              |                           |              |                            |

**Tableau 9. Résumé des examens**

> Détail complet : `examens/synthese-examens.md` (skill `analyse-examens`).

### 5.3 Bilans clés — points de vigilance

<!--
Ne reporter QUE les points de vigilance cliniques issus des analyses et des examens
(valeur critique, anomalie nouvelle/persistante, tendance à surveiller).
Aucune valeur exhaustive ici : le détail vit dans les synthèses dédiées ci-dessus (5.1 et 5.2).
Signaler les anomalies avec ↑ (au-dessus) / ↓ (en-dessous). Toujours indiquer les unités.
-->

| Point de vigilance     | Source (labo / examen) | Constat            | Date       |
| ---------------------- | ---------------------- | ------------------ | ---------- |
| [paramètre / anomalie] | [labo / examen]        | ↑ / ↓ / anomalie   | [date]     |
|                        |                        |                    |            |

**Tableau 10. Bilans clés — points de vigilance**

> 🚨 **Valeurs critiques** : reporter ici toute valeur critique nécessitant une revue urgente — `🚨 CRITIQUE : [valeur] nécessite une revue urgente`.

---

## 6. Chronologie

<!-- Événements clés dans l'ordre chronologique. -->

| Date       | Événement                                      |
| ---------- | ---------------------------------------------- |
| [date]     | [événement clé]                                |
|            |                                                |

**Tableau 11. Chronologie des événements**

---

## 7. Questions ouvertes

<!-- OBLIGATOIRE — aucun dossier n'est complet. Lacunes du dossier, points incertains, examens manquants. -->

| #   | Question ouverte / Lacune                      |
| --- | ---------------------------------------------- |
| 1   | [lacune / point incertain]                     |
| 2   |                                                |

**Tableau 12. Questions ouvertes**

---

<!--
PIED DE PAGE
Reproduire l'avertissement consultatif et la pagination sur chaque page lors du rendu (PDF/Word).
Avec pandoc, la pagination du PDF est gérée par le moteur LaTeX ; l'avertissement peut être placé en pied de page via un en-tête/pied personnalisé.
-->

---

*⚕️ Consultatif — validation médicale requise. — Source : `synthese.md` — Export : YYYY-MM-DD_hh-mm — Page X / Y*
