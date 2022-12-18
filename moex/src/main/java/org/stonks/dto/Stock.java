package org.stonks.dto;

import com.fasterxml.jackson.annotation.JsonGetter;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSetter;
import lombok.*;

@AllArgsConstructor
@Builder
@EqualsAndHashCode
@ToString
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class Stock {
    private String ticker;
    private String shortStockName;

    @JsonSetter("secid")
    public void setTicker(String ticker) {
        this.ticker = ticker;
    }

    @JsonSetter("shortname")
    public void setShortStockName(String shortStockName) {
        this.shortStockName = shortStockName;
    }

    @JsonGetter("ticker")
    public String getTicker() {
        return ticker;
    }

    @JsonGetter("stockName")
    public String getShortStockName() {
        return shortStockName;
    }
}
