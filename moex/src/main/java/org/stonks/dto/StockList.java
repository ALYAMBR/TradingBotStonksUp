package org.stonks.dto;

import lombok.*;

import java.util.List;

@AllArgsConstructor
@Builder
@ToString
@EqualsAndHashCode
@Getter
@Setter
public class StockList {
    private final Integer pageNum;
    private final Integer pageSize;
    private final Integer totalCount;
    private final List<Stock> stocks;
}
