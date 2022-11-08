package org.stonks.dto;

import lombok.*;

@AllArgsConstructor
@Builder
@ToString
@EqualsAndHashCode
@Getter
@Setter
public class Stock {
    private final String ticker;
    private final String exchangeName;
    private final String stockName;
}
