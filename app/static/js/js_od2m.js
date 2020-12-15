/*
    Source : https://codepen.io/JoshuaLewis/pen/dGZzXG
    Modified by Jean-Damien Généro
    Date : 12 décembre 2020
*/

document.addEventListener('DOMContentLoaded', function() {
  TableOfContents();
}
);                        


function TableOfContents(container, output) {
var toc = "";
var level = 0;
var container = document.querySelector(container) || document.querySelector('#contents');
var output = output || '#toc';

container.innerHTML =
    container.innerHTML.replace(
        /<h([\d]) style=".+" id="(.+)">([^<]+)<\/h([\d])>/gi,
        function (str, openLevel, idLevel, titleText, closeLevel) {
            if (openLevel != closeLevel) {
                return str;
            }

            if (openLevel > level) {
                toc += (new Array(openLevel - level + 1)).join('<ul>');
            } else if (openLevel < level) {
                toc += (new Array(level - openLevel + 1)).join('</li></ul>');
            } else {
                toc += (new Array(level+ 1)).join('</li>');
            }

            level = parseInt(openLevel);

            var anchor = idLevel.replace(/ /g, "-");
            toc += '<li><a href="#' + anchor + '">' + titleText
                + '</a>';

            return '<h' + openLevel + '><a href="#' + anchor + '" id="' + anchor + '">'
                + titleText + '</a></h' + closeLevel + '>';
        }
    );

if (level) {
    toc += (new Array(level + 1)).join('</ul>');
}
document.querySelector(output).innerHTML += toc;
};