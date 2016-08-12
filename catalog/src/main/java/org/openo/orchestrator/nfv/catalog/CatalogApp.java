/**
 *     Copyright (C) 2016 ZTE, Inc. and others. All rights reserved. (ZTE)
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *             http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 */
package org.openo.orchestrator.nfv.catalog;

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
import org.openo.orchestrator.nfv.catalog.common.Config;
import org.openo.orchestrator.nfv.catalog.common.HttpServerAddrConfig;
import org.openo.orchestrator.nfv.catalog.common.HttpServerPathConfig;
import org.openo.orchestrator.nfv.catalog.common.MsbAddrConfig;
import org.openo.orchestrator.nfv.catalog.db.dao.DaoManager;
import org.openo.orchestrator.nfv.catalog.db.entity.NodeTemplateData;
import org.openo.orchestrator.nfv.catalog.db.entity.PackageData;
import org.openo.orchestrator.nfv.catalog.db.entity.ServiceTemplateData;
import org.openo.orchestrator.nfv.catalog.db.entity.ServiceTemplateMappingData;
import org.openo.orchestrator.nfv.catalog.health.ConsoleHealthCheck;
import org.openo.orchestrator.nfv.catalog.resources.PackageResource;
import org.openo.orchestrator.nfv.catalog.resources.TemplateResource;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.annotation.JsonInclude;

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
            new HibernateBundle<CatalogAppConfiguration>(ServiceTemplateData.class,
                    PackageData.class, NodeTemplateData.class, ServiceTemplateMappingData.class) {
                @Override
                public DataSourceFactory getDataSourceFactory(CatalogAppConfiguration configuration) {
                    return configuration.getDataSourceFactory();
                }
            };

    @Override
    public void initialize(Bootstrap<CatalogAppConfiguration> bootstrap) {
        bootstrap.addBundle(new AssetsBundle("/api-doc", "/api-doc", "index.html", "api-doc"));
        initDB(bootstrap);
    }

    private void initDao() {
        DaoManager.getInstance().setSessionFactory(bundle.getSessionFactory());
    }

    private void initDB(Bootstrap<CatalogAppConfiguration> bootstrap) {
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
        environment.jersey().packages("org.openo.orchestrator.nfv.catalog.resources");
        // upload file by inputstream need to register MultiPartFeature
        environment.jersey().register(MultiPartFeature.class);

        initSwaggerConfig(environment, configuration);
        initCometd(environment);
        Config.setConfigration(configuration);
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
        config.setResourcePackage("org.openo.orchestrator.nfv.catalog.resources");
        // set rest api basepath in swagger
        SimpleServerFactory simpleServerFactory =
                (SimpleServerFactory) configuration.getServerFactory();
        String basePath = simpleServerFactory.getApplicationContextPath();
        String rootPath = simpleServerFactory.getJerseyRootPath();
        rootPath = rootPath.substring(0, rootPath.indexOf("/*"));
        basePath =
                basePath.equals("/") ? rootPath : (new StringBuilder()).append(basePath)
                        .append(rootPath).toString();
        config.setBasePath(basePath);
        config.setScan(true);
    }

    /**
     * initialize cometd server.
     * 
     * @param environment environment information
     */
    private void initCometd(Environment environment) {
        environment.getApplicationContext().addFilter(CrossOriginFilter.class,
                "/api/nsoccataloguenotification/v1/*",
                EnumSet.of(DispatcherType.REQUEST, DispatcherType.ERROR));// add
                                                                          // filter
        environment
                .getApplicationContext()
                .addServlet("org.cometd.server.CometDServlet",
                        "/api/nsoccataloguenotification/v1/*").setInitOrder(1);// add
                                                                               // servlet
        environment
                .getApplicationContext()
                .addServlet("org.openo.orchestrator.nfv.catalog.cometd.CometdServlet",
                        "/api/nsoccataloguenotification/v1").setInitOrder(2);// add
                                                                             // servlet
    }
}
