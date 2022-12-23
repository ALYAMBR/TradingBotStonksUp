package org.stonks.service.moex;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.json.JsonMapper;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.time.format.DateTimeFormatter;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.Collectors;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.stonks.dto.Bargaining;
import org.stonks.dto.BargainsResponse;
import org.stonks.dto.GetDataInput;
import org.stonks.dto.Stock;
import org.stonks.dto.StockList;
import org.stonks.service.moex.xmlHandlers.BargainingsXMLHandler;
import org.xml.sax.SAXException;

@Service
public class MoexServiceImpl implements MoexService {

    private final RestTemplate http;
    private final SAXParser parser;
    private final ObjectMapper mapper = new JsonMapper();

    private static final String RUB = "RUB";

    @Value("${urls.moex}")
    private String moexUrl;
    @Value("${stocks.moex.paging.perPage}")
    private Integer perPage;
    @Value("${urls.moex.stocks.path}")
    private String STOCKS_INFO_PATH;

    @Value("${urls.moex.stocks.path.without.query}")
    private String STOCKS_INFO_WITHOUT_QUERY_PATH;

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
    public BargainsResponse getBargainingDataByTicker(GetDataInput getDataInput) {
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
        
        return new BargainsResponse(RUB, result);
    }

    @Override
    public StockList getStocksByPage(Integer pageNum, String partOfName) {
        // TODO: убрать когда это апигвна поменяют и сделают нумерацю страниц с 0
        pageNum--;

        String responseBody = null;
        if (partOfName != null) {
            responseBody = http.getForEntity(
                    moexUrl + STOCKS_INFO_PATH,
                    String.class,
                    partOfName, perPage, pageNum * perPage).getBody();
        } else {
            responseBody = http.getForEntity(
                    moexUrl + STOCKS_INFO_WITHOUT_QUERY_PATH,
                    String.class,
                     perPage, pageNum * perPage).getBody();
        }

        try {
            JsonNode securities = mapper.readTree(responseBody).get(1).at("/securities");

            List<Stock> stocks = mapper.convertValue(securities,
                mapper.getTypeFactory().constructCollectionType(List.class, Stock.class));

            stocks = stocks.stream().distinct().collect(Collectors.toList());

            return new StockList(pageNum + 1, perPage, stocks.size(), stocks);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }


    private String createVarsForGetBargaings(GetDataInput getDataInput) {
        return "from=" + getDataInput.getFrom().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))
            + "&till=" + getDataInput.getTill()
            .format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))
            + "&interval=" + getDataInput.getTimeframe();
    }
}
