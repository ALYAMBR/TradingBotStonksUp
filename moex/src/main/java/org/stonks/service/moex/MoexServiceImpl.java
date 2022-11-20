package org.stonks.service.moex;

import jdk.nashorn.internal.objects.annotations.Property;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.stonks.dto.Bargaining;
import org.stonks.dto.GetDataInput;
import org.stonks.dto.StockList;
import org.stonks.model.moex.Security;
import org.stonks.service.moex.xmlHandlers.BargainingsXMLHandler;
import org.stonks.service.moex.xmlHandlers.SecuritiesXMLHandler;
import org.xml.sax.SAXException;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
public class MoexServiceImpl implements MoexService {
    private final RestTemplate http;
    private final SAXParser parser;

    @Property(name = "urls.moex")
    private String moexUrl;
    @Property(name = "urls.moex.bargaining.path")
    private String bargaingPath;
    @Property(name = "urls.moex.securitiesInfo.path")
    private String securityInfoPath;


    @Autowired
    public MoexServiceImpl(RestTemplateBuilder http) {
        this.http = http.build();
        SAXParserFactory factory = SAXParserFactory.newInstance();
        try {
            parser = factory.newSAXParser();
        } catch (ParserConfigurationException | SAXException e) {
            throw new RuntimeException("Не удалось сконфигурировать сервис");
        }
    }

    @Override
    public List<Bargaining> getBargainingDataByTicker(GetDataInput getDataInput) {
        List<Bargaining> result = new LinkedList<>();
        List<Security> securities = getSecurityByName(getDataInput.getTicker());
        for (Security security : securities) {
            String responseBody =
                    http.getForEntity(
                            moexUrl + bargaingPath + "?from={from}&till={till}&interval={interval}"
                            , String.class, createVarsForGetBargaings(getDataInput, security)).getBody();

            if (responseBody == null) {
                throw new RuntimeException("Не удалось получить свечи");
            }
            InputStream targetStream = new ByteArrayInputStream(responseBody.getBytes());
            BargainingsXMLHandler handler = new BargainingsXMLHandler(result);
            try {
                parser.parse(targetStream, handler);
            } catch (SAXException | IOException e) {
                throw new RuntimeException("Не удалось распарсить свечи");
            }
        }
        for (Bargaining bargaining : result) {
            bargaining.setTicker(getDataInput.getTicker());
            bargaining.setPer(getDataInput.getTimeframe());
        }
        return result;
    }

    @Override
    public StockList getStocksByPage(Integer page, String partOfName) {
        return null;
    }

    private Map<String, String> createVarsForGetBargaings(GetDataInput getDataInput, Security security) {
        Map<String, String> vars = new HashMap<>();
        vars.put("from", getDataInput.getFrom().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
        vars.put("till", getDataInput.getTill().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
        vars.put("interval", String.valueOf(getDataInput.getTimeframe()));
        vars.put("security", getDataInput.getTicker());
        vars.put("engine", security.getEngine());
        vars.put("market", security.getMarket());
        return vars;
    }

    //Метод получения Security по имени тикеру
    private List<Security> getSecurityByName(String ticker) {
        List<Security> securities = new LinkedList<>();
        SecuritiesXMLHandler handler = new SecuritiesXMLHandler(securities, ticker);
        Map<String, String> vars = new HashMap<>();
        vars.put("security", ticker);
        String xmlResponse = http.getForEntity(
                moexUrl + securityInfoPath, String.class, vars
        ).getBody();
        InputStream targetStream = new ByteArrayInputStream(xmlResponse.getBytes());
        try {
            parser.parse(targetStream, handler);
        } catch (IOException | SAXException e) {
            throw new RuntimeException("Ошибка при обработке xml документа");
        }
        return securities;
    }
}
