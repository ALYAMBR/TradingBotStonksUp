package org.stonks.service.moex.xmlHandlers;

import org.stonks.model.moex.Security;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

import java.util.List;
import java.util.Objects;

public class SecuritiesXMLHandler extends DefaultHandler {
    private List<Security> securities;
    private String ticker;
    private String id;

    public SecuritiesXMLHandler(List<Security> securities, String ticker) {
        this.securities = securities;
        this.ticker = ticker;
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        if (qName.equals("data")) {
            id = attributes.getValue("id");
        }
        if (qName.equals("row") && Objects.equals(id, "boards")) {
            String engine = attributes.getValue("engine");
            String market = attributes.getValue("market");
            Security security = new Security();
            security.setEngine(engine);
            security.setMarket(market);
            security.setSecurity(ticker);
            securities.add(security);
        }
    }
}
