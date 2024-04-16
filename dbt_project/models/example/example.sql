SELECT
    CURRENT_TIMESTAMP() as date,
    symbol,
    daily_data.avg_price / exchange_rates.value_usd AS avg_price_at_currency,
    exchange_rates.currency_code
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
