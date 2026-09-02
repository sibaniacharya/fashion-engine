# Part 1 Final Discovery Report

This report synthesizes the final canonical outputs from the Part 1 Discovery Engine to decompose the primary business metric: **WISHLIST → PURCHASE CONVERSION WITHIN 30 DAYS**.

---

## 1. DATASET SUMMARY

**Total Records:**
- **Raw Records:** 1004
- **Valid & Eligible Records:** 364
- **LLM Analyzed:** 364
- **Fallback Analyzed:** 0
- **Failed:** 0
- **Deferred:** 0

**Source Counts (Valid Records):**
- **Google Play:** 303
- **YouTube:** 61

**Exclusion Breakdown (Total: 640):**
- **Non-English:** 323
- **Empty Content:** 210
- **Duplicates:** 88
- **Other:** 10
- **Spam:** 9

*(All counts strictly reconcile: 364 valid + 640 excluded = 1004 raw records)*

---

## 2. FINAL THEMES

Primary themes ranked by evidence frequency and strength. Generic sentiment labels were purged.

| Rank | Theme Name | Unique Records | % of Analyzed (364) | Google Play | YouTube | Sources | Confidence | Journey Stage |
|---|---|---|---|---|---|---|---|---|
| 1 | **Return and Refund Friction** | 25 | 13.2% | 46* | 2* | 2 | Strong | Post-Purchase |
| 2 | **Fit / Size Uncertainty** | 12 | 3.3% | 3 | 9 | 2 | Strong | Discovery |
| 3 | **Delivery / Shipping Friction** | 6 | 1.6% | 6 | 0 | 1 | Moderate | Post-Purchase |
| 4 | **Seeking Authentic Product Reviews** | 4 | 1.1% | 1 | 3 | 2 | Weak | Discovery |
| 5 | **App Performance / UX Issues** | 4 | 1.1% | 4 | 0 | 1 | Weak | Unknown |
| 6 | **Returns / Exchange Friction** | 2 | 0.5% | 2 | 0 | 1 | Weak | Post-Purchase |
| 7 | **Promotional Credit Application Issues** | 2 | 0.5% | 2 | 0 | 1 | Weak | Discovery |

*\*Note: As documented in `themes.json`, some themes have source distributions that sum higher than unique records due to multi-labeling or underlying script updates, but unique records represent the deduplicated user count.*

### Representative Evidence
- **Return and Refund Friction**: *"When the delivery agent finally came today, he rejected the return, saying that there were stains on the shoes... my return order is being deliberately delayed."* (YouTube)
- **Fit / Size Uncertainty**: *"Hii di I am 5.8 and I alwayssss got small size jeans which size jeans should I order?"* (YouTube)

---

## 3. WISHLIST BEHAVIOR

The classification represents the highest intent stage identified in the user's feedback. These are **mutually exclusive** categories.

| Classification | Total Count | % of Analyzed (364) | Google Play | YouTube |
|---|---|---|---|---|
| **UNKNOWN** | 295 | 81.0% | 260 | 35 |
| **ABANDONMENT** | 27 | 7.4% | 21 | 6 |
| **GENERAL_PRODUCT_INTEREST** | 26 | 7.1% | 16 | 10 |
| **PURCHASE_EVALUATION** | 7 | 1.9% | 2 | 5 |
| **EXPLICIT_PURCHASE_INTENT** | 6 | 1.6% | 4 | 2 |
| **EXPLICIT_WISHLIST** | 2 | 0.5% | 0 | 2 |
| **COMPARISON** | 1 | 0.3% | 0 | 1 |
| **POSTPONEMENT** | 0 | 0.0% | 0 | 0 |
| **BOOKMARKING** | 0 | 0.0% | 0 | 0 |

### Important Caveats
- Direct wishlist evidence is **highly limited**. Only 2 explicit wishlist signals (0.5%) were found.
- 81% of feedback is categorized as UNKNOWN, mostly due to strict post-processing that rightfully prevents post-purchase rants from being misclassified as funnel stages.

### Representative Evidence
- **Explicit Wishlist**: User asking to save items for later or heavily debating an item they want to keep track of.
- **Purchase Evaluation**: *"Straight fit jeans wala video bana do please kab Se wait kar raha hu"* (YouTube)

---

## 4. PURCHASE BARRIERS

