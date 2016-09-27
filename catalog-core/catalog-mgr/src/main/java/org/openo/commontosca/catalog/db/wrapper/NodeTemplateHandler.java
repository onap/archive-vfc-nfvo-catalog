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
package org.openo.commontosca.catalog.db.wrapper;

import org.openo.commontosca.catalog.db.common.CatalogResuorceType;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.Map;

public class NodeTemplateHandler extends BaseHandler<NodeTemplateData> {
  private static final Logger logger = LoggerFactory.getLogger(NodeTemplateHandler.class);

  /**
   * query node template.
   * @param queryParam query parameter
   * @return NodeTemplateData list
   * @throws CatalogResourceException e
   */
  public ArrayList<NodeTemplateData> query(Map<String, String> queryParam)
      throws CatalogResourceException {
    logger.info("NodeTemplateHandler query nodeTemplate info.");
    ArrayList<NodeTemplateData> data = new ArrayList<NodeTemplateData>();
    Object result = query(queryParam, CatalogResuorceType.NODETEMPLATE.name());
    if (result != null) {
      data = (ArrayList<NodeTemplateData>) result;
    } else {
      logger.warn("NodeTemplateHandler: query nodeTemplate info is null.");
    }
    logger.info("NodeTemplateHandler: query nodeTemplate info end.");
    return data;

  }

  @Override
  public void check(NodeTemplateData nodeTemplateData) throws CatalogResourceException {

  }

}
