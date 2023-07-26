-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Access the database using SQlite3
sqlite3 fiftyville.db

-- See database design
.schema

-- Look for crime scene reports related to the crime
SELECT * FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND street = 'Humphrey Street';

-- Filter crime scene report data to id and description
SELECT id, description FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND street = 'Humphrey Street';

-- Look for and filter data from interview related to the crime
-- First of three leads determined: theif seen at a bakery
SELECT id, transcript FROM interviews
WHERE month = 7
AND day = 28;

-- First lead: Go through bakery security logs for data related to the crime
SELECT hour, minute, id, activity, license_plate FROM bakery_security_logs
WHERE month = 7
AND day = 28;

-- Second lead: Go through atm transactions for data related to the crime
-- Confirm atm locations
SELECT DISTINCT atm_location FROM atm_transactions;

-- Confirm atm transaction types
SELECT DISTINCT transaction_type FROM atm_transactions;

-- Filter atm transactions on Leggett Street
-- Year of crime is assumed to be 2021
SELECT id, year, account_number, amount FROM atm_transactions
WHERE month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- Third lead: Go through phone calls related to the crime
-- Determine unit used in durations
-- Duration is assumed to be recorded in seconds
SELECT duration FROM phone_calls LIMIT 10;

-- Determine phone calls made for less than a minute
SELECT id, caller, receiver, duration
FROM phone_calls
WHERE year = 2021
AND month = 7
AND day = 28
AND duration < 60;

-- Fourth lead determined: Go through flights and airport data related to the crime
-- Supporting lead: flights to Paris
-- Suspects: Robert and Patrick
-- Determine airports
SELECT * FROM airports;

-- Determine flights to Paris
-- One flight to Paris confirmed
SELECT * FROM flights
JOIN airports ON airports.id = destination_airport_id
WHERE airports.id = (
    SELECT id FROM airports
    WHERE city = 'Paris'
);

-- Get passenger details on the targeted flight
SELECT passport_number FROM passengers
JOIN flights ON flights.id = flight_id
WHERE flights.id = (
    SELECT id from airports
    WHERE id = (
        SELECT id FROM airports
        WHERE city = 'Paris'
    )
);

-- Look more into possible suspects
-- Names not in database
SELECT phone_number, passport_number, license_plate FROM people
WHERE name = 'Robert';

SELECT phone_number, passport_number, license_plate FROM people
WHERE name = 'Patrick';

-- Retrace to bakery
-- Determine license plates seen during the morning of the crime
SELECT DISTINCT license_plate FROM bakery_security_logs
WHERE month = 7
AND day = 28
AND hour <= 12
AND activity = 'exit';

-- Retrace to interviews
-- Check if any leads can be acquired from interviews the day before the crime
-- None
SELECT id, description FROM crime_scene_reports
WHERE month = 7
AND day = 27
AND street = 'Humphrey Street';

-- Check if any leads can be acquired from interviews the day after the crime
-- None
SELECT id, description FROM crime_scene_reports
WHERE month = 7
AND day = 29
AND street = 'Humphrey Street';

-- Check available bank accounts
SELECT * FROM bank_accounts;

-- Tackle new connection: Determine possible suspects via their person ids
-- Get person ids connected to the bank account ids recorded with withdrawals during the crime
-- 8 possible ids
SELECT DISTINCT person_id FROM bank_accounts
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE bank_accounts.account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE month = 7
    AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
);

-- Cross reference current data to link most likely theifs
-- Three likely suspects are determined
-- Passport numbers do not match
SELECT DISTINCT name, passport_number FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE people.id IN (
    SELECT DISTINCT person_id FROM bank_accounts
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE bank_accounts.account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
) AND phone_number IN (
    SELECT DISTINCT caller FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
) AND license_plate IN (
    SELECT DISTINCT license_plate FROM bakery_security_logs
    WHERE month = 7
    AND day = 28
    AND hour <= 12
    AND activity = 'exit'
);

-- Redact and replace current flights, airports, & passport number data
-- Paris lead is wrong (logic in determing pertinent data is also wrong)
-- Determine flights during the day after the crime (via origin airport ids)
-- one possible origin determined
SELECT DISTINCT city FROM airports
JOIN flights ON flights.origin_airport_id = airports.id
WHERE airports.id IN (
    SELECT origin_airport_id FROM flights
    WHERE year = 2021
    AND month = 7
    AND day = 29
);

