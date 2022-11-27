package org.stonks.dto;

import lombok.*;

import java.time.OffsetDateTime;

@AllArgsConstructor
@NoArgsConstructor
@Builder
@ToString
@EqualsAndHashCode
@Getter
@Setter
public class GetDataInput {
	private String ticker;
	private String exchangeName;
	private Float timeframe;
	private OffsetDateTime from;
	private OffsetDateTime till;
}
