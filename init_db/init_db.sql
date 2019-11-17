CREATE TABLE machine_statistic
(
    machine   BIGINT,
    ts        TIMESTAMP,
    load_rate DOUBLE PRECISION,
    mileage   DOUBLE PRECISION,
    PRIMARY KEY (machine, ts)
)