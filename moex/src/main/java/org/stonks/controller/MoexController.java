package org.stonks.controller;

import org.springframework.web.bind.annotation.*;
import org.stonks.dto.Bargaining;
import org.stonks.service.moex.MoexService;
import org.stonks.dto.GetDataInput;

import java.time.OffsetDateTime;
import java.util.List;

@RestController
public class MoexController {
	
	MoexService moexService;
	
	@GetMapping("/data/{ticker}")
	public List<Bargaining> getData(
			@PathVariable String ticker,
			@RequestParam String exchangeName,
			@RequestParam String timeframe,
			@RequestParam(required = false) String till,
			@RequestParam(required = false) String from) {
		return moexService.getBargainingDataByTicker(new GetDataInput(
				ticker,
				exchangeName,
				Float.parseFloat(timeframe),
				OffsetDateTime.parse(till),
				OffsetDateTime.parse(from)
		));
	}
}