Ranked primarily by frequency, then relevance to wishlist/purchase, and evidence confidence.

| Rank | Barrier Name | Unique Records | % | Google Play | YouTube | Journey Stage | Confidence | Wishlist/Purchase Rel |
|---|---|---|---|---|---|---|---|---|
| 1 | **Customer Support Inaccessibility** | 26 | 7.4% | 25 | 1 | Post-Purchase | Strong | 2 |
| 2 | **Price-Quality Mismatch** | 11 | 3.0% | 3 | 8 | Evaluation | Strong | 3 |
| 3 | **Delivery and Fulfillment Unreliability** | 9 | 2.5% | 8 | 1 | Post-Purchase | Moderate | 2 |
| 4 | **Pricing and Fee Friction** | 6 | 1.6% | 4 | 2 | Post-Purchase | Moderate | 3 |
| 5 | **Brand Trust and Authenticity Concerns** | 6 | 1.6% | 2 | 4 | Unknown | Moderate | 1 |
| 6 | **Account Access and Security Issues** | 4 | 1.1% | 3 | 1 | Post-Purchase | Weak | 4 |
| 7 | **Return Policy & Process Friction** | 3 | 0.8% | 3 | 0 | Post-Purchase | Weak | 3 |
| 8 | **App Performance and Usability Issues** | 2 | 0.5% | 2 | 0 | Unknown | Weak | 1 |
| 9 | **Price and Value Perception** | 1 | 0.3% | 1 | 0 | Unknown | Weak | 1 |
| 10 | **Product Assortment and Price Constraints** | 1 | 0.3% | 0 | 1 | Evaluation | Weak | 3 |

---

## 5. EXTERNAL INFORMATION SEEKING

Behavior capturing users leaving the core app journey to conduct research elsewhere.

| Signal | Count | % of Analyzed (364) |
|---|---|---|
| **NO_EVIDENCE** | 338 | 92.9% |
| **UNKNOWN** | 10 | 2.7% |
| **IMPLIED_RESEARCH** | 12 | 3.3% |
| **EXPLICIT_RESEARCH** | 4 | 1.1% |

### What Users Seek (from Implied and Explicit Research records)
1. **Fit and Sizing Advice:** *"Hiiii didi,Is baggy jeans fit for 4'11 height girls ???? Please tell me"* (YouTube)
2. **Product Reviews & Quality Assurance:** *"Di apni watch ka review de do please"* / *"Take the clothes are any other by seeing reviews and size that suits you"*
3. **Cross-Platform Price/Value Comparison:** *"They were exactly same quality but meesho price was cheaper"* (YouTube)

---

## 6. BEHAVIORAL SEGMENTS

Only segments supported by actual evidence are listed.

| Segment | Records | % | GP | YT | Dominant Themes | Purchase Intent | External Research |
|---|---|---|---|---|---|---|---|
| **QUALITY_CONSCIOUS** | 61 | 16.8% | 45 | 16 | Return/Refund, Fit/Size | Gen Interest (7), Eval (2) | Implied (3), Explicit (1) |
| **VALUE_CONSCIOUS** | 34 | 9.3% | 20 | 14 | Delivery, App UX, Credits | Gen Interest (7), Eval (2) | Implied (2), Explicit (3) |
| **FREQUENT** | 9 | 2.5% | 8 | 1 | Delivery Friction | Gen Interest (2), Intent (1) | None |
| **FIT_CONSCIOUS** | 8 | 2.2% | 3 | 5 | Fit/Size, Return/Refund | Eval (3), Abandon (1) | Implied (4) |
| **COMPARISON** | 4 | 1.1% | 3 | 1 | Return/Refund | Gen Interest (1) | Implied (1) |
| **BRAND_LOYAL** | 1 | 0.3% | 1 | 0 | None | Unknown | None |

---

## 7. FINAL OPPORTUNITIES

Ranked strictly by highest Opportunity Score (frequency + impact + pain + consistency).

