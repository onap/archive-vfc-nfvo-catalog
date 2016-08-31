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

package org.openo.commontosca.catalog.db.wrapper;

import com.google.gson.Gson;

import org.openo.commontosca.catalog.db.dao.BaseDao;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.BaseData;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.CatalogDbUtil;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;



/**
 * an abstract class for NFV wrapper class.
 * provide the common methods to process the CRUD rest request.
 * 
 */
public abstract class BaseHandler<T extends BaseData> {
  private static final Logger logger = LoggerFactory.getLogger(BaseHandler.class);

  public Gson gson = new Gson();

  /**
   * create date. 
   * @param data data to create
   * @param resouceType resouce type
   * @return T
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"unchecked", "rawtypes"})
  public T create(T data, String resouceType) throws CatalogResourceException {
    T rtnData = null;
    logger.info("BaseHandler:start create data.info:" + CatalogDbUtil.objectToString(data));
    try {
      check(data);
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      rtnData = (T) dao.create(data);
    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while creating " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler:create data end.info:" + CatalogDbUtil.objectToString(data));
    return rtnData;
  }

  /**
   * delete data.
   * @param data data to delete
   * @param resouceType resource type
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public void delete(T data, String resouceType) throws CatalogResourceException {
    logger.info("BaseHandler:start delete data.info:" + CatalogDbUtil.objectToString(data));
    try {
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      dao.delete(data);
    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while deleting " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler:delete data end");
  }

  /**
   * delete data.
   * @param queryParam query param
   * @param resouceType String
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public void delete(Map<String, String> queryParam, String resouceType)
      throws CatalogResourceException {
    logger.info("BaseHandler:start delete data by condition.info:"
        + CatalogDbUtil.objectToString(queryParam));
    List<T> datas;
    try {
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      datas = dao.query(queryParam);
      for (T data : datas) {
        delete(data, resouceType);
      }
    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while deleting " + resouceType, e1);
      throw e1;
    }

  }

  /**
   * update data.
   * @param data data to update
   * @param filter filter
   * @param resouceType resource type
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public void update(T data, String filter, String resouceType) throws CatalogResourceException {
    logger.info("BaseHandler:start update data .info:" + CatalogDbUtil.objectToString(data)
        + " filter:" + filter);
    try {
      check(data);
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      dao.update(data, filter);

    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while updating " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler:update data end ");
  }

  /**
   * query data.
   * @param queryParam query parameter
   * @param resouceType resource type
   * @return T list
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public List<T> query(Map<String, String> queryParam, String resouceType)
      throws CatalogResourceException {
    logger.info("BaseHandler:start query data .info:" + CatalogDbUtil.objectToString(queryParam));
    List<T> datas = null;
    try {
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      datas = dao.query(queryParam);

    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while querying " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler: query data end .info:" + CatalogDbUtil.objectToString(datas));
    return datas;
  }

  /**
   * union query.
   * @param filter filter
   * @param resouceType resource type
   * @return T list
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public List<T> unionQuery(String filter, String resouceType) throws CatalogResourceException {
    logger.info("BaseHandler:start union query data.fliter:" + filter);
    List<T> datas = null;
    try {
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      datas = dao.unionQuery(filter);

    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while union querying " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler:union query data end .info:" + CatalogDbUtil.objectToString(datas));
    return datas;
  }

  /**
   * union delete.
   * @param filter filter
   * @param resouceType resource type
   * @return int
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings({"rawtypes", "unchecked"})
  public int unionDelete(String filter, String resouceType) throws CatalogResourceException {
    logger.info("BaseHandler:start delete query data.fliter:" + filter);
    int num;
    try {
      BaseDao dao = DaoManager.getInstance().getDao(resouceType);
      num = dao.unionDelete(filter);

    } catch (CatalogResourceException e1) {
      logger.error("BaseHandler:error while union delete " + resouceType, e1);
      throw e1;
    }
    logger.info("BaseHandler:union delete data end .num:" + num);
    return num;
  }

  /**
   * check if the related object id exists in the system.
   * 
   * @param data data to check
   * @throws CatalogResourceException e
   */
  public abstract void check(T data) throws CatalogResourceException;

}
