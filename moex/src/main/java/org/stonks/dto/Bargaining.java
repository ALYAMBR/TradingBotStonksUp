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
    private String ticker;
    private Float per;
    private OffsetDateTime date;
    private Float open;
    private Float high;
    private Float low;
    private Float close;
    private Integer vol;
}
