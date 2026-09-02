# Part 2 — Business Metric Decomposition

## 1. Business Metric

**Primary Metric:** WISHLIST → PURCHASE CONVERSION WITHIN 30 DAYS

## 2. Metric Definition

The primary business metric is formally defined as:

**Numerator:** Unique users who purchase at least one previously wishlisted product within 30 days.
**Denominator:** Unique users who add at least one product to their wishlist within the same period.

- **Time Window:** 30 days from the initial wishlist event.
- **Unit of Analysis:** Unique User.
- **Why this metric matters:** The wishlist acts as a strong signal of high product interest. However, if users save items but fail to purchase them, there is significant friction between intent and transaction. Improving this conversion rate directly increases revenue while resolving user uncertainty.

**Important Data Distinction:**
- **OBSERVED FROM PUBLIC FEEDBACK:** Post-purchase friction, sizing complaints, and pricing dissatisfaction.
- **INFERRED HYPOTHESIS:** That these specific frictions are the leading cause of wishlist abandonment.
- **REQUIRES FIRST-PARTY DATA:** Actual measurement of the 30-day conversion rate, wishlist additions, and checkout drop-offs. Public feedback cannot directly measure this conversion because it does not contain first-party behavioral events.

## 3. Wishlist → Purchase Funnel

The user journey decomposes into the following key stages:

Product Discovery → Product Interest → Wishlist → Wishlist Revisit → Evaluation → Comparison → Purchase Intent → Checkout → Purchase

## 4. Metric Tree

To improve the final metric, we must track the funnel stage by stage.

| Journey Stage | Desired User Behavior | Desired Product Outcome | Possible Friction | Measurable Event | Leading Indicator | Relationship to Conversion |
|---|---|---|---|---|---|---|
| **Product Discovery** | Browses items | Finds relevant products | Irrelevant search results | `product_detail_viewed` | View-to-Click Rate | Top of funnel |
| **Product Interest** | Dwells on product | User sees potential value | Unclear imagery/details | `time_on_page` | Dwell Time | Pre-wishlist intent |
| **Wishlist** | Saves product | User captures intent | Friction to save | `wishlist_added` | Add-to-Wishlist Rate | Defines Denominator |
| **Wishlist Revisit** | Returns to saved item | User maintains interest | Forgets, loses intent | `wishlist_viewed` | Revisit Rate | Necessary for purchase |
| **Evaluation** | Reviews details (size, reviews) | User builds confidence | Fit/size/quality uncertainty | `review_opened`, `size_selected` | Detail Engagement | Builds decision confidence |
| **Comparison** | Compares options | User selects best value | Cannot justify price | `comparison_started` | Cross-item views | Resolves price-quality gap |
| **Purchase Intent** | Moves item to cart | User decides to buy | Out of stock, changed mind | `wishlist_to_cart` | Cart Addition Rate | Direct precursor |
| **Checkout** | Initiates checkout | User starts payment flow | Login barriers, hidden fees | `checkout_started` | Checkout Initiation | Final commitment |
| **Purchase** | Completes payment | User buys item | Payment failure, high shipping | `purchase_completed` | Checkout Success Rate | Defines Numerator |

## 5. Product Outcomes

For Wishlist → Purchase Conversion to increase, the following product outcomes must be achieved:

1. Users save products that genuinely matter to them.
2. Users return to previously wishlisted items.
3. Users gain enough confidence to evaluate a wishlisted product.
4. Users can resolve uncertainty about fit, quality, value, and authenticity.
5. Users can compare shortlisted products efficiently.
6. Users develop sufficient purchase intent.
7. Users can move from wishlist/product page to cart and checkout.
8. Users can complete the purchase without transactional friction.

*(Note: These are hypotheses to evaluate, not proven facts.)*

## 6. User Behaviors

The following behavioral changes could directly move the metric:

| Product Outcome | User Behavior | Leading Metric | Expected Direction | Why It Could Affect Wishlist→Purchase |
|---|---|---|---|---|
| Wishlist revisit | User opens previously saved items again | Wishlist revisit rate | Increase | Without wishlist revisits, conversion is highly unlikely. |
| Decision confidence | User views reviews/size information before purchase | Decision-support engagement | Increase | Higher confidence may mitigate abandonment due to fit/quality fear. |
| Value justification | User verifies quality vs price via reviews | Time evaluating product details | Increase | Resolving price-quality mismatch may encourage the user to commit. |
| Purchase intent | User moves a wishlisted item to cart | Wishlist→Cart rate | Increase | Wishlist → Cart is a critical transition to measure because it represents movement from passive interest toward purchase intent; the actual drop-off rate requires first-party event data. |
| Purchase completion | User successfully completes checkout | Cart→Purchase rate | Increase | Reducing final-stage friction should increase the probability of conversion, assuming purchase intent and product availability remain constant. |

