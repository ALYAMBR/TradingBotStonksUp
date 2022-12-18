package org.stonks.controller;

import lombok.AllArgsConstructor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;
import org.stonks.dto.BargainsResponse;
import org.stonks.dto.StockList;
import org.stonks.service.moex.MoexService;
import org.stonks.dto.GetDataInput;

import java.time.OffsetDateTime;

@RestController
@AllArgsConstructor
public class MoexController {
	MoexService moexService;
	
	@GetMapping("/data/{ticker}")
	public BargainsResponse getData(
			@PathVariable String ticker,
			@RequestParam String exchangeName,
			@RequestParam String timeframe,
			@RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) String till,
			@RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) String from) {
		
		return moexService.getBargainingDataByTicker(new GetDataInput(
				ticker,
				exchangeName,
				Float.parseFloat(timeframe),
				OffsetDateTime.parse(from + "+00:00"),
				OffsetDateTime.parse(till + "+00:00")
		));
	}

	@GetMapping("/stocks")
	public StockList findStocks(
		@RequestParam(name = "page", defaultValue = "1") Integer page,
		@RequestParam(name = "query") String prefix) {
		return moexService.getStocksByPage(page, prefix);
	}
}
