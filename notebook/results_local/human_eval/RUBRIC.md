# Human rubric: Cartagena trip plans

Task given to every system: "Plan a 3-day trip to Cartagena, Colombia, for one university student with a total budget of
600,000 COP (lodging, food, local transport and activities; the flight is already paid)."

Rate each answer independently. Write 1 (yes) or 0 (no) for each criterion. When in doubt, write 0.

| Id | Criterion | Decision rule |
|---|---|---|
| c1 | Day-by-day itinerary for all 3 days | 1 if Day 1, Day 2 and Day 3 each have at least one concrete activity. |
| c2 | Itemized budget with a total | 1 if costs are given at least for lodging, food and local transport, AND an explicit total is stated. |
| c3 | Total within 600,000 COP | 1 if the stated total (the upper end, if a range) is ≤ 600,000 COP. 0 if there is no total or it is higher. |
| c4 | Budget lodging only | 1 if the lodging proposed is a hostel or a similar budget option, and no hotel above that level is proposed. |
| c5 | At least two risks with mitigation | 1 if at least two specific risks each come with a concrete mitigation. |
| c6 | Internal consistency | 1 if there are no impossible timings and the paid activities in the itinerary appear in the budget. |
| c7 | Concreteness | 1 if at least five specific places, neighborhoods or transport options in Cartagena are named. |

Optional `notes` column: write "FACTUAL" if you see a clear factual error.
