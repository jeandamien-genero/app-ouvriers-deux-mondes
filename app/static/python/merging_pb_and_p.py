#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author : Jean-Damien Généro
Affiliation : French National Center for Scientific Research (CNRS)
Assigned at the Centre de recherches historiques (CRH, UMR 8558)
Date : 2020-12-10
Update : 2021-06-15
Merging <pb> and <p> in OD2M files.
"""

import re

def merging_pb_and_p(fileslist) -> None:
  """
  Merging <pb> and <p> in OD2M files.
  :param fileslist: list of OD2M files.
  :type fileslist: list
  """
  for item in fileslist:
      with open(item, 'r', encoding='utf-8') as f:
          file = f.read()
          # mettre les <pb/> à l'intérieur d'un paragraphe scindé en deux <p> dont le premier <p> se termine par ¬
          file = re.sub(r'¬\n +<\/p>\n +(<pb facs=".*" n="[0-9]*" source=".+"\/>)\n +<p xml:id=".+">\n +([a-zéàê])',
                        '\\1\\2', file)
          # mettre les <pb/> à l'intérieur d'un paragraphe scindé en deux <p> dont le premier <p> se termine par [,;(]
          file = re.sub(r'([,;(])\n +<\/p>\n +(<pb facs=".*" n="[0-9]*" source=".+"\/>)\n +<p xml:id=".+">\n +([a-zéàê])',
                        '\\1 \\2 \\3', file)
          file = re.sub(r'\n +<\/p>\n +(<pb facs=".*" n="[0-9]*" source=".+"\/>)\n +<p xml:id=".+">\n +([a-zéêà])',
                        ' \\1 \\2', file)
          # mettre les <pb/> qui séparent deux paragraphes au début du deuxième.
          file = re.sub(r'([\dˉ\.!?,à]\n +<\/p>)\n +(<pb facs=".+" n="\d*" source=".+" ?\/>)(\n +<p xml:id=".+">\n + )('
                        r'[à,\.°ˉA-Z\-\déê])', '\\1\\3\\2 \\4', file)
          # mettre les <pb/> des budgets après les titres de sous-sous-section 14, 15 et 16.
          file = re.sub(r'(<pb.+>)(\n +)(<head type="sub_sub_section" xml:id="part_02_05_1[456]">\n +.+\n +<\/head>)',
                        '\\3\\2\\1', file)
          # mettre le <pb/> des Notes au début du premier praragraphe.
          file = re.sub(r'(<pb.+\/>)\n +(<head type="section" xml:id="part_03">\n +NOTES\n +</head>\n +<p.+\n +.+\n '
                        r'+<\/p>\n +<div.+\n +<div.+\n +<head.+\n +.+\n +<\/head>\n +<p.+>\n +)', '\\2\n       \\1', file)
          # mettre un <pb/> dans le premier paragraphe d'une sous-section ou d'une sous-sous-section
          file = re.sub(r'(<pb.+\/>)\n( +<head type="sub_section" xml:id=".+">\n +.+\n +<\/head>\n +<div.+>\n '
                        r'+<head.+\n +.+\n +<\/head>\n +<p.+\n +)', '\\2\\1', file)
          file = re.sub(r'(<pb.+\/>)\n +(<head type="sub_sub_section" xml:id="part_\d{2}_\d{2}_\d{2}">\n +.+\n '
                        r'+<\/head>\n +<p.+>\n +)', '\\2\\1', file)
          # mettre @rend dans //figure et @resp dans //figure/head (sauf §§ 14 à 16)
          file = re.sub(r'(<figure)( type=".+">\n .+<head)( type)', '\\1 rend="portrait"\\2 resp="added"\\3', file)
          # mettre @rend dans les //figure des budgets (§§ 14 à 16)
          file = re.sub(r'(<figure)( type="cptes_.+">)', '\\1 rend="portrait"\\2', file)
          # constituer les @facs des //figure/graphic
          file = re.sub(r'(<graphic facs="#facs_\d{3})_g_\d+"', '\\1"', file)
          result = file
      with open(item, 'w', encoding='utf-8') as f:
          f.write(result)
          print("{} --> done !".format(item))
