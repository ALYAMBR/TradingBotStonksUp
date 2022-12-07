package org.stonks.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.stonks.dto.Bargaining;
import org.stonks.service.moex.MoexService;
import org.stonks.dto.GetDataInput;

import java.time.OffsetDateTime;
import java.util.List;

@RestController
public class MoexController {
	
	@Autowired
	MoexService moexService;
	
	@GetMapping("/data/{ticker}")
	public List<Bargaining> getData(
			@PathVariable String ticker,
			@RequestParam String exchangeName,
			@RequestParam String timeframe,
			@RequestParam String till,
			@RequestParam String from) {
		till.replaceAll("%3A", ":");
		till.replaceAll("%2B", "+");
		
		from.replaceAll("%3A", ":");
		from.replaceAll("%2B", "+");
		return moexService.getBargainingDataByTicker(new GetDataInput(
				ticker,
				exchangeName,
				Float.parseFloat(timeframe),
				OffsetDateTime.parse(from),
				OffsetDateTime.parse(till)
		));
	}
}
