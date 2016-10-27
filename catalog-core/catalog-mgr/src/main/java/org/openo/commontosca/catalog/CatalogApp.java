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
package org.openo.commontosca.catalog;

import com.fasterxml.jackson.annotation.JsonInclude;

import io.dropwizard.Application;
import io.dropwizard.assets.AssetsBundle;
import io.dropwizard.db.DataSourceFactory;
import io.dropwizard.hibernate.HibernateBundle;
import io.dropwizard.migrations.MigrationsBundle;
import io.dropwizard.server.SimpleServerFactory;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import io.swagger.jaxrs.config.BeanConfig;
import io.swagger.jaxrs.listing.ApiListingResource;

import java.util.EnumSet;

import javax.servlet.DispatcherType;

import org.eclipse.jetty.servlets.CrossOriginFilter;
import org.glassfish.jersey.media.multipart.MultiPartFeature;
import org.openo.commontosca.catalog.common.Config;
import org.openo.commontosca.catalog.common.HttpServerAddrConfig;
import org.openo.commontosca.catalog.common.HttpServerPathConfig;
import org.openo.commontosca.catalog.common.MsbAddrConfig;
import org.openo.commontosca.catalog.common.ServiceRegistrer;
import org.openo.commontosca.catalog.db.dao.DaoManager;
import org.openo.commontosca.catalog.db.entity.NodeTemplateData;
import org.openo.commontosca.catalog.db.entity.PackageData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateData;
import org.openo.commontosca.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.commontosca.catalog.health.ConsoleHealthCheck;
import org.openo.commontosca.catalog.resources.PackageResource;
import org.openo.commontosca.catalog.resources.TemplateResource;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class CatalogApp extends Application<CatalogAppConfiguration> {

  private static final Logger LOGGER = LoggerFactory.getLogger(CatalogApp.class);

  public static void main(String[] args) throws Exception {
    new CatalogApp().run(args);
  }

  @Override
  public String getName() {
    return "OPENO-Catalog";
  }

  private final HibernateBundle<CatalogAppConfiguration> bundle =
      new HibernateBundle<CatalogAppConfiguration>(ServiceTemplateData.class, PackageData.class,
          NodeTemplateData.class, ServiceTemplateMappingData.class) {
        @Override
        public DataSourceFactory getDataSourceFactory(CatalogAppConfiguration configuration) {
          return configuration.getDataSourceFactory();
        }
      };

  @Override
  public void initialize(Bootstrap<CatalogAppConfiguration> bootstrap) {
    bootstrap.addBundle(new AssetsBundle("/api-doc", "/api-doc", "index.html", "api-doc"));
    initDb(bootstrap);
  }

  private void initDao() {
    DaoManager.getInstance().setSessionFactory(bundle.getSessionFactory());
  }

  private void initDb(Bootstrap<CatalogAppConfiguration> bootstrap) {
    bootstrap.addBundle(bundle);
    bootstrap.addBundle(new MigrationsBundle<CatalogAppConfiguration>() {
      @Override
      public DataSourceFactory getDataSourceFactory(CatalogAppConfiguration configuration) {
        return configuration.getDataSourceFactory();
      }
    });
  }

  @Override
  public void run(CatalogAppConfiguration configuration, Environment environment) {
    LOGGER.info("Start to initialize catalogue.");
    MsbAddrConfig.setMsbAddress(configuration.getMsbServerAddr());
    HttpServerAddrConfig.setHttpServerAddress(configuration.getHttpServerAddr());
    HttpServerPathConfig.setHttpServerPath(configuration.getHttpServerPath());
    initDao();
    final ConsoleHealthCheck healthCheck = new ConsoleHealthCheck(configuration.getTemplate());
    environment.healthChecks().register("template", healthCheck);

    environment.jersey().register(new PackageResource());
    environment.jersey().register(new TemplateResource());
    // environment.jersey().register(new VNFHostImageResource());
    // environment.jersey().register(new VNFSoftwareVersionResource());

    // register rest interface
    environment.jersey().packages("org.openo.commontosca.catalog.resources");
    // upload file by inputstream need to register MultiPartFeature
    environment.jersey().register(MultiPartFeature.class);

    initSwaggerConfig(environment, configuration);
    initCometd(environment);
    Config.setConfigration(configuration);
    initService();
    LOGGER.info("Initialize catalogue finished.");
  }

  /**
   * initialize swagger configuration.
   * 
   * @param environment environment information
   * @param configuration catalogue configuration
   */
  private void initSwaggerConfig(Environment environment, CatalogAppConfiguration configuration) {
    environment.jersey().register(new ApiListingResource());
    environment.getObjectMapper().setSerializationInclusion(JsonInclude.Include.NON_NULL);

    BeanConfig config = new BeanConfig();
    config.setTitle("Open-o Catalog Service rest API");
    config.setVersion("1.0.0");
    config.setResourcePackage("org.openo.commontosca.catalog.resources");
    // set rest api basepath in swagger
    SimpleServerFactory simpleServerFactory =
        (SimpleServerFactory) configuration.getServerFactory();
    String basePath = simpleServerFactory.getApplicationContextPath();
    String rootPath = simpleServerFactory.getJerseyRootPath();
    rootPath = rootPath.substring(0, rootPath.indexOf("/*"));
    basePath =
        basePath.equals("/") ? rootPath : (new StringBuilder()).append(basePath).append(rootPath)
            .toString();
    config.setBasePath(basePath);
    config.setScan(true);
  }

  private void initService() {
    Thread registerCatalogService = new Thread(new ServiceRegistrer());
    registerCatalogService.setName("register catalog service to Microservice Bus");
    registerCatalogService.start();
  }

  /**
   * initialize cometd server.
   * 
   * @param environment environment information
   */
  private void initCometd(Environment environment) {
    // add filter
    environment.getApplicationContext().addFilter(CrossOriginFilter.class,
        "/openoapi/catalog/v1/catalognotification/*", EnumSet.of(DispatcherType.REQUEST, DispatcherType.ERROR));
    // add servlet
    environment.getApplicationContext()
        .addServlet("org.cometd.server.CometDServlet", "/openoapi/catalog/v1/catalognotification/*")
        .setInitOrder(1);
    // add servlet
    environment.getApplicationContext()
        .addServlet("org.openo.commontosca.catalog.cometd.CometdServlet", "/openoapi/catalog/v1/catalognotification")
        .setInitOrder(2);
  }
}
