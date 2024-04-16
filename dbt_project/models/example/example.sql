SELECT
    'MSFT' AS symbol,
    (daily_data._2__high + daily_data._3__low / 2 ) / exchange_rates.value_usd AS avg_price_at_currency,
    (daily_data._5__volume / 1440) AS avg_num_trades,
    exchange_rates.currency_code,
    CURRENT_TIMESTAMP() AS processing_date
FROM
    {{ source(
        'source_data',
        'time_series_daily'
    ) }}
    daily_data
    LEFT JOIN {{ ref(
        'exchange_rates'
    ) }}
    exchange_rates
    ON TRUE
