package org.stonks.service.moex.xmlHandlers;

import org.stonks.dto.Bargaining;
import org.xml.sax.Attributes;
import org.xml.sax.helpers.DefaultHandler;

import java.time.LocalDate;
import java.time.LocalTime;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;

public class BargainingsXMLHandler extends DefaultHandler {
    private List<Bargaining> bargainings;

    public BargainingsXMLHandler(List<Bargaining> bargainings) {
        this.bargainings = bargainings;
    }


    public void startElement(String uri, String localName, String qName, Attributes attributes) {
        if (qName.equals("row")) {
            Double open = Double.parseDouble(attributes.getValue("open"));
            Double close = Double.parseDouble(attributes.getValue("close"));
            Double high = Double.parseDouble(attributes.getValue("high"));
            Double low = Double.parseDouble(attributes.getValue("low"));
            Integer vol = Integer.parseInt(attributes.getValue("volume"));

            String dateTimeStrValue = attributes.getValue("begin");
            String date = dateTimeStrValue.split(" ")[0];
            String time = dateTimeStrValue.split(" ")[1];
            bargainings.add(
                    Bargaining.builder()
                            .low(low.floatValue())
                            .high(high.floatValue())
                            .close(close.floatValue())
                            .open(open.floatValue())
                            .vol(vol)
                            .date(OffsetDateTime.of(LocalDate.parse(date), LocalTime.parse(time), ZoneOffset.UTC))
                            .build()
            );
        }
    }
}
