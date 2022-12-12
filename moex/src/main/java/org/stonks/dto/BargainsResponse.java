package org.stonks.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@AllArgsConstructor
@Getter
@Setter
public class BargainsResponse {
	String currency;
	List<Bargaining> bargainings;
}
