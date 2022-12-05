package org.stonks.service.moex;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.stonks.dto.Bargaining;
import org.stonks.dto.GetDataInput;
import org.stonks.dto.Stock;
import org.stonks.dto.StockList;
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

    @Value("${urls.moex}")
    private String moexUrl;
    @Value("${urls.moex.bargaining.path}")
    private String bargaingPath;
    @Value("${urls.moex.securities.path}")
    private String securityInfoPath;
    @Value("${stocks.moex.paging.perPage}")
    private Integer perPage;

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

        String responseBody =
                http.getForEntity(
                        moexUrl + bargaingPath + "?from={from}&till={till}&interval={interval}"
                        , String.class, createVarsForGetBargaings(getDataInput)
                ).getBody();

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

        for (Bargaining bargaining : result) {
            bargaining.setTicker(getDataInput.getTicker());
            bargaining.setPer(getDataInput.getTimeframe());
        }
        return result;
    }

    @Override
    public StockList getStocksByPage(Integer page, String partOfName) {
        List<Stock> result = new ArrayList<>();

        String responseBody = http.getForEntity(
            moexUrl + securityInfoPath + "?q={q}&engine={engine}&market={market}&limit={limit}&start={start}",
            String.class, createVarsForGetStocks(page, partOfName)
        ).getBody();

        if (responseBody == null) {
            throw new RuntimeException("Не удалось получить список акций");
        }

        InputStream targetStream = new ByteArrayInputStream(responseBody.getBytes());

        SecuritiesXMLHandler handler = new SecuritiesXMLHandler(result);
        try {
            parser.parse(targetStream, handler);
        } catch (SAXException | IOException e) {
            throw new RuntimeException("Не удалось распарсить акции");
        }

        return StockList.builder()
            .pageNum(page)
            .pageSize(perPage)
            .stocks(result)
            .totalCount(result.size())
            .build();
    }

    private Map<String, String> createVarsForGetBargaings(GetDataInput getDataInput) {
        Map<String, String> vars = new HashMap<>();
        vars.put("from", getDataInput.getFrom().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
        vars.put("till", getDataInput.getTill().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
        vars.put("interval", String.valueOf(getDataInput.getTimeframe()));
        vars.put("security", getDataInput.getTicker());
        return vars;
    }

    private Map<String, String> createVarsForGetStocks(Integer page, String partOfName) {
        Map<String, String> vars = new HashMap<>();
        if (partOfName != null && !(partOfName.isEmpty())) {
            vars.put("q", partOfName);
        }
        vars.put("engine", "stock");
        vars.put("market", "shares");
        vars.put("limit", String.valueOf(perPage));
        vars.put("start", String.valueOf(perPage*(page-1)));
        return vars;
    }
}
