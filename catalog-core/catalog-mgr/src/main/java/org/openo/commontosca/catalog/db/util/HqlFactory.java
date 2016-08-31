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

package org.openo.commontosca.catalog.db.util;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Arrays;

/**
 * a tool class for creating Hibernate's HQL.
 * 
 */
public class HqlFactory {

  private static final Logger logger = LoggerFactory.getLogger(HqlFactory.class);

  /**
   * get update hql.
   * @param obj the object that used to be generate the hql
   * @param excludeProperties the properties that need not to be used
   * @param filter the condition after "where"
   * @return hibernate hql
   */
  public static String getUpdateHql(Object obj, String[] excludeProperties, String filter) {
    StringBuffer hql = new StringBuffer();
    String objName = obj.getClass().getSimpleName();
    hql.append("update ");
    hql.append(objName);
    hql.append(" set ");
    Field[] fields = obj.getClass().getDeclaredFields();
    if (obj.getClass().getGenericSuperclass() != null) {
      Field[] parentFields = obj.getClass().getSuperclass().getDeclaredFields();
      fields = concat(fields, parentFields);
    }
    for (Field field : fields) {
      String name = field.getName();
      Method method = null;
      Object value = null;
      if (!contain(excludeProperties, name)) {
        String upperName = name.substring(0, 1).toUpperCase() + name.substring(1);
        try {
          method = obj.getClass().getMethod("get" + upperName);
          value = method.invoke(obj);
          if (value != null) {
            if (value instanceof String) {
              hql.append(name);
              hql.append("=");
              hql.append("'");
              hql.append(value);
              hql.append("'");
              hql.append(",");
            } else {
              hql.append(name);
              hql.append("=");
              hql.append(value);
              hql.append(",");
            }
          }
        } catch (Exception e1) {
          logger.error("error while creating update hql", e1);
        }
      }
    }

    String sql = hql.toString();
    sql = sql.substring(0, sql.lastIndexOf(","));
    if (filter != null) {
      sql = sql + " where " + filter;
    }
    logger.info("update hql is : " + sql);
    return sql;
  }

  /**
   * judge wether target contains src.
   * @param src String[]
   * @param target String
   * @return boolean
   */
  public static boolean contain(String[] src, String target) {
    if (src == null || src.length == 0 || target == null) {
      return false;
    } else {
      for (String str : src) {
        if(str.equals(target)){
          return true;
        }
      }
    }
    return false;
  }

  /**
   * concat two array.
   * @param first first array
   * @param second second array
   * @return T
   */
  public static <T> T[] concat(T[] first, T[] second) {
    T[] result = Arrays.copyOf(first, first.length + second.length);
    System.arraycopy(second, 0, result, first.length, second.length);
    return result;
  }

  public static String getOidFilter(String key, String value) {
    return key + "= '" + value + "'";
  }

  /**
   * get query hql.
   * @param data Object
   * @param column String
   * @return String
   */
  public static String getQueryHql(Object data, String column) {
    StringBuffer hql = new StringBuffer();
    String objName = data.getClass().getSimpleName();
    hql.append("select q.");
    hql.append(column);
    hql.append(" from ");
    hql.append(objName);
    hql.append(" as q where ");
    Field[] fields = data.getClass().getDeclaredFields();
    if (data.getClass().getGenericSuperclass() != null) {
      Field[] parentFields = data.getClass().getSuperclass().getDeclaredFields();
      fields = concat(fields, parentFields);
    }
    for (Field field : fields) {
      String name = field.getName();
      Method method = null;
      Object value = null;
      String upperName = name.substring(0, 1).toUpperCase() + name.substring(1);
      try {
        method = data.getClass().getMethod("get" + upperName);
        value = method.invoke(data);
        if (value != null) {
          if (value instanceof String) {
            hql.append("q." + name);
            hql.append("=");
            hql.append("'");
            hql.append(value);
            hql.append("'");
            hql.append(" and ");
          } else {
            hql.append("q." + name);
            hql.append("=");
            hql.append(value);
            hql.append("and ");
          }
        }
      } catch (Exception e1) {
        logger.error("error while creating update hql", e1);
      }
    }
    String sql = hql.toString();
    sql = sql.substring(0, sql.lastIndexOf("and"));

    logger.info("query hql is : " + sql);
    return sql.trim();
  }

  public static String getQueryHqlByFilter(Class mainObject, Object filterData, String foreignKey) {
    StringBuffer hql = new StringBuffer();
    String objName = mainObject.getSimpleName();
    // hql.append("select queryTable.");
    hql.append(" from ");
    hql.append(objName);
    hql.append(" as a where ");
    String filterHql = getQueryHql(filterData, foreignKey);
    hql.append("a." + foreignKey);
    hql.append(" in(");
    hql.append(filterHql);
    hql.append(")");
    logger.info("QueryHqlByFilter  is : " + hql);
    return hql.toString();
  }

  public static String getDeleteHqlByFilter(Class mainObject, Object filterData, String foreignKey) {
    StringBuffer hql = new StringBuffer();
    String objName = mainObject.getSimpleName();
    hql.append("delete from ");
    hql.append(objName);
    hql.append(" as b where ");
    String filterHql = getQueryHql(filterData, foreignKey);
    hql.append("b." + foreignKey);
    hql.append(" in(");
    hql.append(filterHql);
    hql.append(")");
    logger.info("DeleteHqlByFilter  is : " + hql);
    return hql.toString();
  }
}
