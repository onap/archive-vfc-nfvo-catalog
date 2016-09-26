/**
 * Copyright 2016 [ZTE] and others.
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
package org.openo.commontosca.catalog.wrapper;

import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.model.parser.AbstractModelParser;

public class TestYamlModelParser extends AbstractModelParser {

  /* (non-Javadoc)
   * @see org.openo.commontosca.catalog.model.parser.AbstractModelParser#parse(java.lang.String, java.lang.String)
   */
  @Override
  public String parse(String packageId, String fileLocation) throws CatalogResourceException {
    // TODO Auto-generated method stub
    return packageId;
  }

}
