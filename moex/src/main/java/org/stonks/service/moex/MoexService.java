package org.stonks.service.moex;

import org.stonks.dto.Bargaining;
import org.stonks.dto.GetDataInput;
import org.stonks.dto.StockList;

import java.util.List;

/**
 *  Сервис для работы с Московской биржей
 */
public interface MoexService {
    /**
     *  Метод совершает список торгов за определенный период времени
     * @param getDataInput - входные параметры для поиска
     * @return - список торгов за данный период
     */
    List<Bargaining> getBargainingDataByTicker(GetDataInput getDataInput);

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
