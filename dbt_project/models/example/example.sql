SELECT
    'MSFT' AS symbol,
    ((CAST(daily_data._2__high AS FLOAT64) + CAST(daily_data._3__low AS FLOAT64)) / 2 ) / exchange_rates.value_usd AS avg_price_at_currency,
    (CAST(daily_data._5__volume AS INT64) / 1440) AS avg_num_trades,
    exchange_rates.currency_code,
    _airbyte_extracted_at AS ingestion_date,
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
