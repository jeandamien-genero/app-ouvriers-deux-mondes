# app-ouvriers-deux-mondes

_Les Ouvriers des deux mondes_ are a collection of sociological surveys published under the aegis of Frédéric Le Play (†1882) and of the International Society of socio-economic practical studies. Those monographs were assembled in three sets composed of thirteen volumes from 1857 to 1913, with an addition of two booklets published in 1930. The ANR “Time Us” program undertook the transcription and structuration of the monographs following the TEI standard in order to make it possible to consult and study them digitally. 

Initial acquisition and structuration of the texts were automatically produced based on the digitization of _[Internet Archive](http://timeusage.paris.inria.fr/mediawiki/index.php/Aper%C3%A7u_des_%C3%A9tats#Les_Ouvriers_des_Mondes)_, using [the LSE-OD2M app](https://gitlab.inria.fr/almanach/time-us/LSE-OD2M) developed by Alix Chagué, Research and Development engineer of the [ALMAnaCH team at Inria](https://team.inria.fr/almanach/fr/). Scientific encoding was then carry out by Jean-Damien Généro, Studies Engineer at CNRS, first welcomed at the [Centre Maurice Halbwachs](https://www.cmh.ens.fr/) (CMH) and then assigned at the [Centre de recherches historiques](http://crh.ehess.fr/) (CRH) under the supervision of Anne Lhuissier, Research Director at INRAE (CMH) and Stéphane Baciocchi, Research Engineer from EHESS (CRH).
 
The goal of the app is to present the advance of the work on the monographs. It is currently developed by Jean-Daming Généro from XML-TEI files structured by Alix Chagué and himself.

Les _Ouvriers des deux mondes_ sont des recueils d'enquêtes sociologiques publiées sous l'égide de Frédéric Le Play (†1882) et de la Société internationale des études pratiques d'économie sociale. Ces monographies ont été rassemblées en trois séries de treize volumes de 1857 à 1913, deux fascicules supplémentaires paraissant en 1930. Le programme ANR « [Time Us](http://larhra.ish-lyon.cnrs.fr/anr-time-us) » a entrepris de transcrire et de structurer les monographies au standard TEI afin de permettre leur consultation électronique et leur étude.

L'acquisition et la structuration initiale des textes ont été réalisées automatiquement à partir des [numérisations d'Internet Archive](http://timeusage.paris.inria.fr/mediawiki/index.php/Aper%C3%A7u_des_%C3%A9tats#Les_Ouvriers_des_Mondes), à l'aide de l'application [LSE-OD2M](https://gitlab.inria.fr/almanach/time-us/LSE-OD2M) développée par Alix Chagué, ingénieure de recherche et de développement de l'[équipe ALMAnaCH d'Inria](https://team.inria.fr/almanach/fr/). L'encodage scientifique a ensuite été réalisé par Jean-Damien Généro, ingénieur d'études du CNRS accueilli au [Centre Maurice Halbwachs](https://www.cmh.ens.fr/) (CMH) puis affecté au [Centre de recherches historiques](http://crh.ehess.fr/) (CRH) sous la supervision d'Anne Lhuissier, directrice de recherche de l'INRAE (CMH) et de Stéphane Baciocchi, ingénieur de recherche de l'EHESS (CRH).

Cette application a pour but de présenter un état du travail sur les monographies. Elles est développée par Jean-Damien Généro, à partir de fichiers XML-TEI structurés par Alix Chagué et lui-même.

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
