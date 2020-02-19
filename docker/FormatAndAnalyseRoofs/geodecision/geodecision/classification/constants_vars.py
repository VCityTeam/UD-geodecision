#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 12:08:10 2019

@author: thomas
"""

# Variables dictionary source: 
## https://www.insee.fr/fr/statistiques/4176293?sommaire=4176305#dictionnaire
gridded_data_var = {
        "Id_carr1km" : "Identifiant Inspire du carreau de 1 km",
        "Ind" : "Nombre d’individus",
        "Men" : "Nombre de ménages",
        "Men_pauv" : "Nombre de ménages pauvres",
        "Men_1ind" : "Nombre de ménages d’un seul individu",
        "Men_5ind" : "Nombre de ménages de 5 individus ou plus",
        "Men_prop" : "Nombre de ménages propriétaires",
        "Men_fmp" : "Nombre de ménages monoparentaux",
        "Ind_snv" : "Somme des niveaux de vie winsorisés des individus",
        "Men_surf" : "Somme de la surface des logements du carreau",
        "Men_coll" : "Nombre de ménages en logements collectifs",
        "Men_mais" : "Nombre de ménages en maison",
        "Log_av45" : "Nombre de logements construits avant 1945",
        "Log_45_70" : "Nombre de logements construits entre 1945 et 1969",
        "Log_70_90" : "Nombre de logements construits entre 1970 et 1989",
        "Log_ap90" : "Nombre de logements construits depuis 1990",
        "Log_inc" : "Nombre de logements dont la date de construction est inconnue",
        "Log_soc" : "Nombre de logements sociaux",
        "Ind_0_3" : "Nombre d’individus de 0 à 3 ans",
        "Ind_4_5" : "Nombre d’individus de 4 à 5 ans",
        "Ind_6_10" : "Nombre d’individus de 6 à 10 ans",
        "Ind_11_17" : "Nombre d’individus de 11 à 17 ans",
        "Ind_18_24" : "Nombre d’individus de 18 à 24 ans",
        "Ind_25_39" : "Nombre d’individus de 25 à 39 ans",
        "Ind_40_54" : "Nombre d’individus de 40 à 54 ans",
        "Ind_55_64" : "Nombre d’individus de 55 à 64 ans",
        "Ind_65_79" : "Nombre d’individus de 65 à 79 ans",
        "Ind_80p" : "Nombre d’individus de 80 ans ou plus",
        "Ind_inc" : "Nombre d’individus dont l’âge est inconnu",
        "I_pauv" : "Nombre de carreaux de 200 m compris dans le carreau de 1 km qui ont été traités pour respecter la confidentialité sur le nombre de ménages pauvres",
        "I_est_1km" : "Vaut 1 si le carreau est imputé par une valeur approchée, 0 ou 2 sinon"
        }
