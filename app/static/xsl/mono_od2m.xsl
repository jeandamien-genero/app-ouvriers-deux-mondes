<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0" xmlns:xi="http://www.w3.org/2001/XInclude" exclude-result-prefixes="xs tei xi"
    version="1.0">
    <!--  xpath-default-namespace="http://www.tei-c.org/ns/1.0" -->
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    <!-- MISE EN FORME DU DOCUMENT HTML -->
    <xsl:template match="/">
        <html lang="fr">
            <xsl:element name="head">
                <xsl:element name="meta">
                    <xsl:attribute name="http-equiv">
                        <xsl:text>Content-Type</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="content">
                        <xsl:text>text/html; charset=UTF-8</xsl:text>
                    </xsl:attribute>
                </xsl:element>
                <xsl:element name="title">
                    <xsl:value-of select="//teiHeader//titleStmt/title"/>
                </xsl:element>
                <xsl:element name="meta">
                    <xsl:attribute name="name">
                        <xsl:text>author</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="content">
                        <xsl:value-of select="normalize-space(//respStmt[2]//name)"/>
                    </xsl:attribute>
                </xsl:element>
                <xsl:element name="meta">
                    <xsl:attribute name="description">
                        <xsl:text>author</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="content">
                        <xsl:value-of select="normalize-space(//sourceDesc/p)"/>
                    </xsl:attribute>
                </xsl:element>
                <!-- CSS pour les liens -->
                <xsl:element name="style">
                    <xsl:attribute name="type">
                        <xsl:text>text/css</xsl:text>
                    </xsl:attribute>
                    <xsl:text>a:link, a:visited {
                                text-decoration: none;
                                color: inherit;
                               }
                               a:hover, a:active {
                                text-decoration: none;
                                color: #B1B0B0;
                    }</xsl:text>
                </xsl:element>
            </xsl:element>
            <body>
                <!-- monographie -->
                <xsl:apply-templates select="//text"/>
                <div style="font-size: 10pt; margin: 70; text-align: justify;">
                    <h1>Notes</h1>
                    <xsl:apply-templates select="//text//note[@type='bp']/p"/>
                </div>
                <!-- JS -->
                <script type="text/javascript" src="../static/js/js_od2m.js"></script>
            </body>
        </html>
    </xsl:template>
    <!-- STRUCTURE LOGIQUE >> DIVISONS -->
    <xsl:template match="//text//div">
        <xsl:choose>
            <!-- div globale de la monographie -->
            <xsl:when test="./@type='chapter'">
                <div type="chapter">
                    <xsl:attribute name="id">
                        <!-- <xsl:value-of select="replace(//div[@type='chapter']/@ana,'#','')"/> -->
                        <xsl:text>contents</xsl:text>
                    </xsl:attribute>
                    <xsl:attribute name="style">
                        <xsl:text>margin: 70; text-align: justify;</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </div>
            </xsl:when>
            <!-- div des grandes sections -->
            <xsl:when test="./@type='section'">
                <!-- mise en forme s'il s'agit du titre de la monographie -->
                <xsl:if test="./@n='001'">
                    <div type="section" style="font-weight: bold; text-align: center; margin-bottom: 60; padding-top: 25;">
                        <xsl:apply-templates/>
                    </div>
                    <hr/>
                    <div id="toc">
                        <h3>Sommaire</h3>
                    </div>
                    <hr/>
                </xsl:if>
                <!-- pas de mise en forme pour toutes les autres grandes sections -->
                <xsl:if test="./@n[not(contains(., '001'))]">
                    <div type="section">
                        <xsl:apply-templates/>
                    </div>
                </xsl:if>
            </xsl:when>
            <!-- div des sous sections -->
            <xsl:when test="./@type='sub_section'">
                <div type="sub_section">
                    <xsl:apply-templates/>
                </div>
            </xsl:when>
            <!-- div des sous-sous-sections -->
            <xsl:when test="./@type='sub_sub_section'">
                <div type="sub_sub_section">
                    <xsl:apply-templates/>
                </div>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <!-- STRUCTURE LOGIQUE >> TITRES -->
    <xsl:template match="//text//head">
        <xsl:choose>
            <!-- sections -->
            <xsl:when test="./@type='section'">
                <h1 style="font-size: x-large; align: center;">
                    <xsl:attribute name="id">
                        <xsl:value-of select="./@xml:id"/>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </h1>
            </xsl:when>
            <!-- sous-sections -->
            <xsl:when test="./@type='sub_section'">
                <h2 style="font-size: large;">
                    <xsl:attribute name="id">
                        <xsl:value-of select="./@xml:id"/>
                    </xsl:attribute>
                    <xsl:attribute name="style">
                        <xsl:text>margin: 30 auto 45 auto</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </h2>
            </xsl:when>
            <!-- sous-sous-sections -->
            <xsl:when test="./@type='sub_sub_section'">
                <h3 style="font-size: medium;">
                    <xsl:attribute name="id">
                        <xsl:value-of select="./@xml:id"/>
                    </xsl:attribute>
                    <xsl:attribute name="style">
                        <xsl:text>margin: 30 auto 30 auto</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates/>
                </h3>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <!-- PARAGRAPHES -->
    <xsl:template match="//text//div//p">
        <xsl:element name="p">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="//text//div//p/text()">
        <xsl:value-of select="translate(.,'¬','')"/>
    </xsl:template>
    <!-- RENVOIS -->
    <xsl:template match="//text//ref">
        <xsl:choose>
            <!-- Renvois internes à la monographie : création d'un lien -->
            <xsl:when test="./@type='renvoi_int_mono'">
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:value-of select="./@target"/>
                    </xsl:attribute>
                    <xsl:value-of select="."/>
                </xsl:element>
            </xsl:when>
            <!-- Renvois externes : pas de lien -->
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="//pb">
        <xsl:variable name="url_page">
            <xsl:value-of select="translate(./@facs, '#', '')"/>
        </xsl:variable>
        <xsl:element name="a">
            <xsl:attribute name="href">
                <xsl:value-of select="./ancestor::TEI/facsimile[@xml:id=$url_page]/graphic/@url"/>
            </xsl:attribute>
            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>
            <xsl:text>[</xsl:text><xsl:value-of select="./@n"/><xsl:text>]</xsl:text>
        </xsl:element>
    </xsl:template>
    <!-- IMAGES DES FIGURES -->
    <xsl:template match="//figure[@type[not(contains(., 'depenses')) and not(contains(., 'recettes')) and not(contains(., 'cptes_annexes'))]]">
        <xsl:variable name="url_fig">
            <xsl:value-of select="translate(./graphic/@facs, '#', '')"/>
        </xsl:variable>
        <xsl:element name="figure">
            <xsl:element name="img">
                <xsl:attribute name="src">
                    <xsl:value-of select="./ancestor::TEI/facsimile[@xml:id=$url_fig]/graphic/@url"/>
                </xsl:attribute>
                <xsl:attribute name="width">
                    <xsl:text>30%</xsl:text>
                </xsl:attribute>
                <xsl:attribute name="alt">
                    <xsl:value-of select="normalize-space(./head)"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:element name="figcaption">
                <xsl:value-of select="normalize-space(./head)"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- NOTES -->
    <!-- appels de note -->
    <xsl:template match="//note[@type='bp']">
        <xsl:element name="sup">
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:text>#</xsl:text>
                    <xsl:number count="//text//note[@type='bp']" level="any" format="1"/>
                </xsl:attribute>
                <xsl:number count="//text//note[@type='bp']" level="any" format="1"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- notes -->
    <xsl:template match="//note[@type='bp']/p[1]">
        <xsl:element name="p">
            <xsl:attribute name="id">
                <xsl:number count="//text//note[@type='bp']" level="any" format="1"/>
            </xsl:attribute>
            <xsl:number count="//text//note[@type='bp']" level="any" format="1"/>
            <xsl:text>. </xsl:text>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="//note[@type='bp']/p[position()&gt;1]">
        <xsl:element name="p">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>