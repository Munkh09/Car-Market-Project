CREATE INDEX idx_price ON carpost (price);

CREATE INDEX idx_mileage ON carpost(mileage);

CREATE INDEX idx_city ON carpost (city);

CREATE INDEX idx_model ON carpost(model);

CREATE INDEX idx_mpg ON carpost(mpg);

CREATE INDEX idx_carYear ON carpost(carYear);

CREATE INDEX idx_fuel ON carpost(fuel);

CREATE INDEX idx_email_pass ON useraccount(email, pass);
