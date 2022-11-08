package org.stonks.service;

import org.springframework.stereotype.Service;
import org.stonks.dto.Bargaining;
import org.stonks.dto.StockList;

import java.time.OffsetDateTime;
import java.util.List;

/**
 *  Сервис для работы с Московской биржей
 */
@Service
public interface MoexService {
    /**
     *  Метод совершает список торгов за определенный период времени
     * @param ticker - тикер акции
     * @param timeframe - таймфрэйм торгов
     * @param from - с какой даты получить данные
     * @param till - по какую
     * @return - список торгов за данный период
     */
    List<Bargaining> getBargainingDataByTicker(
            String ticker,
            Float timeframe,
            OffsetDateTime from,
            OffsetDateTime till
    );

    /**
     *  Метод делает постраничный поиск акций
     * @param page - номер страницы
     * @param partOfName - часть названия акции (опционально)
     * @return - страница акций
     */
    StockList getStocksByPage(
            Integer page,
            String partOfName
    );
}
