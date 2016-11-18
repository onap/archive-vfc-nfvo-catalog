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

package org.openo.commontosca.catalog.db.hibernate;

import com.google.common.collect.ImmutableList;

import com.fasterxml.jackson.datatype.hibernate4.Hibernate4Module;

import io.dropwizard.db.DataSourceFactory;
import io.dropwizard.hibernate.HibernateBundle;
import io.dropwizard.hibernate.SessionFactoryFactory;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;

import org.hibernate.SessionFactory;
import org.openo.commontosca.catalog.CatalogAppConfiguration;


public class HibernateBundleExt extends HibernateBundle<CatalogAppConfiguration> {

  private static final String DEFAULT_NAME = "hibernate";

  private SessionFactory sessionFactory;

  private final ImmutableList<Class<?>> entities;
  private final SessionFactoryFactory sessionFactoryFactory;

  protected HibernateBundleExt(Class<?> entity, Class<?>... entities) {
    this(ImmutableList.<Class<?>>builder().add(entity).add(entities).build(),
        new SessionFactoryFactory());
  }

  protected HibernateBundleExt(ImmutableList<Class<?>> entities,
      SessionFactoryFactory sessionFactoryFactory) {
    super(entities, sessionFactoryFactory);
    this.entities = entities;
    this.sessionFactoryFactory = sessionFactoryFactory;
  }

  public final void initializeExt(Bootstrap<?> bootstrap) {
    bootstrap.getObjectMapper().registerModule(createHibernate4Module());
  }

  /**
   * Override to configure the {@link Hibernate4Module}.
   */
  protected Hibernate4Module createHibernate4Module() {
    return new Hibernate4Module();
  }

  protected String name() {
    return DEFAULT_NAME;
  }

  public final void runExt(CatalogAppConfiguration configuration, Environment environment)
      throws Exception {
    final DataSourceFactory dbConfig = getDataSourceFactory(configuration);
    this.sessionFactory =
        sessionFactoryFactory.build(this, environment, dbConfig, entities, name());

  }

  public SessionFactory getSessionFactory() {
    return sessionFactory;
  }


  @Override
  public DataSourceFactory getDataSourceFactory(CatalogAppConfiguration configuration) {
    return configuration.getDataSourceFactory();
  }

}
