package org.stonks.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.stonks.dto.Bargaining;
import org.stonks.dto.GetDataInput;
import org.stonks.service.MoexService;

import java.util.List;

@RestController
public class MoexController {
	
	@Autowired
	MoexService moexService;
	
	@GetMapping("/data/{ticker}")
	public List<Bargaining> getData(@RequestBody GetDataInput getDataInput) {
		return moexService.getBargainingDataByTicker(getDataInput);
	}
}