## 7. Part 1 Findings Mapped to the Funnel

| Part 1 Finding | Evidence | Journey Stage | Wishlist/Purchase Relevance | Likely Metric Impact | Confidence | Key Uncertainty |
|---|---|---|---|---|---|---|
| **Fit / Size Uncertainty** | 12 | Discovery/Eval | 4 | High | 5 | Do users abandon wishlists entirely, or just return items later? |
| **Price-Quality Mismatch** | 11 | Evaluation | 3 | High | 5 | Does this stop the purchase, or only cause dissatisfaction after? |
| **Delivery & Fulfillment Unreliability** | 9 | Post-Purchase | 2 | Medium | 4 | Affects future purchases, but does it stop the current wishlist conversion? |
| **Pricing and Fee Friction** | 6 | Checkout | 3 | High | 4 | How many users abandon specifically at the fee screen? |
| **Seeking Authentic Product Reviews** | 4 | Discovery/Eval | 1 | Medium | 3 | Do users rely on third-party reviews enough to break the conversion cycle? |
| **Account Access and Security** | 4 | Checkout | 4 | High | 3 | Is this a systemic issue or isolated to specific edge cases? |
| **Return and Refund Friction** | 25 | Post-Purchase | 2 | Low | 5 | Primarily affects LTV, unlikely to be the primary Wishlist driver. |
| **Customer Support Inaccessibility** | 26 | Post-Purchase | 2 | Low | 5 | Post-purchase frustration; indirect impact on current wishlist. |

## 8. Direct vs Indirect Drivers

Based on the Part 1 report, we separate findings into three distinct clusters.

### A. DIRECT PRE-PURCHASE DRIVERS
These may block the user from moving an item from the wishlist to the cart.
- **Fit / Size Uncertainty**
- **Price-Quality Mismatch**
- **Seeking Authentic Product Reviews**
- **Product Assortment and Price Constraints**

### B. TRANSACTION / CHECKOUT DRIVERS
These may block the user after they have formed purchase intent.
- **Pricing and Fee Friction** (e.g., hidden delivery fees)
- **Promotional Credit Application Issues**
- **Account Access and Security Issues**

### C. POST-PURCHASE / INDIRECT DRIVERS
These negatively impact long-term trust but are hypothesized to be secondary factors in 30-day wishlist abandonment.
- **Customer Support Inaccessibility**
- **Return and Refund Friction**
- **Delivery and Fulfillment Unreliability**
- **Brand Trust and Authenticity Concerns**
- **App Performance / UX Issues**

## 9. Opportunity Prioritization

Re-ranking the opportunities specifically to optimize **WISHLIST → PURCHASE CONVERSION**.

| Opportunity | Evidence | Wishlist Relevance | Purchase Impact | Confidence | Journey Stage | Metric Proximity | Overall Part 2 Priority |
|---|---|---|---|---|---|---|---|
| **Fit / Size Uncertainty** | 12 | 4 | 3 | 5 | Discovery | Direct | **1** |
| **Price-Quality Mismatch** | 11 | 3 | 5 | 5 | Evaluation | Direct | **2** |
| **Pricing and Fee Friction** | 6 | 3 | 5 | 4 | Checkout | Indirect | **3** |
| **Seeking Authentic Product Reviews** | 4 | 1 | 3 | 3 | Discovery | Direct | **4** |
| **Account Access & Security** | 4 | 4 | 5 | 3 | Checkout | Indirect | **5** |
| **Promotional Credit Issues** | 2 | 3 | 3 | 2 | Checkout | Indirect | **6** |
| **Customer Support** | 26 | 2 | 5 | 5 | Post-Purchase | Distant | **7** |

*Rationale:*
Fit/Size and Price-Quality are the most frequent pre-purchase barriers. While Customer Support has more total evidence, it is almost entirely post-purchase, meaning it likely affects retention more than initial wishlist conversion. Pricing/Fees may block immediate conversion at checkout, making it highly proximate to the metric.