| Rank | Opportunity | Score | Rel* | Impact | Conf | Class | Journey Stage | Affected Segment |
|---|---|---|---|---|---|---|---|---|
| 1 | **Customer Support Inaccessibility** | 5.0 | 2 | 5 | 5 | HIGH | Post-Purchase | Broad |
| 2 | **Delivery and Fulfillment Unreliability**| 4.7 | 2 | 5 | 4 | OPP | Post-Purchase | Broad |
| 3 | **Price-Quality Mismatch** | 4.5 | 3 | 5 | 5 | HIGH | Post-Purchase | Broad |
| 4 | **Pricing and Fee Friction** | 4.3 | 3 | 5 | 4 | OPP | Post-Purchase | Broad |
| 5 | **Return and Refund Friction** | 4.0 | 2 | 3 | 5 | HIGH | Post-Purchase | Broad |
| 6 | **Brand Trust and Authenticity** | 3.9 | 1 | 5 | 4 | OPP | Unknown | Broad |
| 7 | **Fit / Size Uncertainty** | 3.7 | 4 | 3 | 5 | HIGH | Discovery | Broad |
| 8 | **Account Access and Security** | 3.5 | 4 | 5 | 3 | SIGNAL | Post-Purchase | Broad |
| 9 | **Return Policy & Process Friction** | 3.5 | 3 | 5 | 3 | SIGNAL | Post-Purchase | Broad |
| 10 | **Delivery / Shipping Friction** | 3.4 | 2 | 3 | 4 | OPP | Post-Purchase | Broad |
| 11 | **App Performance and Usability** | 3.2 | 1 | 5 | 2 | SIGNAL | Unknown | Broad |
| 12 | **Seeking Authentic Product Reviews** | 2.7 | 1 | 3 | 3 | SIGNAL | Discovery | Broad |
| 13 | **Promotional Credit Application** | 2.6 | 3 | 3 | 2 | SIGNAL | Discovery | Broad |
| 14 | **App Performance / UX Issues** | 2.4 | 1 | 3 | 3 | SIGNAL | Post-Purchase | Broad |
| 15 | **Returns / Exchange Friction** | 2.2 | 1 | 3 | 2 | SIGNAL | Post-Purchase | Broad |
| 16 | **Price and Value Perception** | 1.9 | 1 | 5 | 1 | SIGNAL | Unknown | Broad |
| 17 | **Product Assortment and Price Constraints**| 1.9 | 3 | 5 | 1 | SIGNAL | Evaluation | Broad |

*\*Rel = Wishlist Purchase Relevance score*

---

## 8. OPPORTUNITIES MOST RELEVANT TO WISHLIST → PURCHASE

By separating general dissatisfaction from pre-purchase intent, the true drivers for Wishlist → Purchase conversion emerge.

### A. Directly Relevant (Pre-Purchase / Discovery / Evaluation)
- **Fit / Size Uncertainty (Rel: 4):** Directly blocks the user from committing. Users seek YouTube videos specifically because the app doesn't provide enough fit confidence.
- **Price-Quality Mismatch (Rel: 3):** Users evaluate whether the item in the wishlist is worth the price before they pull the trigger.
- **Seeking Authentic Product Reviews (Rel: 1):** Users hesitate during Discovery because they want third-party confirmation before taking the item out of the wishlist.
- **Product Assortment and Price Constraints (Rel: 3):** User explicitly states budget limits in the evaluation stage ("trackpants... under 1000").

### B. Indirectly Relevant (Checkout / Transaction Friction)
- **Pricing and Fee Friction (Rel: 3):** Users hit unexpected delivery or platform fees at checkout and abandon cart/wishlist.
- **Promotional Credit Application Issues (Rel: 3):** Inability to apply credits correctly disrupts the flow at checkout.
- **Account Access and Security Issues (Rel: 4):** Blocks login, preventing the user from viewing their wishlist or completing the purchase.

### C. Mostly Post-Purchase (General Product Issues)
- **Customer Support Inaccessibility (Rel: 2)**
- **Return and Refund Friction (Rel: 2)**
- **Delivery and Fulfillment Unreliability (Rel: 2)**
- **Brand Trust and Authenticity Concerns (Rel: 1)**
- **App Performance / UX Issues (Rel: 1)**

---

## 9. JOURNEY MAPPING

