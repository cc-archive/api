<?xml version="1.0" encoding="utf8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:variable name="license-locale">
    <xsl:value-of select="/answers/locale" />
  </xsl:variable>

  <xsl:template name="attribution">
    <xsl:choose>
       <!-- generated locale choice lines -->
       
         <xsl:when test="$license-locale='en' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='af' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='ca' ">Reconeixement</xsl:when>
       
         <xsl:when test="$license-locale='it' ">Attribuzione</xsl:when>
       
         <xsl:when test="$license-locale='eu' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='gl' ">Recoñecemento</xsl:when>
       
         <xsl:when test="$license-locale='es' ">Reconocimiento</xsl:when>
       
         <xsl:when test="$license-locale='nl' ">Naamsvermelding</xsl:when>
       
         <xsl:when test="$license-locale='pt' ">Atribuição</xsl:when>
       
         <xsl:when test="$license-locale='es_CL' ">Atribución</xsl:when>
       
         <xsl:when test="$license-locale='de_AT' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='es_AR' ">Atribución</xsl:when>
       
         <xsl:when test="$license-locale='zh_TW' ">姓名標示</xsl:when>
       
         <xsl:when test="$license-locale='foo' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='en_GB' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='en_CA' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='fr' ">Paternité</xsl:when>
       
         <xsl:when test="$license-locale='bg' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='hr' ">Imenovanje</xsl:when>
       
         <xsl:when test="$license-locale='de' ">Namensnennung</xsl:when>
       
         <xsl:when test="$license-locale='hu' ">Nevezd meg!</xsl:when>
       
         <xsl:when test="$license-locale='fi' ">Nimi mainittava</xsl:when>
       
         <xsl:when test="$license-locale='ja' ">帰属</xsl:when>
       
         <xsl:when test="$license-locale='fr_CA' ">Paternité</xsl:when>
       
         <xsl:when test="$license-locale='he' ">ייחוס</xsl:when>
       
         <xsl:when test="$license-locale='ko' ">저작자표시</xsl:when>
       
         <xsl:when test="$license-locale='sv' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='st' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='kr' ">저작자표시</xsl:when>
       
         <xsl:when test="$license-locale='pl' ">Uznanie autorstwa</xsl:when>
       
         <xsl:when test="$license-locale='sl' ">Priznanje avtorstva</xsl:when>
       
         <xsl:when test="$license-locale='ua' ">Attribution</xsl:when>
       
         <xsl:when test="$license-locale='se' ">Erkännande</xsl:when>
       
       <xsl:otherwise>Attribution</xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="derivatives">
    <xsl:param name="derivs" />

    <xsl:variable name="prettystring">

      <xsl:choose>
        <xsl:when test="$derivs='n'">
          <xsl:choose>
            <!-- generated locale choice lines -->
            
              <xsl:when test="$license-locale='en' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='af' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='ca' ">SenseObraDerivada</xsl:when>
            
              <xsl:when test="$license-locale='it' ">NoOpereDerivate</xsl:when>
            
              <xsl:when test="$license-locale='eu' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='gl' ">SenObraDerivada</xsl:when>
            
              <xsl:when test="$license-locale='es' ">SinObraDerivada</xsl:when>
            
              <xsl:when test="$license-locale='nl' ">GeenAfgeleideWerken</xsl:when>
            
              <xsl:when test="$license-locale='pt' ">Não a obras derivadas</xsl:when>
            
              <xsl:when test="$license-locale='es_CL' ">SinDerivadas</xsl:when>
            
              <xsl:when test="$license-locale='de_AT' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='es_AR' ">SinDerivadas</xsl:when>
            
              <xsl:when test="$license-locale='zh_TW' ">禁止改作</xsl:when>
            
              <xsl:when test="$license-locale='foo' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='en_GB' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='en_CA' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='fr' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='bg' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='hr' ">Bez prerada</xsl:when>
            
              <xsl:when test="$license-locale='de' ">KeineBearbeitung</xsl:when>
            
              <xsl:when test="$license-locale='hu' ">Ne változtasd!</xsl:when>
            
              <xsl:when test="$license-locale='fi' ">Ei jälkiperäisiä teoksia</xsl:when>
            
              <xsl:when test="$license-locale='ja' ">派生禁止</xsl:when>
            
              <xsl:when test="$license-locale='fr_CA' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='he' ">איסור יצירות נגזרות</xsl:when>
            
              <xsl:when test="$license-locale='ko' ">변경금지</xsl:when>
            
              <xsl:when test="$license-locale='sv' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='st' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='kr' ">변경금지</xsl:when>
            
              <xsl:when test="$license-locale='pl' ">Bez utworów zależnych</xsl:when>
            
              <xsl:when test="$license-locale='sl' ">Brez predelav</xsl:when>
            
              <xsl:when test="$license-locale='ua' ">NoDerivs</xsl:when>
            
              <xsl:when test="$license-locale='se' ">IngaBearbetningar</xsl:when>
            

            <xsl:otherwise>NoDerivs</xsl:otherwise>
          </xsl:choose>
        </xsl:when>
 
        <xsl:when test="$derivs='sa'">
          <xsl:choose>
            <!-- generated locale choice lines -->
            
              <xsl:when test="$license-locale='en' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='af' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='ca' ">CompartirIgual</xsl:when>
            
              <xsl:when test="$license-locale='it' ">StessaLicenza</xsl:when>
            
              <xsl:when test="$license-locale='eu' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='gl' ">CompartirIgual</xsl:when>
            
              <xsl:when test="$license-locale='es' ">CompartirIgual</xsl:when>
            
              <xsl:when test="$license-locale='nl' ">GelijkDelen</xsl:when>
            
              <xsl:when test="$license-locale='pt' ">Compartilhamento pela mesma licença</xsl:when>
            
              <xsl:when test="$license-locale='es_CL' ">Licenciar Igual</xsl:when>
            
              <xsl:when test="$license-locale='de_AT' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='es_AR' ">CompartirDerivadasIgual</xsl:when>
            
              <xsl:when test="$license-locale='zh_TW' ">相同方式分享</xsl:when>
            
              <xsl:when test="$license-locale='foo' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='en_GB' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='en_CA' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='fr' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='bg' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='hr' ">Dijeli pod istim uvjetima</xsl:when>
            
              <xsl:when test="$license-locale='de' ">Weitergabe unter gleichen Bedingungen</xsl:when>
            
              <xsl:when test="$license-locale='hu' ">Így add tovább!</xsl:when>
            
              <xsl:when test="$license-locale='fi' ">Sama lisenssi</xsl:when>
            
              <xsl:when test="$license-locale='ja' ">同一条件許諾</xsl:when>
            
              <xsl:when test="$license-locale='fr_CA' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='he' ">שיתוף זהה</xsl:when>
            
              <xsl:when test="$license-locale='ko' ">동일조건변경허락</xsl:when>
            
              <xsl:when test="$license-locale='sv' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='st' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='kr' ">동일조건변경허락</xsl:when>
            
              <xsl:when test="$license-locale='pl' ">Na tych samych warunkach</xsl:when>
            
              <xsl:when test="$license-locale='sl' ">Deljenje pod enakimi pogoji</xsl:when>
            
              <xsl:when test="$license-locale='ua' ">ShareAlike</xsl:when>
            
              <xsl:when test="$license-locale='se' ">DelaLika</xsl:when>
            

            <xsl:otherwise>ShareAlike</xsl:otherwise>
          </xsl:choose>
        </xsl:when>

      </xsl:choose>

    </xsl:variable>

    <xsl:if test="string-length($prettystring) &gt; 0">
      <xsl:value-of select="concat('-', $prettystring)" />
    </xsl:if>

  </xsl:template>

  <xsl:template name="noncommercial">
    <xsl:param name="commercial" />

    <xsl:variable name="prettystring">
      <xsl:if test="./commercial='n'">
        <xsl:choose>
          <!-- generated locale choice lines -->
          
            <xsl:when test="$license-locale='en' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='af' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='ca' ">NoComercial</xsl:when>
          
            <xsl:when test="$license-locale='it' ">NonCommerciale</xsl:when>
          
            <xsl:when test="$license-locale='eu' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='gl' ">NonComercial</xsl:when>
          
            <xsl:when test="$license-locale='es' ">NoComercial</xsl:when>
          
            <xsl:when test="$license-locale='nl' ">NietCommercieel</xsl:when>
          
            <xsl:when test="$license-locale='pt' ">Uso Não-Comercial</xsl:when>
          
            <xsl:when test="$license-locale='es_CL' ">NoComercial</xsl:when>
          
            <xsl:when test="$license-locale='de_AT' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='es_AR' ">NoComercial</xsl:when>
          
            <xsl:when test="$license-locale='zh_TW' ">非商業性</xsl:when>
          
            <xsl:when test="$license-locale='foo' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='en_GB' ">Non-Commercial</xsl:when>
          
            <xsl:when test="$license-locale='en_CA' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='fr' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='bg' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='hr' ">Nekomercijalno</xsl:when>
          
            <xsl:when test="$license-locale='de' ">NichtKommerziell</xsl:when>
          
            <xsl:when test="$license-locale='hu' ">Ne add el!</xsl:when>
          
            <xsl:when test="$license-locale='fi' ">Ei kaupalliseen käyttöön</xsl:when>
          
            <xsl:when test="$license-locale='ja' ">非営利</xsl:when>
          
            <xsl:when test="$license-locale='fr_CA' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='he' ">שימוש לא מסחרי</xsl:when>
          
            <xsl:when test="$license-locale='ko' ">비영리</xsl:when>
          
            <xsl:when test="$license-locale='sv' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='st' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='kr' ">비영리</xsl:when>
          
            <xsl:when test="$license-locale='pl' ">Użycie niekomercyjne</xsl:when>
          
            <xsl:when test="$license-locale='sl' ">Nekomercialno</xsl:when>
          
            <xsl:when test="$license-locale='ua' ">NonCommercial</xsl:when>
          
            <xsl:when test="$license-locale='se' ">IckeKommersiell</xsl:when>
          
          <xsl:otherwise>NonCommercial</xsl:otherwise>
        </xsl:choose>
      </xsl:if>
    </xsl:variable>

    <xsl:if test="string-length($prettystring) &gt; 0">
      <xsl:value-of select="concat('-', $prettystring)" />
    </xsl:if>

  </xsl:template>

  <xsl:template name="thiswork">
     <xsl:param name="license_name" />
     <xsl:param name="license_url" />
     <xsl:variable name="work_type">
       <xsl:choose>
          
          <xsl:when test="$license-locale='en' ">work</xsl:when>
          
          <xsl:when test="$license-locale='af' ">work</xsl:when>
          
          <xsl:when test="$license-locale='ca' ">obra</xsl:when>
          
          <xsl:when test="$license-locale='it' ">opera</xsl:when>
          
          <xsl:when test="$license-locale='eu' ">work</xsl:when>
          
          <xsl:when test="$license-locale='gl' ">obra</xsl:when>
          
          <xsl:when test="$license-locale='es' ">obra</xsl:when>
          
          <xsl:when test="$license-locale='nl' ">werk</xsl:when>
          
          <xsl:when test="$license-locale='pt' ">obra</xsl:when>
          
          <xsl:when test="$license-locale='es_CL' ">work</xsl:when>
          
          <xsl:when test="$license-locale='de_AT' ">work</xsl:when>
          
          <xsl:when test="$license-locale='es_AR' ">obra</xsl:when>
          
          <xsl:when test="$license-locale='zh_TW' ">著作</xsl:when>
          
          <xsl:when test="$license-locale='foo' ">work</xsl:when>
          
          <xsl:when test="$license-locale='en_GB' ">work</xsl:when>
          
          <xsl:when test="$license-locale='en_CA' ">work</xsl:when>
          
          <xsl:when test="$license-locale='fr' ">création</xsl:when>
          
          <xsl:when test="$license-locale='bg' ">work</xsl:when>
          
          <xsl:when test="$license-locale='hr' ">djelo</xsl:when>
          
          <xsl:when test="$license-locale='de' ">Inhalt</xsl:when>
          
          <xsl:when test="$license-locale='hu' ">Mű</xsl:when>
          
          <xsl:when test="$license-locale='fi' ">teos</xsl:when>
          
          <xsl:when test="$license-locale='ja' ">作品</xsl:when>
          
          <xsl:when test="$license-locale='fr_CA' ">création</xsl:when>
          
          <xsl:when test="$license-locale='he' ">יצירה</xsl:when>
          
          <xsl:when test="$license-locale='ko' ">저작물</xsl:when>
          
          <xsl:when test="$license-locale='sv' ">work</xsl:when>
          
          <xsl:when test="$license-locale='st' ">work</xsl:when>
          
          <xsl:when test="$license-locale='kr' ">저작물</xsl:when>
          
          <xsl:when test="$license-locale='pl' ">utwór</xsl:when>
          
          <xsl:when test="$license-locale='sl' ">delo</xsl:when>
          
          <xsl:when test="$license-locale='ua' ">work</xsl:when>
          
          <xsl:when test="$license-locale='se' ">verk</xsl:when>
          

          <xsl:otherwise>work</xsl:otherwise>
       </xsl:choose>
     </xsl:variable>

      <xsl:choose>
       <!-- generated locale choice lines -->
       

            <xsl:when test="$license-locale='en' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='af' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='ca' ">Aquesta <xsl:value-of select="$work_type"/> està subjecta a una <a rel="license" href="{$license_url}">Llicència de Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='it' ">Questo/a <xsl:value-of select="$work_type"/> è pubblicato sotto una <a rel="license" href="{$license_url}">Licenza Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='eu' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='gl' ">Esta <xsl:value-of select="$work_type"/> está baixo unha licenza <a rel="license" href="{$license_url}"><xsl:value-of select="$license_name"/> de Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='es' ">Esta <xsl:value-of select="$work_type"/> está bajo una <a rel="license" href="{$license_url}">licencia de Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='nl' ">Op dit <xsl:value-of select="$work_type"/> is een <a rel="license" href="{$license_url}">Creative Commons Licentie</a> van toepassing.</xsl:when>

       

            <xsl:when test="$license-locale='pt' ">Esta <xsl:value-of select="$work_type"/> está licenciada sob uma <a rel="license" href="{$license_url}">Licença Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='es_CL' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='de_AT' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='es_AR' ">Esta <xsl:value-of select="$work_type"/> está licenciada bajo una <a rel="license" href="{$license_url}">Licencia Creative Commons <xsl:value-of select="$license_name"/> </a>.</xsl:when>

       

            <xsl:when test="$license-locale='zh_TW' ">本 <xsl:value-of select="$work_type"/> 係採用 <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> 授權條款</a>授權.</xsl:when>

       

            <xsl:when test="$license-locale='foo' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='en_GB' ">This <xsl:value-of select="$work_type"/> is licenced under a <a rel="license" href="{$license_url}">Creative Commons Licence</a>.</xsl:when>

       

            <xsl:when test="$license-locale='en_CA' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons Licence</a>.</xsl:when>

       

            <xsl:when test="$license-locale='fr' ">Ce/tte <xsl:value-of select="$work_type"/> est mis/e à disposition sous un <a rel="license" href="{$license_url}">contrat Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='bg' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='hr' ">Ovo <xsl:value-of select="$work_type"/> je ustupljeno pod <a rel="license" href="{$license_url}">Creative Commons licencom <xsl:value-of select="$license_name"/></a>.</xsl:when>

       

            <xsl:when test="$license-locale='de' ">Dieser <xsl:value-of select="$work_type"/> ist unter einer <a rel="license" href="{$license_url}">Creative Commons-Lizenz</a> lizenziert.</xsl:when>

       

            <xsl:when test="$license-locale='hu' ">Ezt a <xsl:value-of select="$work_type"/> művet <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> Licenc alatt tették közzé</a>.</xsl:when>

       

            <xsl:when test="$license-locale='fi' ">Tämän <xsl:value-of select="$work_type"/>teoksen käyttöoikeutta koskee <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/>-lisenssi</a>.</xsl:when>

       

            <xsl:when test="$license-locale='ja' ">この<xsl:value-of select="$work_type"/>は、<a rel="license" href="{$license_url}">クリエイティブ・コモンズ・ライセンス</a>の下でライセンスされています。</xsl:when>

       

            <xsl:when test="$license-locale='fr_CA' ">Cette <xsl:value-of select="$work_type"/> est mise à disposition sous un <a rel="license" href="{$license_url}">contrat Creative Commons</a>.</xsl:when>

       

            <xsl:when test="$license-locale='he' "><span dir="rtl"><xsl:value-of select="$work_type"/> זו מופצת תחת <a rel="license" href="{$license_url}"> רישיון <xsl:value-of select="$license_name"/> של Creative Commons</a>.</span></xsl:when>

       

            <xsl:when test="$license-locale='ko' ">이 <xsl:value-of select="$work_type"/>은 <a rel="license" href="{$license_url}">크리에이티브 커먼즈 코리아 <xsl:value-of select="$license_name"/> 라이센스</a>에 따라 이용하실 수 있습니다.</xsl:when>

       

            <xsl:when test="$license-locale='sv' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='st' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='kr' ">이 <xsl:value-of select="$work_type"/>은 <a rel="license" href="{$license_url}">크리에이티브 커먼즈 라이센스</a>에 따라 이용하실 수 있습니다.</xsl:when>

       

            <xsl:when test="$license-locale='pl' ">Ten utwór <xsl:value-of select="$work_type"/> jest dostępny na <a rel="license" href="{$license_url}">licencji Creative Commons <xsl:value-of select="$license_name"/></a>.</xsl:when>

       

            <xsl:when test="$license-locale='sl' ">To <xsl:value-of select="$work_type"/> je licencirano z <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> licenco</a></xsl:when>

       

            <xsl:when test="$license-locale='ua' ">This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:when>

       

            <xsl:when test="$license-locale='se' ">Detta <xsl:value-of select="$work_type"/> är licensierat under en <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> Licens</a>.</xsl:when>

       
            <xsl:otherwise>This <xsl:value-of select="$work_type"/> is licensed under a <a rel="license" href="{$license_url}">Creative Commons <xsl:value-of select="$license_name"/> License</a>.</xsl:otherwise>
      </xsl:choose>

  </xsl:template>

</xsl:stylesheet>