-- Get details from determined origin
SELECT * FROM airports
JOIN flights ON flights.origin_airport_id = airports.id
WHERE airports.id IN (
    SELECT origin_airport_id FROM flights
    WHERE year = 2021
    AND month = 7
) AND day = 29;

--  Determine destinations of suspected flights
SELECT DISTINCT city from airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE airports.id IN (
    SELECT destination_airport_id FROM airports
    JOIN flights ON flights.destination_airport_id = airports.id
    WHERE airports.id IN (
        SELECT origin_airport_id FROM flights
        WHERE year = 2021
        AND month = 7
    ) AND day = 29
);

-- Determine main flight (earliest flight the day after the crime)
SELECT * FROM airports
JOIN flights ON flights.origin_airport_id = airports.id
WHERE airports.id IN (
    SELECT origin_airport_id FROM flights
    WHERE year = 2021
    AND month = 7
) AND day = 29 ORDER BY hour;

--  Determine main flight destination
--  New York City
SELECT DISTINCT city from airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE airports.id = (
    SELECT destination_airport_id FROM airports
    JOIN flights ON flights.destination_airport_id = airports.id
    WHERE airports.id IN (
        SELECT origin_airport_id FROM flights
        WHERE year = 2021
        AND month = 7
    ) AND day = 29 ORDER BY hour LIMIT 1
);

-- Determine passengers on the NYC flight
SELECT passengers.flight_id, name, passengers.passport_number, passengers.seat
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.year = 2021
AND flights.month = 7
AND flights.day = 29
AND flights.hour = 8
AND flights.minute = 20
ORDER BY passengers.passport_number;

-- Cross reference with main suspects
-- Two main suspects remaining
SELECT DISTINCT name, passport_number FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE people.id IN (
    SELECT DISTINCT person_id FROM bank_accounts
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE bank_accounts.account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
) AND phone_number IN (
    SELECT DISTINCT caller FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
) AND license_plate IN (
    SELECT DISTINCT license_plate FROM bakery_security_logs
    WHERE month = 7
    AND day = 28
    AND hour <= 12
    AND activity = 'exit'
) AND passport_number IN (
    SELECT passengers.passport_number FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.year = 2021
    AND flights.month = 7
    AND flights.day = 29
    AND flights.hour = 8
    AND flights.minute = 20
);

-- Revise bakery security logs logic
SELECT DISTINCT name, passport_number FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE people.id IN (
    SELECT DISTINCT person_id FROM bank_accounts
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    WHERE bank_accounts.account_number IN (
        SELECT account_number FROM atm_transactions
        WHERE month = 7
        AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw'
    )
) AND phone_number IN (
    SELECT DISTINCT caller FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
) AND license_plate IN (
    SELECT DISTINCT license_plate FROM bakery_security_logs
    WHERE month = 7
    AND day = 28
    AND hour = 10
    AND activity = 'exit'
    AND bakery_security_logs.minute >= 15
    AND bakery_security_logs.minute <= 25
) AND passport_number IN (
    SELECT passengers.passport_number FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    WHERE flights.year = 2021
    AND flights.month = 7
    AND flights.day = 29
    AND flights.hour = 8
    AND flights.minute = 20
);

-- BRUCE IS THE THEIF

-- Determine accomplish
SELECT DISTINCT name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE people.phone_number IN (
    SELECT DISTINCT receiver FROM phone_calls
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller = (
        SELECT phone_number FROM people
        JOIN bank_accounts ON bank_accounts.person_id = people.id
        WHERE people.id IN (
            SELECT DISTINCT person_id FROM bank_accounts
            JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
            WHERE bank_accounts.account_number IN (
                SELECT account_number FROM atm_transactions
                WHERE month = 7
                AND day = 28
                AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw'
            )
        ) AND phone_number IN (
            SELECT DISTINCT caller FROM phone_calls
            WHERE year = 2021
            AND month = 7
            AND day = 28
            AND duration < 60
        ) AND license_plate IN (
            SELECT DISTINCT license_plate FROM bakery_security_logs
            WHERE month = 7
            AND day = 28
            AND hour = 10
            AND activity = 'exit'
            AND bakery_security_logs.minute >= 15
            AND bakery_security_logs.minute <= 25
        ) AND passport_number IN (
            SELECT passengers.passport_number FROM people
            JOIN passengers ON people.passport_number = passengers.passport_number
            JOIN flights ON passengers.flight_id = flights.id
            WHERE flights.year = 2021
            AND flights.month = 7
            AND flights.day = 29
            AND flights.hour = 8
            AND flights.minute = 20
        )
    )
);

-- ROBIN IS THE ACCOMPLICE