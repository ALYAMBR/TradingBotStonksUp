package org.stonks.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

import java.time.OffsetDateTime;

@Builder
@AllArgsConstructor
@Getter
@Setter
public class Bargaining {
    private final String ticker;
    private final String per;
    private final OffsetDateTime date;
    private final Float open;
    private final Float high;
    private final Float low;
    private final Float close;
    private final Float vol;
}
