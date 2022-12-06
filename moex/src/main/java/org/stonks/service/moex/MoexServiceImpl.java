package org.stonks.service.moex;


import lombok.NonNull;
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
                        moexUrl + String.format("/iss/engines/stock/markets/shares/securities/%s/candles.xml?%s",
                                getDataInput.getTicker(), createVarsForGetBargaings(getDataInput)),
                        String.class
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
            moexUrl + securityInfoPath + "?" + createVarsForGetStocks(page, partOfName),
            String.class
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

    private String createVarsForGetBargaings(GetDataInput getDataInput) {
        StringBuilder queryVars = new StringBuilder();
        queryVars.append("from=" + getDataInput.getFrom().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")))
                .append("till=" + getDataInput.getTill().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")))
                .append("interval=" + getDataInput.getTimeframe());
        return queryVars.toString();
    }

    private String createVarsForGetStocks(Integer page, @NonNull String partOfName) {
        StringBuilder queryVars = new StringBuilder();
        queryVars.append("q=" + partOfName)
                .append("engine=stock")
                .append("market=shares")
                .append("limit=" + perPage)
                .append("start=" + perPage*(page-1));
        
        return queryVars.toString();
    }
}
