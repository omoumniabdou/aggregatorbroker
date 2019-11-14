CREATE TABLE machine_statistic
(
    machine_id BIGINT,
    timestamp  TIMESTAMP,
    load_rate  DOUBLE PRECISION,
    mileage    DOUBLE PRECISION,
    PRIMARY KEY (machine_id, timestamp)
)