CREATE TABLE Rates (
    codename VARCHAR(3) PRIMARY KEY,
    rate DOUBLE NOT NULL,
    symbol VARCHAR(10)
);

INSERT INTO Rates
VALUES
    ('CAD', 1.2652320884, '$'), ('HKD', 7.7527413637, 'HK$'),
    ('ISK', 128.2875752329, 'kr'), ('PHP', 47.9314040729, '₱'),
    ('DKK', 6.1312556682, 'kr'), ('HUF', 295.2840300107, 'ft'),
    ('CZK', 21.1740456757, 'Kč'), ('GBP', 0.7191441999 ,'£'),
    ('RON', 4.0195399456, 'lei'), ('SEK', 8.2805672356, 'kr'),
    ('IDR', 13898.3510594443, 'Rp'), ('INR', 72.6094484294, '₹'),
    ('BRL', 5.3701047077, 'R$'), ('RUB', 73.3405886718, '₽'),
    ('HRK', 6.2428889439, 'kn'), ('JPY', 105.3013438866, '¥'),
    ('THB', 29.890345453, '฿'), ('CHF', 0.8905927941, 'CHF'),
    ('EUR', 0.8244702778, '€'), ('MYR', 4.0344628576, 'RM'),
    ('BGN', 1.6124989694, 'лв'), ('TRY', 6.9600131915, '₺'),
    ('CNY', 6.4582405804, '¥'), ('NOK', 8.406546294, 'kr'),
    ('NZD', 1.3838733614, '$'), ('ZAR', 14.4287245445, 'R'),
    ('USD', 1, '$'), ('MXN', 19.937752494, '$'),
    ('SGD', 1.3229450078, '$'), ('AUD', 1.2863385275, '$'),
    ('ILS', 3.2442080963, '₪'), ('KRW', 1102.4156979141, '₩'),
    ('PLN', 3.6989034545, 'zł')