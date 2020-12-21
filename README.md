# app-ouvriers-deux-mondes

Les _Ouvriers des deux mondes_ sont des recueils d'enquêtes sociologiques publiées sous l'égide de Frédéric Le Play (†1882) et de la Société internationale des études pratiques d'économie sociale. Ces monographies ont été rassemblées en trois séries de treize volumes de 1857 à 1913, deux fascicules supplémentaires paraissant en 1930. Le programme ANR « [Time Us](http://larhra.ish-lyon.cnrs.fr/anr-time-us) » a entrepris de transcrire et de structurer les monographies au standard TEI afin de permettre leur consultation électronique et leur étude.

L'acquisition et la structuration initiale des textes ont été réalisées automatiquement à partir des [numérisations d'Internet Archive](http://timeusage.paris.inria.fr/mediawiki/index.php/Aper%C3%A7u_des_%C3%A9tats#Les_Ouvriers_des_Mondes), à l'aide de l'application [LSE-OD2M](https://gitlab.inria.fr/almanach/time-us/LSE-OD2M) développée par Alix Chagué, ingénieure de recherche et de développement de l'[équipe ALMAnaCH d'Inria](https://team.inria.fr/almanach/fr/). L'encodage scientifique a ensuite été réalisé par Jean-Damien Généro, ingénieur d'études du CNRS accueilli au [Centre Maurice Halbwachs](https://www.cmh.ens.fr/) (CMH) puis affecté au [Centre de recherches historiques](http://crh.ehess.fr/) (CRH) sous la supervision d'Anne Lhuissier, directrice de recherche de l'INRAE (CMH) et de Stéphane Baciocchi, ingénieur de recherche de l'EHESS (CRH).

Cette application a pour but de présenter un état du travail sur les monographies.

---

## Fonctionnalités

- Liste des monographies ;

- Visualisation du texte des monographies avec lien vers les images IIIF des pages.

---

## Installation

*Nota : commandes à exécuter dans le terminal (Linux ou macOS).*

  * Cloner le dossier : ```git clone https://github.com/jeandamien-genero/app-ouvriers-deux-mondes```
  
  * Installer l'environnement virtuel :
  
    * Vérifier que la version de Python est bien 3.x : ```python --version```;
    
    * Aller dans le dossier : ```cd app-ouvriers-deux-mondes```;
    
    * Installer l'environnement : ```python3 -m venv [nom de l'environnement]```.
  
  * Installer les packages et librairies :
  
    * Activer l'environnement : ```source [nom de l'environnement]/bin/activate```;
    
    * Installation : `pip install requirements.txt`
    
    * Sortir de l'environnement : ```deactivate``` ;
 
 ---

## Lancement
  
  * Activer l'environnement : ```source [nom de l'environnement]/bin/activate``` ;
    
  * Lancement : ```python run.py``` ;
    
  * Aller sur ```http://127.0.0.1:5000/``` ;
    
  * Désactivation : ```ctrl + c``` ;
    
  * Sortir de l'environnement : ```deactivate```.

---