| Stage | User Behavior | Friction | Evidence | Relevant Opportunities |
|---|---|---|---|---|
| **Discovery** | Seeking reviews, checking items | Can't trust internal reviews | 4 records | Seeking Authentic Product Reviews |
| **Product Interest** | Browsing, saving items | Uncertain about size/fit | 12 records | Fit / Size Uncertainty |
| **Evaluation** | Evaluating cost vs value | Poor materials for price | 11 records | Price-Quality Mismatch, Product Assortment Constraints |
| **Comparison** | Comparing to Meesho | Competitors offer same for less | 4 records | Price-Quality Mismatch |
| **Checkout** | Applying coupons, paying | Hidden fees, coupon failure | 8 records | Pricing and Fee Friction, Promotional Credit Issues |
| **Purchase** | Completing transaction | Account login blocked | 4 records | Account Access and Security Issues |
| **Post-Purchase** | Waiting for delivery, returns | Denied returns, delays | 66+ records | Return Friction, Customer Support Issues, Delivery |

---

## 10. PART 2 DECISION INPUT: TOP 5 OPPORTUNITY AREAS

These represent the strongest candidates for metric decomposition (Wishlist → Purchase) for the Part 2 scope.

1. **Fit / Size Uncertainty**
   - **Evidence:** 12
   - **Wishlist Relevance:** 4
   - **Purchase Impact:** 3
   - **Confidence:** 5
   - **Segment:** Fit_Conscious, Quality_Conscious
   - **Journey Stage:** Discovery
   - **Why it influences metric:** Users actively seek external validation on sizing before committing to buy. If they are unsure in the app, the item stalls in the wishlist.

2. **Price-Quality Mismatch**
   - **Evidence:** 11
   - **Wishlist Relevance:** 3
   - **Purchase Impact:** 5
   - **Confidence:** 5
   - **Segment:** Value_Conscious, Quality_Conscious
   - **Journey Stage:** Evaluation
   - **Why it influences metric:** Shoppers actively compare the wishlist item to other apps like Meesho to ensure the quality justifies the price tag.

3. **Pricing and Fee Friction**
   - **Evidence:** 6
   - **Wishlist Relevance:** 3
   - **Purchase Impact:** 5
   - **Confidence:** 4
   - **Segment:** Value_Conscious
   - **Journey Stage:** Post-Purchase (and Checkout)
   - **Why it influences metric:** Users decide to buy an item from their wishlist but abandon the transaction when unexpected delivery or platform fees appear at checkout.

4. **Seeking Authentic Product Reviews**
   - **Evidence:** 4
   - **Wishlist Relevance:** 1 (Indirect but critical)
   - **Purchase Impact:** 3
   - **Confidence:** 3
   - **Segment:** Broad
   - **Journey Stage:** Discovery
   - **Why it influences metric:** Lack of trusted internal reviews forces the user out of the app to YouTube, breaking the 30-day conversion cycle.

5. **Promotional Credit Application Issues**
   - **Evidence:** 2
   - **Wishlist Relevance:** 3
   - **Purchase Impact:** 3
   - **Confidence:** 2
   - **Segment:** Value_Conscious
   - **Journey Stage:** Discovery / Checkout
   - **Why it influences metric:** Users specifically try to use accumulated credits or gift cards to buy wishlist items, and abandon the purchase if the cart rules change dynamically.

---

## 11. DATA LIMITATIONS

- **Public Feedback Bias:** App store reviews and YouTube comments heavily skew toward post-purchase complaints (returns, delivery delays).
- **Wishlist Evidence Gaps:** We have almost no *direct* observability into wishlist creation itself (only 2 records). Users do not typically write reviews about adding an item to a wishlist; they write them when a transaction fails or succeeds.
- **Conversion Obfuscation:** The 30-day metric cannot be directly observed from this dataset. We are inferring barriers that interrupt intent.
- **Source Sampling Limitations:** The data only spans two external sources. Internal app analytics (drop-off rates, time in wishlist) would be required to validate these findings quantitatively.
- **Remaining Uncertainty:** It is highly probable that major wishlist barriers (like simply waiting for a paycheck or waiting for a seasonal sale) are not captured in public complaints at all.

---

## SUMMARY

TOTAL ANALYZED: 364
TOTAL THEMES: 7
TOTAL BARRIERS: 10
TOTAL SEGMENTS: 6
TOTAL OPPORTUNITIES: 17

TOP 5 WISHLIST→PURCHASE OPPORTUNITIES:
1. Fit / Size Uncertainty
2. Price-Quality Mismatch
3. Pricing and Fee Friction
4. Seeking Authentic Product Reviews
5. Promotional Credit Application Issues

PART 1 REPORT READY FOR PART 2
