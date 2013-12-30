
"""
Django middleware to pretty print html output - uses xslt to prettyprint html
assumes lxml present
"""

import logging
import traceback
import lxml.html
import lxml.etree


DOCTYPE_PUBLIC = '-//W3C//DTD HTML'
DOCTYPE_SYSTEM = ''
WHITESPACE = '  '
INDENT_SEED = '&#xA;'

class OCDWhiteMiddleware:
    
    """
    Strips leading and trailing whitespace from response content.
    """
    
    def __init__(self):
        
        self.xslt = """<?xml version="1.0" encoding="UTF-8"?>
                  <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                      <xsl:output encoding="UTF-8" method="xml" doctype-public="%s" doctype-system="%s"/>
                      <xsl:param name="whitespace" select="'%s'"/>
                      <xsl:template match="* | comment()">
                          <xsl:param name="indent" select="'%s'"/>
                          <xsl:choose>
                              <xsl:when test="string-length(normalize-space(.)) = 0 and not(*) and not(contains('br|hr|meta|link',name()))">
                                  <xsl:value-of select="$indent"/>
                                  <xsl:copy>
                                      <xsl:copy-of select="@*"/>
                                      <xsl:comment> </xsl:comment>
                                  </xsl:copy>
                              </xsl:when>
                              <xsl:otherwise>
                                  <xsl:value-of select="$indent"/>
                                  <xsl:copy>
                                      <xsl:copy-of select="@*"/>
                                      <xsl:apply-templates>
                                          <xsl:with-param name="indent" select="concat($indent, $whitespace)"/>
                                      </xsl:apply-templates>
                                      <xsl:if test="*">
                                          <xsl:value-of select="$indent"/>
                                      </xsl:if>
                                  </xsl:copy>
                              </xsl:otherwise>
                          </xsl:choose>
                      </xsl:template>
                      <xsl:template match="text()[normalize-space(.)='']"></xsl:template>
                  </xsl:stylesheet>""" % (DOCTYPE_PUBLIC, DOCTYPE_SYSTEM, WHITESPACE, INDENT_SEED)
                  
        self.xslt_doc = lxml.etree.fromstring(self.xslt)
    
    def process_response(self, request, response):
        
        if(response.status_code == 200 and 'text/html' in response['Content-Type']):
            try:
                response_string = response.content.decode('utf8') 
                html = lxml.html.fromstring(response_string)
                transform = lxml.etree.XSLT(self.xslt_doc)            
                response.content = lxml.html.tostring(transform(html), encoding="UTF-8")
                return response
            except Exception:
                logging.warn("OCDWhiteMiddleware error @ %s\n%s" % (request.path,traceback.format_exc()))
                return response
        else:
            return response

