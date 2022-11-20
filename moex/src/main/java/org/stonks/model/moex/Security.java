package org.stonks.model.moex;

import lombok.*;

@Builder
@Setter
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class Security {
    private String engine;
    private String market;
    private String security;
}
