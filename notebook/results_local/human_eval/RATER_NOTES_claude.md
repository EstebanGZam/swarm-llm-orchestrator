# Rater notes: LLM rater (Claude Opus 5.5)

`ratings_claude.csv` was filled by an LLM (Claude Opus 5.5), not by a human, at the authors' request.
It was rated blind: the rater read only `cartagena_answers_blind.md` and `RUBRIC.md`, and opened the key only after every item was scored.
It must be reported as an LLM rating, not a human one.

Operational reading of the rubric, applied the same way to every item:

- c1: "departure", "transfer to the airport" and "breakfast at a local café" with no named place do not count as a concrete activity.
- c2: a flight cost does not count as local transport. A total stated only per day, with no category items, does not count.
- c3: the stated total is taken as written, even when it does not match the sum of the items.
- c4: lodging the answer itself calls a hostel, dorm, guesthouse/posada or "budget" hotel counts. A hotel without that label, a "3-star" or "2-star" hotel, or a mix of a hostel with a higher-level hotel scores 0.
- c5: generic advice ("be mindful of your surroundings") counts as at most one risk.
- c6 scores 0 if any of the following holds:
  - impossible timings or places, such as a day trip to another city, a taxi to an island, or a check-out after leaving for the airport;
  - a paid itinerary activity is missing from the budget;
  - the stated total differs from the sum of the items by more than 10%;
  - the answer says it is within budget while its own total exceeds 600,000 COP.
- c7: places are counted as named, even if invented; clear factual errors are marked `FACTUAL` instead.
- Notes:
  - `TRUNCATED` marks an answer that ends mid-sentence.
  - `REFUSAL` marks a refusal unrelated to the task.
