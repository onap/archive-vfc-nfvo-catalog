/**
 * Copyright 2016 ZTE Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.openo.commontosca.catalog.model.externalservice.container;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.XMLFilterImpl;

/**
 * NamespaceFilter.
 * 
 * @author 10189609
 * 
 */
public class NamespaceFilter extends XMLFilterImpl {

  private String usedNamespaceUri;
  private boolean addNamespace;

  // State variable
  private boolean addedNamespace = false;

  /**
   * constructor.
   * @param namespaceUri namspace uri
   * @param addNamespace add namespace or not
   */
  public NamespaceFilter(String namespaceUri, boolean addNamespace) {
    super();

    if (addNamespace) {
      this.usedNamespaceUri = namespaceUri;
    } else {
      this.usedNamespaceUri = "";
    }
    this.addNamespace = addNamespace;
  }



  @Override
  public void startDocument() throws SAXException {
    super.startDocument();
    if (addNamespace) {
      startControlledPrefixMapping();
    }
  }



  @Override
  public void startElement(String arg0, String arg1, String arg2, Attributes arg3)
      throws SAXException {

    super.startElement(this.usedNamespaceUri, arg1, arg2, arg3);
  }

  @Override
  public void endElement(String arg0, String arg1, String arg2) throws SAXException {

    super.endElement(this.usedNamespaceUri, arg1, arg2);
  }

  @Override
  public void startPrefixMapping(String prefix, String url) throws SAXException {


    if (addNamespace) {
      this.startControlledPrefixMapping();
    } else {
      // Remove the namespace, i.e. don´t call startPrefixMapping for parent!
    }

  }

  private void startControlledPrefixMapping() throws SAXException {

    if (this.addNamespace && !this.addedNamespace) {
      // We should add namespace since it is set and has not yet been done.
      super.startPrefixMapping("", this.usedNamespaceUri);

      // Make sure we dont do it twice
      this.addedNamespace = true;
    }
  }

}
