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

package org.openo.commontosca.catalog.db.dao;

import io.dropwizard.hibernate.AbstractDAO;
import io.dropwizard.util.Generics;

import org.hibernate.Criteria;
import org.hibernate.HibernateException;
import org.hibernate.Query;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.criterion.Restrictions;
import org.openo.commontosca.catalog.db.exception.CatalogResourceException;
import org.openo.commontosca.catalog.db.util.HqlFactory;

import java.util.List;
import java.util.Map;


/**
 * a base class for Hibernate DAO classes. provide the common methods to create,delete,update and
 * query data.
 * 
 */
public class BaseDao<T> extends AbstractDAO<T> {

  /**
   * base dao constructor.
   * 
   * @param sessionFactory session factory
   */
  public BaseDao(SessionFactory sessionFactory) {
    super(sessionFactory);
    this.sessionFactory = sessionFactory;
    this.entityClass = Generics.getTypeParameter(getClass());
  }

  public String[] excludeProperties;
  private SessionFactory sessionFactory;
  protected Session session;
  private final Class<?> entityClass;

  @Override
  protected Session currentSession() {
    return this.session;
  }

  /**
   * update data.
   * 
   * @param data the object to update
   * @throws CatalogResourceException e1
   */
  public void update(T data, String filter) throws CatalogResourceException {
    try {
      String hql = HqlFactory.getUpdateHql(data, excludeProperties, filter);
      beginTransaction();
      Query query = this.session.createQuery(hql);
      query.executeUpdate();
      closeTransaction();
    } catch (Exception e1) {
      transactionRollBack();
      throw new CatalogResourceException("error while updating data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
  }

  /**
   * delete data.
   * 
   * @param data the object to delete
   * @throws CatalogResourceException e1
   */
  public void delete(T data) throws CatalogResourceException {
    try {
      beginTransaction();
      this.session.delete(data);
      closeTransaction();
    } catch (Exception e1) {
      transactionRollBack();
      throw new CatalogResourceException("error while deleting data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
  }

  /**
   * create data.
   * 
   * @param data the object to create
   * @return data
   * @throws CatalogResourceException e1
   */
  public T create(T data) throws CatalogResourceException {
    try {
      beginTransaction();
      session.save(data);
      closeTransaction();
    } catch (HibernateException e1) {
      transactionRollBack();
      throw new CatalogResourceException("error while creating data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
    return data;
  }

  /**
   * union query.
   * 
   * @param unionHql union hql
   * @return list
   * @throws CatalogResourceException e1
   */
  public List<T> unionQuery(String unionHql) throws CatalogResourceException {
    List<T> data;
    try {
      beginTransaction();
      Query query = this.session.createQuery(unionHql);
      data = query.list();
      closeTransaction();
    } catch (Exception e1) {
      transactionRollBack();
      throw new CatalogResourceException("error while union query data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
    return data;
  }

  /**
   * union delete.
   * 
   * @param unionHql union hql
   * @return int
   * @throws CatalogResourceException e1
   */
  public int unionDelete(String unionHql) throws CatalogResourceException {
    int num = 0;
    try {
      beginTransaction();
      Query query = this.session.createQuery(unionHql);
      num = query.executeUpdate();
      closeTransaction();
    } catch (Exception e1) {
      transactionRollBack();
      throw new CatalogResourceException("error while union query data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
    return num;
  }

  /**
   * query data.
   * 
   * @param queryParams the condition map used to query objects
   * @return data list
   * @throws CatalogResourceException e1
   */
  @SuppressWarnings("unchecked")
  public List<T> query(Map<String, String> queryParams) throws CatalogResourceException {
    List<T> result = null;
    try {
      beginTransaction();
      Criteria criteria = this.session.createCriteria(entityClass);
      for (String key : queryParams.keySet()) {
        criteria.add(Restrictions.eq(key, queryParams.get(key)));
      }
      result = (List<T>) criteria.list();
      closeTransaction();
    } catch (HibernateException e1) {
      throw new CatalogResourceException("error while querying data.errorMsg:" + e1.getMessage(),
          e1);
    } finally {
      closeSession();
    }
    return result;
  }

  protected void beginTransaction() {
    this.session = this.sessionFactory.openSession();
    this.session.beginTransaction();
  }

  protected void closeTransaction() {
    this.session.getTransaction().commit();
  }

  protected void closeSession() {
    this.session.close();
  }

  protected void transactionRollBack() {
    this.session.getTransaction().rollback();
  }

}
