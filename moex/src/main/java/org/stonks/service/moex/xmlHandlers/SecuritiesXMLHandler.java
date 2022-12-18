package org.stonks.service.moex.xmlHandlers;

import org.stonks.dto.Stock;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

import java.util.List;
import java.util.Objects;

public class SecuritiesXMLHandler extends DefaultHandler {
    private List<Stock> stocks;
    private String id;

    public SecuritiesXMLHandler(List<Stock> stocks) {
        this.stocks = stocks;
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        if (qName.equals("data")) {
            id = attributes.getValue("id");
        }
        if (qName.equals("row") && Objects.equals(id, "securities")) {
            String ticker = attributes.getValue("secid");
            String name = attributes.getValue("name");
            Stock stock = Stock.builder()
                .shortStockName(name)
                .ticker(ticker)
                .build();
            stocks.add(stock);
        }
    }
}
