package org.stonks.dto;

import lombok.*;

import java.time.OffsetDateTime;

@AllArgsConstructor
@Builder
@ToString
@EqualsAndHashCode
@Getter
@Setter
public class GetDataInput {
	private final String ticker;
	private final String exchangeName;
	private final Float timeframe;
	private final OffsetDateTime from;
	private final OffsetDateTime till;
}
