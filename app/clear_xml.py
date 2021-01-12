#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Date : 4 janvier 2021
"""

# import os
import re

titles = {"OBSERVATIONS PRÉLIMINAIRES DÉFINISSANT LA CONDITION DES DIVERS MEMBRES DE LA FAMILLE": "Observations "
                                                                                                  "préliminaires "
                                                                                                  "définissant la "
                                                                                                  "condition des "
                                                                                                  "divers membres de "
                                                                                                  "la famille",
          "OBSERVATIONS PRÉLIMINAIRES DÉFTNISSANT LA CONDITION DES DIVERS MEMBRES DE LA FAMILLE": "Observations "
                                                                                                  "préliminaires "
                                                                                                  "définissant la "
                                                                                                  "condition des "
                                                                                                  "divers membres de "
                                                                                                  "la famille",
          "ÉTAT DU SOL, DE L'INDUSTRIE ET DE LA POPULATION": "État du sol, de l'industrie et de la population",
          "ÉTAT CIVIL DE LA FAMILLE": "État civil de la famille",
          "RELIGION ET HABITUDES MORALES": "Religion et habitudes morales",
          "HYGIÈNE ET SERVICE DE SANTÉ": "Hygiène et service de santé",
          "RANG DE LA FAMILLE": "Rang de la famille", "PROPRIÉTÉS": "Propriétés", "SUBVENTIONS": "Subventions",
          "TRAVAUX ET INDUSTRIES": "Travaux et industries", "ALIMENTS ET REPAS": "Aliments et repas",
          "HABITATION, MOBILIER ET VÊTEMENTS": "Habitation, mobilier et vêtements", "RÉCRÉATIONS": "Récréations",
          "PHASES PRINCIPALES DE L'EXISTENCE": "Phases principales de l'existence",
          "MŒURS ET INSTITUTIONS ASSURANT LE BIEN-ÊTRE PHYSIQUE ET MORAL DE LA FAMILLE":
              "Mœurs et institutions assurant le bien-être physique et moral de la famille",
          "MOEURS ET INSTITUTIONS ASSURANT LE BIEN-ÊTRE PHYSIQUE ET MORAL DE LA FAMILLE":
              "Mœurs et institutions assurant le bien-être physique et moral de la famille",
          "BUDGET DES RECETTES DE L'ANNÉE": "Budget des recettes de l'année",
          "BUDGET DES DÉPENSES DE L'ANNÉE": "Budget des dépenses de l'année",
          "NOTES": "Notes", "NOTES DIVERSES": "Notes diverses", "Notes DIVERSES": "Notes diverses",
          "COMPTES ANNEXES AUX BUDGETS": "Comptes annexés aux budgets",
          "COMPTES ANNEXÉS AUX BUDGETS": "Comptes annexés aux budgets",
          "TRAVAUX DE LA FAMILLE": "Travaux de la famille"}

def clear_file(input_file):
  with open(input_file, 'r', encoding='utf-8') as xml_file:
    file = xml_file.read()
    # enlever le saut de ligne entre <p> et <pb>,
    # mettre un espace entre les <pb/> de début de ligne et le mot qui suit :
    file = re.sub(r'(<p.+>)\n  {3,}(<pb.+\/>)([\wéèà\-°\*ê\)\(§:;=,\\\[\].!])', '\\1\\2 \\3', file)
    # mettre un espace entre les <pb/> de début de ligne et le mot qui suit :
    file = re.sub(r'( {3,}<pb.+\/>)([\wéèà\-°\*ê\)\(§:;=,\\\[\].!])', '\\1 \\2', file)
    # rassembler <p> et <pb> quand il y a un saut de ligne entre les deux,
    # mettre un espace entre le <pb> et le mot qui suit :
    file = re.sub(r'(<p.+>)\n +(<pb.+\/>)\n +(\w)', '\\1\\2 \\3', file)
    # sortir les paranthèses des balises <ref> quand la balise n'est pas sur la même ligne :
    file = re.sub(r'(.)\n +(<ref target=".+" type=".+">)\n +(\()(.+)(\))\n +(<\/ref>)', '\\1 \\3\\2\\4\\6\\5', file)
    # enlever les sauts à la ligne entre la balise et son contenu :
    file = re.sub(r'(>)\n +([\wéèà\-°\*ê\)\(§:;=,\\\[\].!].*)\n +(<)', '\\1\\2\\3', file)
    # enlever les sauts à la ligne entre la balise <note> et son contenu :
    file = re.sub(r'(.)\n +(<note)', '\\1\\2', file)
    # mettre un espace entre les renvois <ref> et le caractère précédent :
    file = re.sub(r'([\.\wéè])(<ref)', '\\1 \\2', file)
    # mettre un espace entre les renvois <ref> et le caractère suivant :
    file = re.sub(r'(</ref>)([\wéè:;])', '\\1 \\2', file)
    # sortir les paranthèses des balises <ref> quand la balise est sur la même ligne :
    file = re.sub(r'(<ref target=".+" type=".+">)(\()(.+)(\))(<\/ref>)', '\\2\\1\\3\\5\\4', file)
    # enlever les numéros de paragraphes pour les titres de sous-sous-sections (§ \d.)
    # file = re.sub(r'§ ?\d{1,2}ᵉ?ʳ? ?\.? ?— ?', '', file)
    # enlever les numéros de paragraphes pour les titres de sous-sections (I.)
    # file = re.sub(r'I+V?\. ?([DMH])', '\\1', file)
    # AJOUTS APP PYTHON
    # enlever le saut de ligne entre </p> et la ligne précédente qui se termine par un point :
    file = re.sub(r'(\.)\n +(<\/p>)', '\\1\\2', file)
    # enlever le saut de ligne entre ) ou ] et un point ou une virgule (pas d'espace)
    file = re.sub(r'([\)\]])\n +([\.,])', '\\1\\2', file)
    # enlever le saut de ligne entre ) ou ] et une lettre (ajout d'un espace)
    file = re.sub(r'([\)\]])\n +([\wéèà])', '\\1 \\2', file)
    # enlever le saut de ligne entre ) ou ] et un ; ou un : (ajout d'un espace)
    file = re.sub(r'([\)\]])\n +([:;])', '\\1 \\2', file)
    # enlever le saut de ligne entre un > et une lettre
    file = re.sub(r'(>)\n +([\wéà])', '\\1\\2', file)
    # enlever le saut de ligne entre un "> et <pb
    file = re.sub(r'(">)\n +(<pb)', '\\1\\2', file)
    # enlever le saut de ligne entre une lettre ou un chiffre et <ref (ajout d'un espace)
    file = re.sub(r'([\wéèà])\n +(<ref)', '\\1 \\2', file)
    # enlever le saut de ligne entre une lettre ou un chiffre et </p
    file = re.sub(r'([\wéèà])\n +(.<\/p)', '\\1\\2', file)
    # enlever le saut de ligne entre "> et —
    file = re.sub(r'(">)\n +(—)', '\\1\\2', file)
    # enlever le saut de ligne entre — et </p>
    file = re.sub(r'(—)\n +(<\/p)', '\\1\\2', file)
    # mettre les titres en minuscules :
    for key in titles:
      file = file.replace(key, titles[key])
    # suppression des namespaces qui bloquent la transformation XSL
    file = re.sub('(<TEI xml:id=".+" xml:lang="fr") xmlns=".+" xmlns:xi=".+">', '\\1>', file)
    result = file
  with open(input_file, 'w') as wf:
    wf.write(result)
# print(result)