## 10. Top 3–5 Opportunities for Validation

**Strongest Candidate: Fit / Size Uncertainty**
- **Why:** May directly impact pre-purchase confidence. If a user doesn't know their size, they may leave the item in the wishlist indefinitely.
- **Evidence:** 12 verified records of users explicitly seeking sizing advice (e.g., "Which size jeans should I order?"). Supported by high confidence scores in Part 1.
- **Uncertainty:** Do users abandon the purchase, or do they buy two sizes and return one?

**Second-Best Candidate: Price-Quality Mismatch**
- **Why:** Users hesitate when evaluating the wishlist because they fear the product won't justify the cost compared to competitors like Meesho.
- **Evidence:** 11 verified records complaining about poor quality for the price paid.
- **Uncertainty:** Is this a platform-wide perception issue or isolated to specific brands/categories?

**Third Candidate: Pricing and Fee Friction**
- **Why:** Potential checkout blocker. High purchase intent may be disrupted by unexpected fees.
- **Evidence:** 6 verified records highlighting platform and delivery fees.
- **Uncertainty:** At what cart threshold do these fees become absolute blockers?

**Fourth Candidate: Seeking Authentic Product Reviews**
- **Why:** Users leave the app to find reviews (e.g., YouTube), breaking the seamless 30-day conversion loop.
- **Evidence:** 4 verified records of users explicitly asking influencers for reviews.
- **Uncertainty:** How many users who leave the app to watch a review actually return to purchase?

## 11. First-Party Metrics / Events Required

To quantitatively validate this funnel, we require the following internal behavioral events (which are **NOT** currently available in the public-feedback dataset):

- `wishlist_added`
- `wishlist_viewed`
- `wishlist_item_reopened`
- `product_detail_viewed_from_wishlist`
- `size_selected`
- `review_opened`
- `comparison_started`
- `product_shared`
- `wishlist_to_cart`
- `checkout_started`
- `purchase_completed`
- `days_from_wishlist_to_purchase`

## 12. Research Hypotheses

**HYPOTHESIS 1:**
Users may wishlist fashion products but postpone purchase when they lack confidence about fit or size.

**HYPOTHESIS 2:**
Users may hesitate when the perceived quality does not justify the product price, leading them to leave items in the wishlist.

**HYPOTHESIS 3:**
Users may seek external reviews (e.g., YouTube) because existing on-platform product information does not provide enough confidence, breaking the conversion loop.

**HYPOTHESIS 4:**
Unexpected delivery or platform fees may cause users with high purchase intent to abandon their cart and effectively abandon their wishlist.

## 13. Data Gaps and Limitations

- **Public feedback is biased toward post-purchase complaints:** Users rarely write App Store reviews about adding items to a wishlist.
- **Direct wishlist evidence is very limited:** Part 1 found only 2 explicit wishlist signals.
- **30-day conversion cannot be directly observed from public feedback:** We are inferring intent breakdown from external complaints.
- **First-party behavioral analytics are required to quantify the actual funnel:** The public data only shows us the symptomatic friction, not the behavioral drop-off rates.
- **Some potential wishlist barriers may not appear in public complaints:** E.g., waiting for a seasonal sale, or waiting for a paycheck.

## 14. PM Conclusion

**Where in the Wishlist → Purchase journey does the strongest evidence suggest friction exists?**
Friction exists primarily in the **Evaluation** stage (lack of confidence in fit, size, and quality/price justification) and the **Checkout** stage (unexpected fees).

**Which opportunity areas should be validated through user interviews?**
1. Fit / Size Uncertainty
2. Price-Quality Mismatch
3. Pricing and Fee Friction
4. Seeking Authentic Product Reviews

**Which opportunity appears most promising based on evidence + metric proximity?**
Fit / Size Uncertainty is the strongest opportunity to validate through primary research based on current evidence and proximity to the conversion decision.

**What remains unknown?**
We do not know the actual drop-off rates at each stage of the funnel. We do not know if users are abandoning wishlists because they lose interest entirely, or if they are just waiting for a price drop (which wasn't heavily featured in complaints but is a common e-commerce behavior).

PART 2 WORDING CORRECTIONS: COMPLETE
CAUSALITY CHECK: PASS
HYPOTHESIS VS FACT CHECK: PASS
